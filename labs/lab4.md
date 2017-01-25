#Lab 4 - Partitioning Data#
*During this lab you will learn how to create and query partitioned tables.*

**Create a Spark EMR cluster**
- Follow the instructions [at this link](http://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-access-ssh.html) to create the SSH key you will require later

- Open EMR console [at this link](https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1)
- Click Create Cluster
- Set the cluster name to `<USERNAME>_spark`
- Select `Spark` in the `Applications` section
- Set the instance type to `c4.large`
- Select the EC2 Key Pair you created in the previous step.
- Click Create Cluster
- While the cluster is being provisioned and started continue to the next step.

**Create an S3 bucket**
- In a new browser window/tab open S3 console with this link

- Click Create Bucket
- Enter your username as the Bucket Name
- Select ‘US Standard’ as the Region
- Click Create
- Close the S3 browser window/tab.
- Wait while the cluster is being provisioned and running. (Approx. 5-10 minutes)

**Connect to your EMR cluster master**

- When the EMR cluster is ready click the SSH link to the left of the Master public DNS.

- Follow the instructions to SSH into the master instance.

- Once connected run the command `screen` at the prompt

**Create a partitioning batch job**
