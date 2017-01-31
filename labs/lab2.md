#Lab 2 - Interacting with AWS Athena#

*During this lab, you will create a new database using the AWS Management Console, create a new table and run your first query. Then you will connect to your table using MySQLWorkbench as well as visualize the data using AWS QuickSight*

**^^^Please make sure you are using US-East region (N.Virginia)^^^**

**Examine S3 bucket content**
 - Open [AWS Management Console Console](https://dahouse.signin.aws.amazon.com/console) and navigate to S3
 - Locate the ```nyc-yellow-trips``` bucket and navigate to ```csv``` folder. Note the amount of files and the format by downloading [sample file](https://s3.amazonaws.com/nyc-yellow-trips/csv/trips999999999999.csv)

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
  - Value: ```s3://your-full-name-jdbc-staging/```
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
 - Enter the name ```your-name-yellow-trips-csv``` and click ```Create Data Source```
 - Select the database with your username , the table ```yellow_trips_csv``` and then click ```Edit/Preview Data```
 - In the table view find the ```pickup_timestamp``` & ```dropoff_timestamp``` columns and click the ‘#’ (hash) icon just below the column title. Select ```Date``` from the drop-down list.
 - In the left side panel ```Fields``` section find the ```pickup_datetime``` & ```dropoff_datetime``` columns and uncheck it.
 - Click ```Save & Visualize```
 - Select ```Vertical Bar Chart``` from the ```Visual Types``` Panel
 - Drag ```vendor_id``` into ‘Group/Color’ box
 - Drag ```rate_code``` into ‘X axis’ box
 - Drag ```trip_distance``` into ‘Value’ box, then click the down arrow of the box and select ```Average``` under the  ```Aggregate```
 
 **You have succesfully completed Lab 2 ;-)**
