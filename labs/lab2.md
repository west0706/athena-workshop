#Lab 2 - Interacting with AWS Athena#

*During this lab, you will create a new database using the AWS Management Console, create a new table and run your first query. Then you will connect to your table using MySQLWorkbench as well as visualize the data using AWS QuickSight*

**^^^Please make sure your AWS Management Console is set on US-East Region (N.Virginia)^^^**

![alt tag](https://github.com/doitintl/athena-workshop/blob/master/images/region.png)

**Examine S3 bucket content**
- Open [AWS Management Console Console](https://dahouse.signin.aws.amazon.com/console) and navigate to S3

- Locate the ```nyc-yellow-trips``` bucket and navigate to ```csv``` folder. Note the amount of files and the format by downloading [sample file](https://s3.amazonaws.com/nyc-yellow-trips/csv/trips999999999999.csv)

**Create S3 bucket**
- Open [AWS Management Console Console](https://dahouse.signin.aws.amazon.com/console) and navigate to S3

- Click 'Create Bucket'
- Enter 'Bucket Name' - e.g. <USER_NAME>-athena
- Choose Region 'US Standard'
- Click 'Create'

**Create a Database and the Table**
- Open [AWS Management Console Console](https://dahouse.signin.aws.amazon.com/console)

- First, you will be creating a **database**. In the query edit box, type the following query and click ```Run Query```
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. shaharf)*
 
 ```
 CREATE DATABASE IF NOT EXISTS <USER_NAME>
 ```
- Now, you will create an **external table based on CSV files** by copying the following DDL query into the query window and click ```Run Query```
 
 ```
CREATE EXTERNAL TABLE IF NOT EXISTS <USER_NAME>.yellow_trips_csv(
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
- Navigate to Athena Catalog Manager and explore the database and table you've created

- Finally, you are ready to run your first Athena query! Paste the following query into your query box, click ```Format Query``` and then ```Click Run Query```. Note the runtime of the query and amount of data scanned. 

 ```
SELECT from_unixtime(yellow_trips_csv.pickup_timestamp) as pickup_date, from_unixtime(yellow_trips_csv.dropoff_timestamp) as dropoff_date ,* FROM <USER_NAME>.yellow_trips_csv limit 100
```

**Interact with AWS Athena using JDBC Driver**
- Make sure you have AWS CLI tool is installed - if not please install using the instructions [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

- Make sure you have SQL Workbench installed  if not please install using the instructions [here](http://www.sql-workbench.net/downloads.html)
- Download the JDBC driver into the SQL Workbench directory from this [link](https://s3.amazonaws.com/athena-downloads/drivers/AthenaJDBC41-1.0.0.jar)
- Start SQL Workbench
- Click ```Manage Drivers```, create a new driver with the following settings
- Name: Athena
- Library: Select Athena JDBC Driver JAR (downloaded in the previous step)
- Classname: com.amazonaws.athena.jdbc.AthenaDriver
- Sample URL: jdbc:awsathena://athena.us-east-1.amazonaws.com:443
- Press OK
- Create a new connection with the following settings
- Name: Athena
- Driver: Athena
- URL: jdbc:awsathena://athena.us-east-1.amazonaws.com:443
- Username: ```Your Access Key``` (it is provided in the email we sent you earlier with your IAM user details)
- Password: ```Your Secret Key``` (it is provided in the email we sent you earlier with your IAM user details)
- Extended Properties:
- Key: s3_staging_dir
- Value: ```s3://<USER_NAME>-jdbc-staging/```
- Click OK
- Run the following query in the SQL Workbench query window

```
SELECT from_unixtime(yellow_trips_csv.pickup_timestamp) as pickup_date, 
       from_unixtime(yellow_trips_csv.dropoff_timestamp) as dropoff_date , * 
FROM <USER_NAME>.yellow_trips_csv limit 100
```

**Interact with AWS Athena using AWS QuickSight**

- Open QuickSight from [here](https://us-east-1.quicksight.aws.amazon.com)

- Click Manage Data
- Click New Data Set
- Select Athena as your data source
- Enter the name ```<USER_NAME>-yellow-trips-csv``` and click ```Create Data Source```
- Select the database with your username , the table ```yellow_trips_csv``` and then click ```Edit/Preview Data```
- Open the 'Tables' panel and click 'Switch to custom SQL tool'
- Enter any name for the Query and copy the following SQL into the 'Custom SQL' text box
```
SELECT *, 
    greatest(0,trip_distance*3600.0/(dropoff_timestamp-pickup_timestamp)) as avg_speed,
    hour(from_unixtime(pickup_timestamp)) as hour
FROM <USER_NAME>.yellow_trips_csv
WHERE pickup_timestamp is not null and pickup_timestamp is not null and pickup_timestamp<>dropoff_timestamp
```
- Click 'Finish'
- Click ```Save & Visualize```
- Select ```Vertical Bar Chart``` from the ```Visual Types``` Panel
- Drag ```hour``` into ‘X axis’ box
- Drag ```avg_speed``` into ‘Value’ box, then click the down arrow of the box and select ```Average``` under the  ```Aggregate```
 
**Interact with Athena from a NodeJS application using JDBC**
- Open AWS console at [https://console.aws.amazon.com/athena/](https://console.aws.amazon.com/athena/)

- Enter the following DDL query into the query window
- *Remember to replace `<USER_NAME>` with your AWS username. (e.g. shaharf)*
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

- Make sure you have Python 2.7, NodeJS and NPM installed on your machine. If not install from [here](https://nodejs.org/en/download/) and [here](https://www.python.org/downloads/).

- Set environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to your AWS key and secret. (Received by Email)
- Clone the workshop git repository into your machine and install:
```
git clone https://github.com/doitintl/athena-workshop.git
cd athena-workshop/jdbc
npm i
```

- Run the application to query Athena from NodeJS and get the daily total fare paid:
```
npm start
```

- After about 5 seconds the application should terminate after having printed output such as this:
```
Results: [{"vendor":"VTS","total":66.75000190734863},{"vendor":"CMT","total":14.200000286102295},{"vendor":"DDS","total":6.300000190734863}]
```

**You have successfully completed Lab 2 ;-)**
