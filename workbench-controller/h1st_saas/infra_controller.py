import boto3
import ulid
import logging
import time
import requests
import h1st_saas.config as config
import h1st_saas.util as util


logger = logging.getLogger(__name__)

class InfraController:
    """
    This class provides function to manage the underlying ECS infrastructure
    and perform common tasks such as draining or reallocating instances
    """

    def __init__(self):
        pass

    def determine_provider(self, cpu, ram):
        # XXX it's super complicated to automatically determine which provider can
        # provide the request unit, so we make a shortcut and hard code the provider here

        capacity = {
            'H1st-staging': [
                {
                    'max_cpu': 8192,  # 8192
                    'max_ram': 15000, # 15577
                    'instance_type': 'c5.2xlarge',
                    'name': 'h1st-staging',
                },
                {
                    'max_cpu': 73728, # 73728
                    'max_ram': 140000, # 140770
                    'instance_type': 'c5.18xlarge',
                    'name': 'h1st-staging-large'
                },
            ],
            'H1st': [
                {
                    'max_cpu': 8192,  # 8192
                    'max_ram': 15000, # 15577
                    'instance_type': 'c5.2xlarge',
                    'name': 'h1st',
                }
            ]
        }

        providers = capacity[config.ECS_CLUSTER]
        for cap in providers:
            if cap['max_ram'] >= ram and cap['max_cpu'] >= cpu:
                return cap['name'], cap['instance_type']

        raise Exception(f'Unable to satisfy requested resource: cpu: {cpu} ram: {ram}')

    def list_instances(self):
        ecs = boto3.client('ecs')
        paginator = ecs.get_paginator('list_container_instances')

        arns = []
        for page in paginator.paginate(cluster=config.ECS_CLUSTER):
            for arn in page['containerInstanceArns']:
                arns.append(arn)

        result = {}
        for i in range(0, len(arns), 50):
            resp = ecs.describe_container_instances(
                cluster=config.ECS_CLUSTER,
                containerInstances=arns[i:i+50]
            )

            for instance in resp['containerInstances']:
                instance['id'] = instance['ec2InstanceId']
                instance['resources'] = self._get_resources(instance)

                del instance['attributes']
                del instance['remainingResources']
                del instance['registeredResources']

                result[instance['id']] = instance

        return result

    def list_providers(self):
        # TODO: cache this
        ecs = boto3.client('ecs')
        asg = boto3.client('autoscaling')

        resp = ecs.describe_clusters(clusters=[config.ECS_CLUSTER])
        providers = list(filter(lambda x: 'FARGATE' not in x, resp['clusters'][0]['capacityProviders']))

        result = {}
        if len(providers):
            resp = ecs.describe_capacity_providers(capacityProviders=providers)
            providers = resp['capacityProviders']

            for provider in providers:
                asgArn = provider['autoScalingGroupProvider']['autoScalingGroupArn']
                group = asg.describe_auto_scaling_groups(
                    AutoScalingGroupNames=[asgArn.split('/')[-1]]
                )['AutoScalingGroups'][0]

                launch_config = asg.describe_launch_configurations(
                    LaunchConfigurationNames=[group['LaunchConfigurationName']]
                )['LaunchConfigurations'][0]

                result[provider['name']] = {
                    'name': provider['name'],
                    'auto_scaling_group': {
                        'name': group['AutoScalingGroupName'],
                        'instance_type': launch_config['InstanceType'],
                        'desired_size': group['DesiredCapacity'],
                        'min_size': group['MinSize'],
                        'max_size': group['MaxSize'],
                    },
                    'instances': group['Instances'],
                }

        return result

    def start_instance(self, instance_id):
        # TODO: make sure this is managed by us
        ec2 = boto3.client('ec2')
        ec2.start_instances(
            InstanceIds=[instance_id]
        )

    def stop_instance(self, instance_id):
        # TODO: make sure this is managed by us
        ec2 = boto3.client('ec2')
        ec2.stop_instances(
            InstanceIds=[instance_id]
        )

    def drain_instance(self, instance_id):
        # mark as drain in ecs
        ecs = boto3.client('ecs')
        instances = self.list_instances()

        for instance in instances.values():
            if instance['ec2InstanceId'] == instance_id:
                ecs.update_container_instances_state(
                    cluster=config.ECS_CLUSTER,
                    containerInstances=[instance['containerInstanceArn']],
                    status='DRAINING',
                )
                return True

        # TODO: 
        # stop all containers
        # detach from autoscaling group
        # delete

        return False

    def _get_resources(self, instance):
        resources = {}

        # merge resoruce value
        for res in instance['remainingResources']:
            if res['name'] == 'CPU':
                resources['CPU'] = {
                    'available': res['integerValue']
                }
            elif res['name'] == 'MEMORY':
                resources['MEMORY'] = {
                    'available': res['integerValue']
                }

        for res in instance['registeredResources']:
            if res['name'] == 'CPU':
                resources['CPU']['total'] = res['integerValue']
            elif res['name'] == 'MEMORY':
                resources['MEMORY']['total'] = res['integerValue']

        return resources