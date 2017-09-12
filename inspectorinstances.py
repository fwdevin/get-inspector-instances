# This script prints instance IDs of instances that have
# had Inspector assessments run against them.
#
# 2017 Devin S.

#!/usr/local/bin/python3

import boto3
from botocore.exceptions import EndpointConnectionError

ec2 = boto3.client('ec2')

regions_list = ec2.describe_regions()

regions = regions_list['Regions']

agents_list = []
instances_list = []

print('Checking all regions for assessments...\n')

for region in regions:
	try:
		x = region['RegionName']
		client = boto3.client('inspector', region_name=x)
		
		# Try getting a list of assessment runs from the region
		runs = client.list_assessment_runs()
	except EndpointConnectionError as e:
		print('Error: %s, this region may not currently be supported by Inspector.\n' % (e))
		continue
	
	runs = runs['assessmentRunArns']
	
	for run in runs:
		agents_list.append(client.list_assessment_run_agents(assessmentRunArn=run))
	
	# Get the instance IDs of the instances in the assessment runs
	for agent in agents_list:
		x = agent['assessmentRunAgents']
		for a in x:
			instances_list.append(a['agentId'])

print('These instances have had assessments run against them:\n' + str(list(set(instances_list))) + '\n')
