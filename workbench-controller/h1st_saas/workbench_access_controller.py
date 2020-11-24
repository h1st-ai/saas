import boto3

from h1st_saas import config
from .workbench_controller import WorkbenchController


class WorkbenchAccessController:
    """
    Main class to manage the access to workbench
    """
    def __init__(self):
        # XXX: just use a better prefix later
        # get the sharing table from the primary table
        is_staging = "_staging" in config.DYNDB_TABLE

        self.sharing_table = config.DYNDB_TABLE.replace("_staging", "") + "_sharing"
        if is_staging:
            self.sharing_table += "_staging"

        self.wc = WorkbenchController()

    def list_workbench(user_id):
        """
        List all workbenches access by a user
        """
        pass

    def share(self, workbench_id, user_id, permission=None):
        """
        Share a workbecnh with another user
        """
        dyn = boto3.client('dynamodb')
        dyn.put_item(
            TableName=self.sharing_table,
            Item={
                'workbench_id': {'S': workbench_id},
                'user_id': {'S': user_id},
                'permission': {'S': permission or ""}
            }
        )

    def unshare(self, workbench_id, user_id):
        """
        Unshare the workbench
        """
        dyn = boto3.client('dynamodb')
        dyn.delete_item(
            TableName=self.sharing_table,
            Key={
                'workbench_id': {'S': workbench_id},
                'user_id': {'S': user_id},
            }
        )

    def cleanup(self, workbench_id):
        """
        Delete share item by workbench id
        """
        dyn = boto3.client('dynamodb')

        pager = dyn.get_paginator('scan').paginate(
            TableName=self.sharing_table,
        )

        to_delete = []
        for page in pager:
            for item in page['Items']:
                if item['workbench_id']['S'] == workbench_id:
                    to_delete.append((workbench_id, item['user_id']['S']))

        for i in range(0, len(to_delete), 10):
            items = to_delete[i:i+10]

            dyn.batch_write_item(
                RequestItems={
                    self.sharing_table: [
                        {
                            'DeleteRequest': {
                                'Key': {
                                    'workbench_id': {'S': item[0]},
                                    'user_id': {'S': item[1]},
                                }
                            }
                        }
                        for item in items
                    ]
                }
            )
