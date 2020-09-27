import boto3
import ulid
import logging
import time
import requests
import h1st_saas.config as config
import h1st_saas.util as util
from h1st_saas.gateway_controller import GatewayController


logger = logging.getLogger(__name__)


class WorkbenchController:
    def __init__(self):
        self._gw = GatewayController()

    def sync(self):
        dyn = boto3.client('dynamodb')

        pager = dyn.get_paginator('scan').paginate(
            TableName=config.DYNDB_TABLE,
            IndexName='status-task_arn-index',
        )

        results = []
        for page in pager:
            for i in page['Items']:
                r = self._flatten_item(i)

                if r['status'] != 'stopped':
                    item = self.refresh(r['user_id'], r['workbench_id'])
                    results.append(item)

                    if item['status'] != r['status']:
                        logger.info('Workbench %s: %s -> %s' % (
                            item['workbench_id'],
                            r['status'],
                            item['status']
                        ))

        return results

    def list_workbench(self, user):
        dyn = boto3.client('dynamodb')

        if user:
            resp = dyn.query(
                TableName=config.DYNDB_TABLE,
                KeyConditions={
                    'user_id': {
                        'AttributeValueList': [{'S': user}],
                        'ComparisonOperator': 'EQ'
                    }
                }
            )
        else:
            resp = dyn.scan(TableName=config.DYNDB_TABLE)

        result = []
        for i in resp['Items']:
            result.append(self._flatten_item(i))

        return result

    def launch(self, user, workbench_name=""):
        wid = util.random_char()  # TODO: conflict
        dyn = boto3.client('dynamodb')
        ecs = boto3.client('ecs')

        # TODO: detect when we reach max capacity
        if config.ECS_MAX_WB:
            pass

        user = str(user)

        if not workbench_name:
            workbench_name = "wb-" + wid
        else:
            workbench_name = str(workbench_name)

        task_arn = None

        try:
            result = self._start(user, wid, {
                'workbench_name': workbench_name,
            })
            task_arn = result['tasks'][0]['taskArn']
            version_arn = result['tasks'][0]['taskDefinitionArn']

            dyn.put_item(
                TableName=config.DYNDB_TABLE,
                Item={
                    'user_id': { 'S': user, },
                    'workbench_id': { 'S': wid, },
                    'workbench_name': { 'S': workbench_name },
                    'task_arn': { 'S': task_arn, },
                    'origin_task_arn': { 'S': task_arn, },
                    'version_arn': { 'S': version_arn },
                    'status': { 'S': 'starting' },
                    'desired_status': { 'S': 'running' },
                    'public_endpoint': { 'S': f'{config.BASE_URL}/{wid}/' },
                }
            )
        except:
            if task_arn is not None:
                ecs.stop_task(
                    cluster=config.ECS_CLUSTER,
                    task=task_arn,
                    reason='Launch failure',
                )

            raise

        return wid

    def get(self, user, wid, refresh=False):
        if refresh:
            return self.refresh(user, wid)

        return self._get_item(user, wid, True)

    def refresh(self, user, wid):
        """
        Refresh the status of a workbench and return the updated instance
        """
        ecs = boto3.client('ecs')
        ec2 = boto3.client('ec2')

        item = self._get_item(user, wid, True)

        update = {}
        
        if 'task_arn' in item:
            tasks = ecs.describe_tasks(cluster=config.ECS_CLUSTER, tasks=[item['task_arn']])['tasks']

            if tasks:
                task = tasks[0]

                ecs_status = task['lastStatus'].lower()

                # the private endpoint won't change during the lifecycle
                if ecs_status == 'running' and 'private_endpoint' not in item:
                    container = None

                    for i in range(len(task['containers'])):
                        if task['containers'][i]['name'] == 'workbench':
                            container = task['containers'][i]
                            break

                    containerPort = container['networkBindings'][0]['hostPort']
                    
                    containerInstances = ecs.describe_container_instances(
                        cluster=config.ECS_CLUSTER, containerInstances=[task['containerInstanceArn']]
                    )['containerInstances']
                    instanceId = containerInstances[0]['ec2InstanceId']

                    instances = (ec2.describe_instances(InstanceIds=[instanceId]))
                    privateAddr = (instances['Reservations'][0]['Instances'][0]['PrivateIpAddress'])

                    update['private_endpoint'] = f"http://{privateAddr}:{containerPort}"
                elif ecs_status == 'stopped':
                    # TODO: something is wrong here
                    logger.warn(f'Status is out of sync for workbench {wid}. Removing container info')
                    update['task_arn'] = None

                update['status'] = ecs_status
            else:
                logger.warn(f"Found invalid task arn {item['task_arn']} for workbench {wid}")
                update = {
                    'status': 'stopped',
                    'task_arn': None,
                    'private_endpoint': None,
                }
        else:
            update = {'status': 'stopped'}

        if 'private_endpoint' in update and update['private_endpoint'] != item.get('private_endpoint'):
            # TODO: the gateway should be able to pull this by itself
            self._gw.setup(wid, update['private_endpoint'])

            if config.WB_VERIFY_ENDPOINT == 'public' and 'public_endpoint' in item:
                try:
                    check = requests.head(item['public_endpoint'])
                    if check.status_code >= 400:
                        logger.warn(f"Workbench {wid} container status is running but endpoint return {check.status_code}")
                        update = {'status': 'pending'}
                    else:
                        logger.info(f'Workbench {wid} is ready, status: {check.status_code}')

                        # XXX: still need to give it sometime to be ready
                        # best case is probably to have workbench ping us back when it is ready
                except:
                    logger.warn('Unable to verify endpoint ' + item['public_endpoint'])
                    update = {'status': 'pending'}

        if update:
            # print(update)
            self._update_item(user, wid, update)

        item.update(update)
        return item

    def start(self, user, wid):
        """
        Start a stopped workbench
        """
        item = self._get_item(user, wid, True)
        task_arn = None

        if 'task_arn' not in item:
            try:
                result = self._start(user, wid, item)
                task_arn = result['tasks'][0]['taskArn']
                version_arn = result['tasks'][0]['taskDefinitionArn']

                self._update_item(user, wid, {
                    'task_arn': task_arn,
                    'version_arn': version_arn,
                    'status': 'starting',
                    'desired_status': 'running',
                    'origin_task_arn': task_arn,
                    'public_endpoint': f'{config.BASE_URL}/{wid}/',  # this to make sure it picks up latest endpoint config
                })
            except:
                if task_arn is not None:
                    ecs.stop_task(
                        cluster=config.ECS_CLUSTER,
                        task=task_arn,
                        reason='Launch failure',
                    )

                raise
        else:
            # TODO: make sure the container is running
            self.refresh(user, wid)

    def stop(self, user, wid):
        """
        Stop a workbench
        """
        ecs = boto3.client('ecs')

        item = self._get_item(user, wid)

        if 'task_arn' in item:
            ecs.stop_task(
                cluster=config.ECS_CLUSTER,
                task=item['task_arn']['S'],
                reason='Request by user'
            )

        self._update_item(user, wid, {
            'task_arn': None,
            'private_endpoint': None,
            'status': 'stopped',  # TODO: add "stopping" status
            'desired_status': 'stopped',
        })

        self._gw.destroy(wid)

    def destroy(self, user, wid):
        """
        Destroy a workbench, all data will be lost
        """
        self.stop(user, wid)
        dyn = boto3.client('dynamodb')
        dyn.delete_item(
            TableName=config.DYNDB_TABLE,
            Key=self._item_key(user, wid)
        )

    def _start(self, user, wid, item=None):
        ecs = boto3.client('ecs')
        item = item or {}

        wb_path = "/home/project"

        # TODO: save on s3
        envvar = [
            {'name': 'WORKBENCH_ID', 'value': str(wid)},
            {'name': 'WORKSPACE_PATH', 'value': wb_path},
            {'name': 'H1ST_MODEL_REPO_PATH', 'value': f"{wb_path}/.models"},
            {'name': 'PYTHONPATH', 'value': wb_path},
            {'name': 'GA_ID', 'value': config.GA_ID},
        ]

        # jupyter
        jupyter_url = f'{config.BASE_URL}/{wid}/jupyter'
        envvar += [
            {'name': 'JUPYTER_BASE_URL', 'value': jupyter_url},
            {'name': 'JUPYTER_APP_URL', 'value': jupyter_url},
            {'name': 'JUPYTER_WS_URL', 'value': jupyter_url.replace("https://", "wss://")},
            {'name': 'JUPYTER_TOKEN', 'value': 'abc'},
        ]

        if 'workbench_name' in item:
            envvar.append({'name': 'WORKBENCH_NAME', 'value': str(item['workbench_name'])})

        # override the command of the container
        ws_cmd = [
            "bash", "-c",
            f"set -ex && mkdir -p /efs/data/ws-{wid} && rm -rf {wb_path} && ln -s /efs/data/ws-{wid} {wb_path} && " + config.WB_BOOT_COMMAND,
        ]

        result = ecs.run_task(
            cluster=config.ECS_CLUSTER,
            taskDefinition=config.ECS_TASK_DEFINITION,
            overrides={
                'containerOverrides': [
                    {
                        'name': 'workbench',
                        'environment': envvar,
                        'cpu': config.WB_DEFAULT_CPU,
                        'memory': config.WB_DEFAULT_RAM,
                        "command": ws_cmd,
                    }
                ]
            },
            tags=[
                {'key': 'Project', 'value': 'H1st'},
                {'key': 'Workbench ID', 'value': wid},
                {'key': 'User ID', 'value': user},
            ]
        )

        return result

    def _item_key(self, user, wid):
        return {
            'user_id': {'S': user},
            'workbench_id': {'S': wid},
        }

    def _get_item(self, user, wid, flatten=False):
        dyn = boto3.client('dynamodb')
        item = dyn.get_item(
            TableName=config.DYNDB_TABLE,
            Key={
                'user_id': {'S': user},
                'workbench_id': {'S': wid},
            }).get('Item')

        if not item:
            raise RuntimeError("Workbench is not valid")

        if flatten:
            item = self._flatten_item(item)

        return item

    def _update_item(self, user, wid, data):
        updates = {}
        for k, v in data.items():
            if v is None:
                updates[k] = {'Action': 'DELETE'}
            else:
                updates[k] = {
                    'Action': 'PUT',
                    'Value': {'S': str(v)},
                }

        dyn = boto3.client('dynamodb')
        dyn.update_item(
            TableName=config.DYNDB_TABLE,
            Key=self._item_key(user, wid), 
            AttributeUpdates=updates
        )

    def _flatten_item(self, i):
        v = {}

        # flatten the dict
        for k in i:
            x = list(i[k].keys())[0]
            v[k] = i[k][x]

        return v
