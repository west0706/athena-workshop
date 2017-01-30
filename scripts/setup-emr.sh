#!/bin/bash

f [ $# -ne 1 ]
then
echo "USAGE: emr-setup.sh student-name"
return
fi

student=$1

echo Setting up EMR cluster for student $student

aws emr create-cluster --name emr-$student --auto-scaling-role EMR_AutoScaling_DefaultRole --applications \
    Name=Hadoop Name=Hive Name=Pig Name=Hue Name=Spark Name=Presto \
    --ec2-attributes '{"KeyName":"vadim_dahouse","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-10477259","EmrManagedSlaveSecurityGroup":"sg-1ffc5363","EmrManagedMasterSecurityGroup":"sg-23fc535f"}' \
    --service-role EMR_DefaultRole --enable-debugging --release-label emr-5.3.0 \
    --log-uri 's3n://dahouse-emr-logs/$student/' \
    --instance-groups '[{"InstanceCount":2,"InstanceGroupType":"CORE","InstanceType":"m3.xlarge","Name":"Core - 2"},{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m3.xlarge","Name":"Master - 1"}]' \
    --scale-down-behavior TERMINATE_AT_INSTANCE_HOUR --region us-east-1
