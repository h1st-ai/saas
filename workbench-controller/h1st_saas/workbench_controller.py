import boto3
import ulid
import h1st_saas.config as config
import h1st_saas.util as util


class WorkbenchController:
    def list_workbench(self):
        pass

    def launch(self):
        wid = util.random_char()
        dyn = boto3.client('dynamodb')
        ecs = boto3.client('ecs')

        owner = 'bao'
        task_arn = None

        try:
            result = ecs.run_task(
                cluster=config.ECS_CLUSTER,
                taskDefinition=config.ECS_TASK_DEFINITION,
                overrides={
                    'containerOverrides': [
                        {
                            'name': 'workbench',
                            'environment': [
                                {'name': 'WB_USER', 'value': owner},
                                {'name': 'WB_ID', 'value': wid}
                            ],
                            'cpu': 1024,
                            'memory': 2048,
                        }
                    ]
                },
                tags=[
                    {'key': 'Project', 'value': 'H1st'},
                    {'key': 'Workbench ID', 'value': wid},
                ]
            )

            task_arn = result['tasks'][0]['taskArn']

            dyn.put_item(
                TableName=config.DYNDB_TABLE,
                Item={
                    'user_id': {
                        'S': owner,
                    },
                    'workbench_id': {
                        'S': wid,
                    },
                    'task_arn': {
                        'S': task_arn,
                    },
                    'status': {
                        'S': 'new'
                    }
                }
            )
        except:
            if task_arn is not None:
                ecs.stop_task(
                    cluster=config.ECS_CLUSTER,
                    task=task_arn,
                    reason='Launch failure',
                )

        return wid

    def start(self, wid):
        """
        Start a stopped workbench
        """
        pass

    def stop(self, wid):
        """
        Stop a workbench
        """
        # ecs.stop_task(
        #     cluster=config.ECS_CLUSTER,
        #     task='arn:aws:ecs:us-west-1:394497726199:task/H1st/1d7dc305fc5d4a2e900bec4d0661f15c',
        #     reason='Request by user'
        # )

        return

    def destroy(self, wid):
        """
        Destroy a workbench, all data will be lost
        """
        # TODO: stop & delete in dynamodb
        self.stop(wid)
