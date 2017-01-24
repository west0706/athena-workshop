**Lab 2 - Interacting with AWS Athena**

*During this lab, you will create a new database using the AWS Management Console, create a new table and run your first query. Then you will connect to your table using MySQLWorkbench as well as AWS QuickSight*

Create a Database and the Table
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
