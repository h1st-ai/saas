import boto3
import ulid
import logging
import time
import requests
import h1st_saas.util as util
from h1st_saas.gateway_controller import GatewayController
import h1st_saas.config as config


logger = logging.getLogger(__name__)


class DeploymentController:
    def __init__(self):
        self._gw = GatewayController()

    # def sync(self):
    #     dyn = boto3.client('dynamodb')

    #     pager = dyn.get_paginator('scan').paginate(
    #         TableName=config.INFERENCE_DYNDB_TABLE,
    #         IndexName='status-task_arn-index',
    #     )

    #     results = []
    #     for page in pager:
    #         for i in page['Items']:
    #             r = util.flatten_dyndb_item(i)

    #             if r['status'] != 'stopped':
    #                 item = self.refresh(r['user_id'], r['deployment_id'])
    #                 results.append(item)

    #                 if item['status'] != r['status']:
    #                     logger.info('Deployment %s: %s -> %s' % (
    #                         item['deployment_id'],
    #                         r['status'],
    #                         item['status']
    #                     ))

    #     return results

    def all(self, user):
        dyn = boto3.client('dynamodb')
        resp = dyn.query(
            TableName=config.INFERENCE_DYNDB_TABLE,
            KeyConditions={
                'user_id': {
                    'AttributeValueList': [{'S': user}],
                    'ComparisonOperator': 'EQ'
                }
            }
        )

        result = []
        for i in resp['Items']:
            result.append(util.flatten_dyndb_item(i))

        return result

    def launch(self, user, deployment_name=""):
        did = util.random_char()  # TODO: conflict
        dyn = boto3.client('dynamodb')
        ecs = boto3.client('ecs')

        # TODO: detect when we reach max capacity
        if config.INFERENCE_ECS_MAX:
            pass

        user = str(user)

        if not deployment_name:
            deployment_name = "deployment-" + did
        else:
            deployment_name = str(deployment_name)

        task_arn = None

        try:
            result = self._start(user, did, {
                'deployment_name': deployment_name,
            })
            task_arn = result['tasks'][0]['taskArn']
            version_arn = result['tasks'][0]['taskDefinitionArn']

            dyn.put_item(
                TableName=config.INFERENCE_DYNDB_TABLE,
                Item={
                    'user_id': { 'S': user, },
                    'deployment_id': { 'S': did, },
                    'deployment_name': { 'S': deployment_name },
                    'task_arn': { 'S': task_arn, },
                    'origin_task_arn': { 'S': task_arn, },
                    'version_arn': { 'S': version_arn },
                    'status': { 'S': 'starting' },
                    'desired_status': { 'S': 'running' },
                    'public_endpoint': { 'S': f'{config.INFERENCE_BASE_URL}/{did}/' },
                }
            )
        except:
            if task_arn is not None:
                ecs.stop_task(
                    cluster=config.ECS_CLUSTER,
                    task=task_arn,
                    reason='Launch failure',
                )

        return did

    def get(self, user, did, refresh=False):
        if refresh:
            return self.refresh(user, did)

        return self._get_item(user, did, True)

    def refresh(self, user, did):
        """
        Refresh the status of a deployment and return the updated instance
        """
        ecs = boto3.client('ecs')
        ec2 = boto3.client('ec2')

        item = self._get_item(user, did, True)

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
                        if task['containers'][i]['name'] == 'inference':
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
                    logger.warn(f'Status is out of sync for deployment {did}. Removing container info')
                    update['task_arn'] = None

                update['status'] = ecs_status
            else:
                logger.warn(f"Found invalid task arn {item['task_arn']} for Deployment {did}")
                update = {
                    'status': 'stopped',
                    'task_arn': None,
                    'private_endpoint': None,
                }
        else:
            update = {'status': 'stopped'}
        
        if 'private_endpoint' in update and update['private_endpoint'] != item.get('private_endpoint'):
            # TODO: the gateway should be able to pull this by itself
            self._gw.setup('deployment', did, update['private_endpoint'])

            if config.INFERENCE_VERIFY_ENDPOINT == 'public' and 'public_endpoint' in item:
                try:
                    check = requests.head(item['public_endpoint'])
                    if check.status_code >= 400:
                        logger.warn(f"Deployment {did} container status is running but endpoint return {check.status_code}")
                        update = {'status': 'pending'}
                    else:
                        logger.info(f'Deployment {did} is ready, status: {check.status_code}')

                        # XXX: still need to give it sometime to be ready
                        # best case is probably to have Deployment ping us back when it is ready
                except:
                    logger.warn('Unable to verify endpoint ' + item['public_endpoint'])
                    update = {'status': 'pending'}

        if update:
            self._update_item(user, did, update)

        item.update(update)
        return item

    def start(self, user, did):
        """
        Start a stopped deployment
        """
        ecs = boto3.client('ecs')
        
        item = self._get_item(user, did, True)
        task_arn = None

        if 'task_arn' not in item:
            try:
                result = self._start(user, did, item)
                task_arn = result['tasks'][0]['taskArn']
                version_arn = result['tasks'][0]['taskDefinitionArn']

                self._update_item(user, did, {
                    'task_arn': task_arn,
                    'version_arn': version_arn,
                    'status': 'starting',
                    'desired_status': 'running',
                    'origin_task_arn': task_arn,
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
            self.refresh(user, did)

    def stop(self, user, did):
        """
        Stop a deployment
        """
        ecs = boto3.client('ecs')

        item = self._get_item(user, did)

        if 'task_arn' in item:
            ecs.stop_task(
                cluster=config.ECS_CLUSTER,
                task=item['task_arn']['S'],
                reason='Request by user'
            )

        self._update_item(user, did, {
            'task_arn': None,
            'private_endpoint': None,
            'status': 'stopped',
            'desired_status': 'stopped',
        })

        self._gw.destroy('deployment', did)

    def destroy(self, user, did):
        """
        Destroy a deployment, all data will be lost
        """
        self.stop(user, did)
        dyn = boto3.client('dynamodb')
        dyn.delete_item(
            TableName=config.INFERENCE_DYNDB_TABLE,
            Key=self._item_key(user, did)
        )

    def _start(self, user, did, item=None):
        ecs = boto3.client('ecs')
        item = item or {}

        deployment_path = "/home/project"

        # TODO: save on s3
        envvar = [
            {'name': 'DEPLOYMENT_ID', 'value': str(did)},
            {'name': 'WORKSPACE_PATH', 'value': deployment_path},
            {'name': 'H1ST_MODEL_REPO_PATH', 'value': f"${deployment_path}/.models"},
            {'name': 'PYTHONPATH', 'value': deployment_path},
        ]

        if 'deployment_name' in item:
            envvar.append({'name': 'DEPLOYMENT_NAME', 'value': str(item['deployment_name'])})

        # override the command of the container
        ws_cmd = [
            "bash", "-c",
            f"set -ex && mkdir -p /efs/data/ws-{did} && rm -rf {deployment_path} && ln -s /efs/data/ws-{did} {deployment_path} && " + config.INFERENCE_BOOT_COMMAND,
        ]

        result = ecs.run_task(
            cluster=config.ECS_CLUSTER,
            taskDefinition=config.INFERENCE_ECS_TASK_DEFINITION,
            overrides={
                'containerOverrides': [
                    {
                        'name': 'inference',
                        'environment': envvar,
                        'cpu': config.INFERENCE_DEFAULT_CPU,
                        'memory': config.INFERENCE_DEFAULT_RAM,
                        "command": ws_cmd,
                    }
                ]
            },
            tags=[
                {'key': 'Project', 'value': 'H1st'},
                {'key': 'Deployment ID', 'value': did},
                {'key': 'User ID', 'value': user},
            ]
        )

        return result

    def _item_key(self, user, did):
        return {
            'user_id': {'S': user},
            'deployment_id': {'S': did},
        }

    def _get_item(self, user, did, flatten=False):
        dyn = boto3.client('dynamodb')
        item = dyn.get_item(
            TableName=config.INFERENCE_DYNDB_TABLE,
            Key={
                'user_id': {'S': user},
                'deployment_id': {'S': did},
            }).get('Item')

        if not item:
            raise RuntimeError("Deployment is not valid")

        if flatten:
            item = util.flatten_dyndb_item(item)

        return item

    def _update_item(self, user, did, data):
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
            TableName=config.INFERENCE_DYNDB_TABLE,
            Key=self._item_key(user, did), 
            AttributeUpdates=updates
        )
