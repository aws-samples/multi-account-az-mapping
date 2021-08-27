## Mutli-Account Availability Zone (AZ) mapping

AWS independently maps Availability Zone names for each individual account. This means that for example an AZ named us-east-1a in one account might not be the same location as us-east-1a in another AWS account. 

Multi-account organizations may have a requirement to ensure a consistent AZ mapping for all of their subnets in their VPCs across their accounts. This solution can deploy resources in each of your accounts to aide in ensuring the same Availability Zone IDs are used when creating subnets, and not relying on the AZ name.

### How it works
The `az-mapping.yaml` deploys a set of Systems Manager Parameter Store values storing the Availabilty Zone Id and Availability Zone Name. These values are then used when VPCs are created to ensure a consistent mapping to Zone Name from a set of given Zone Ids in each account.

1. Determine the Availability Zone Ids for the AZs you want to use.
2. Use the az-mapping.yaml to create a stack in all relevant accounts. (Customizations for Control Tower Solution, CloudFormation StackSets, etc.)
   * Specify the Zone Ids parameter value, comma separated, and in an ordered format.
3. Update your infrastructure as code that creates your VPC to reference the SSM Parameter Store values to get the AZ Name for each subnet.
4. Create VPCs in your relevant accounts using your infrastructure as code.

See `vpc-example.yaml` for a working CloudFormation example which creates a VPC using the SSM Parameter Store values for the AZ Names.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

