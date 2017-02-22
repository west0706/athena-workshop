#!/bin/bash

if [ $# -eq 0 ]; then
    echo "USAGE: emr-setup.sh student-name"
    exit 1
fi

student=$1

echo Setting up EMR cluster for student $student

aws emr create-cluster --name emr-$student \
    --applications Name=Hadoop Name=Hive Name=Pig Name=Hue Name=Spark Name=Presto \
    --ec2-attributes '{"KeyName":"'$student'","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-10477259","EmrManagedSlaveSecurityGroup":"sg-1ffc5363","EmrManagedMasterSecurityGroup":"sg-23fc535f"}' \
    --service-role EMR_DefaultRole --enable-debugging --release-label emr-5.3.1 --region us-east-1 \
    --log-uri 's3n://dahouse-emr-logs/$student/' \
    --instance-groups '[{"InstanceCount":2,"InstanceGroupType":"CORE","InstanceType":"m3.xlarge","Name":"Core - 2"},{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m3.xlarge","Name":"Master - 1"}]' \
