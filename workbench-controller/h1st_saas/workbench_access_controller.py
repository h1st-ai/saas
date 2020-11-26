import boto3
import datetime

from h1st_saas import config
from .workbench_controller import WorkbenchController


class WorkbenchAccessController:
    DEFAULT_PERMISSION = 'read-write'

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

    def list_workbenches(self, user_id):
        """
        List all workbenches access by a user
        """
        wbs = self.wc.list_workbenches(user_id)
        shares = self.list_shares(user_id=user_id)

        if shares:
            wbs += self.wc.get_multi([
                {'user_id': s['owner_id'], 'workbench_id': s['workbench_id']} for s in shares
            ])

        return sorted(wbs, key=lambda x: x.get('created_at', ''))

    def add_shares(self, shares):
        for s in shares:
            if not s.get('permission'):
                self.share(s['workbench_id'], s['user_id'], s.get('permission'))
            else:
                self.unshare(s['workbench_id'], s['user_id'])

    def list_shares(self, workbench_id=None, user_id=None):
        if not workbench_id and not user_id:
            raise Exception('You have to specify user id or workbench id')

        dyn = boto3.client('dynamodb')

        if workbench_id:
            pager = dyn.get_paginator('query').paginate(
                TableName=self.sharing_table,
                IndexName='workbench-index',
                KeyConditions={
                    'workbench_id': {
                        'AttributeValueList': [{'S': workbench_id}],
                        'ComparisonOperator': 'EQ'
                    }
                }
            )
        elif user_id:
            pager = dyn.get_paginator('query').paginate(
                TableName=self.sharing_table,
                KeyConditions={
                    'user_id': {
                        'AttributeValueList': [{'S': user_id}],
                        'ComparisonOperator': 'EQ'
                    }
                }
            )

        items = []
        for page in pager:
            for item in page['Items']:
                items.append({
                    'user_id': item['user_id']['S'],
                    'workbench_id': item['workbench_id']['S'],
                    'owner_id': item['owner_id']['S'],
                    'permission': item['permission']['S'],
                })

        return items

    def share(self, workbench_id, user_id, permission=None):
        """
        Share a workbecnh with another user
        """
        wb = self.wc.get_by_wid(workbench_id)

        if wb['user_id'] == user_id:
            raise Exception('Can not share to yourself')

        dyn = boto3.client('dynamodb')
        dyn.put_item(
            TableName=self.sharing_table,
            Item={
                'workbench_id': {'S': workbench_id},
                'user_id': {'S': user_id},
                'owner_id': {'S': wb['user_id']},
                'permission': {'S': permission or self.DEFAULT_PERMISSION},
                'created_at': {'S': str(datetime.datetime.utcnow())},
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

        pager = dyn.get_paginator('query').paginate(
            TableName=self.sharing_table,
            IndexName='workbench-index',
            KeyConditions={
                'workbench_id': {
                    'AttributeValueList': [{'S': workbench_id}],
                    'ComparisonOperator': 'EQ'
                }
            }
        )

        to_delete = []
        for page in pager:
            for item in page['Items']:
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
