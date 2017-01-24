#Lab 2 - Interacting with AWS Athena#

*During this lab, you will create a new database using the AWS Management Console, create a new table and run your first query. Then you will connect to your table using MySQLWorkbench as well as AWS QuickSight*

**Create a Database and the Table**
 - Open AWS console at https://console.aws.amazon.com/athena/
 - In the query edit box, type ```CREATE DATABASE IF NOT EXISTS your_name``` and click ```Run Query```
 - Enter the following DDL query into the query window and click ```Run Query```
 
 ```
CREATE EXTERNAL TABLE IF NOT EXISTS `vadim@doit-intl.com`.yellow_trips_csv(
         pickup_timestamp BIGINT,
         dropoff_timestamp BIGINT,
         vendor_id STRING,
         pickup_datetime TIMESTAMP,
         dropoff_datetime TIMESTAMP,
         pickup_longitude FLOAT,
         pickup_latitude FLOAT,
         dropoff_longitude FLOAT,
         dropoff_latitude FLOAT,
         rate_code STRING,
         passenger_count INT,
         trip_distance FLOAT,
         payment_type STRING,
         fare_amount FLOAT,
         extra FLOAT,
         mta_tax FLOAT,
         imp_surcharge FLOAT,
         tip_amount FLOAT,
         tolls_amount FLOAT,
         total_amount FLOAT,
         store_and_fwd_flag STRING)
         ROW FORMAT DELIMITED
         FIELDS TERMINATED BY ',' 
         LOCATION 's3://nyc-yellow-trips/csv/'
```
 - Paste the following query into your query box, click ```Format Query``` and then ```Click Query```. Note the runtime of the query and amount of data scanned. 

 ```
SELECT from_unixtime(yellow_trips_csv.pickup_timestamp) as pickup_date, from_unixtime(yellow_trips_csv.dropoff_timestamp) as dropoff_date ,* FROM <USER_NAME>.yellow_trips_csv limit 100
```
**Interact with AWS Athena using JDBC Driver**
 - Make sure you have AWS CLI tool is installed - if not please install using the instructions [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
 - Make sure you have SQL Workbench installed  if not please install using the instructions [here](http://www.sql-workbench.net/downloads.html)
 - Download the JDBC driver into the SQL Workbench directory from this [link](https://s3.amazonaws.com/athena-downloads/drivers/AthenaJDBC41-1.0.0.jar)
 - Start SQL Workbench
 - Click ‘Manage Drivers’, create a new driver with the following settings
  - Name: Athena
  - Library: <Add the path to the Athena JDBC downloaded in the previous step>
  - Classname: com.amazonaws.athena.jdbc.AthenaDriver
  - Sample URL: jdbc:awsathena://athena.us-east-1.amazonaws.com:443
  - Press OK
  
 - Create a new connection with the following settings
  - Name: Athena
  - Driver: Athena
  - URL: jdbc:awsathena://athena.us-east-1.amazonaws.com:443
  - Username: <Your Access Key>
  - Password: <Your Secret Key>
  - Extended Properties:
  - Key: s3_staging_dir
  - Value: s3://<Staging Bucket Name>/
  - Click OK
- Run the following query in the SQL Workbench query window

```
SELECT from_unixtime(yellow_trips_csv.pickup_timestamp) as pickup_date, 
       from_unixtime(yellow_trips_csv.dropoff_timestamp) as dropoff_date , * 
FROM <USER_NAME>.yellow_trips_csv limit 100
```



