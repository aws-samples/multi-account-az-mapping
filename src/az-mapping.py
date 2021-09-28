# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import boto3
import cfnresponse

def lambda_handler(event, context):
    azIds = event['ResourceProperties']['azIds']

    if event['RequestType'] == 'Create':
        create(azIds)
    elif event['RequestType'] == 'Delete':
        delete(azIds)
    elif event['RequestType'] == 'Update':
        delete(azIds)
        create(azIds)
    else:
        print('no changes')

    response_data = {}
    cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    

# Use the ordered parameter list of azIds (zone ids) to create SSM Parameters 
# for the AZ Mapping. Store the resulting zone name mapping along with the zone-id
def create(azIds):
    ssm = boto3.client('ssm')
    
    azs = getAZs(azIds)
    for az in azs:
        azId = az.get('ZoneId')
        azName = az.get('ZoneName')
        # AZ Number should match the ordered zone id parameter
        azNumber = azIds.index(azId) + 1
        ssm.put_parameter(
            Name='/az-mapping/az' + str(azNumber), 
            Description=azId,
            Value=azName,
            Type='String',
            Overwrite=True,
            Tier='Standard')

# Delete the az mapping parameters
def delete(azIds):
    ssm = boto3.client('ssm')
    
    azNumber=1
    azs = getAZs(azIds)
    for az in azs:
        ssm.delete_parameter(
            Name='/az-mapping/az' + str(azNumber)
            )
        azNumber = azNumber + 1

# Get the AZ objects that match the given zone IDs
def getAZs(azIds):
    ec2c = boto3.client('ec2')
    r = ec2c.describe_availability_zones(
            ZoneIds=azIds
        )
    azs = r.get('AvailabilityZones')
    return azs