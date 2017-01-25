#Lab 3 - Supported Formats and SerDes#
*During this lab you will explore ways to define external tables using various file formats.*

**Create External Table from Parquet files**
- Open AWS console at [https://console.aws.amazon.com/athena/](https://console.aws.amazon.com/athena/)

- Enter the following DDL query into the query window
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*
```
CREATE EXTERNAL TABLE IF NOT EXISTS <USER_NAME>.yellow_trips_parquet(
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
         store_and_fwd_flag STRING
) STORED AS PARQUET LOCATION 's3://nyc-yellow-trips/parquet/';
```

**Create External Table from ORC files**
- Enter the following DDL query into the query window
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*

```
CREATE EXTERNAL TABLE IF NOT EXISTS <USER_NAME>.yellow_trips_orc(
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
         store_and_fwd_flag STRING
) STORED AS ORC LOCATION 's3://nyc-yellow-trips/orc/';
```

**Compare the query performance**
- Run the following queries one by one and compare the performance while noting the amount of scanned data.
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*

```
SELECT COUNT(*) FROM <USER_NAME>.yellow_trips_csv;
SELECT COUNT(*) FROM <USER_NAME>.yellow_trips_parquet;
SELECT COUNT(*) FROM <USER_NAME>.yellow_trips_orc;
```

```
SELECT max(passenger_count) FROM <USER_NAME>.yellow_trips_csv WHERE vendor_id <> 'VTS';
SELECT max(passenger_count) FROM <USER_NAME>.yellow_trips_parquet WHERE vendor_id <> 'VTS';
SELECT max(passenger_count) FROM <USER_NAME>.yellow_trips_orc WHERE vendor_id <> 'VTS';
```

**Create External Table from text files with custom format**
- Run the following DDL query
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*

```
CREATE EXTERNAL TABLE IF NOT EXISTS <USER NAME>.elb_logs_raw_native (
         request_timestamp string,
         elb_name string,
         request_ip string,
         request_port int,
         backend_ip string,
         backend_port int,
         request_processing_time double,
         backend_processing_time double,
         client_response_time double,
         elb_response_code string,
         backend_response_code string,
         received_bytes bigint,
         sent_bytes bigint,
         request_verb string,
         url string,
         protocol string,
         user_agent string,
         ssl_cipher string,
         ssl_protocol string 
) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
         'serialization.format' = '1','input.regex' = '([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*):([0-9]*) ([.0-9]*) ([.0-9]*) ([.0-9]*) (-|[0-9]*) (-|[0-9]*) ([-0-9]*) ([-0-9]*) \\\"([^ ]*) ([^ ]*) (- |[^ ]*)\\\" (\"[^\"]*\") ([A-Z0-9-]+) ([A-Za-z0-9.-]*)$' )
LOCATION 's3://athena-examples/elb/raw/';
```

- When finished run the following query

```
SELECT * FROM <USERNAME>.elb_logs_raw_native WHERE elb_response_code <> '200' LIMIT 100;
```

**Create External Table from results of previous queries**
- Click the ‘Settings’ button at the top right.
- Note the URL from the ‘Query results location’ text box and find the bucket in the S3
- Run the following query
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*

```
SELECT * 
FROM <USER NAME>.yellow_trips_csv 
limit 10000;
```

- Look for the results of the query within the S3 bucket. (path should be similar to .../Unsaved/2017/01/24/aa9...fbb.csv)

- You can copy the results into any S3 bucket for re-use or use from this location.
- Run the DDL query below after replacing `<RESULTS PATH>` with this path  
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*
```
CREATE EXTERNAL TABLE IF NOT EXISTS <USER NAME>.yellow_trips_csv_query-result(
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
         store_and_fwd_flag STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION '<RESULTS PATH>';
```

- Run the following query on the results table
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. srfrnk_doit)*
```
select count(*) from <USER NAME>.yellow_trips_csv_query-result
```

**You have sucessully completed Lab 3 :-)**
