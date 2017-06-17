# Lab 1 - AWS Athena 사용해보기

>*이번 실습에서는 AWS Management Console을 사용하여 새 데이터베이스 및 테이블을 만들고 Athena를 이용하여 쿼리를 실행합니다. 추가로 MySQLWorkbench를 사용하여 생성한 테이블에 연결하고 AWS QuickSight를 사용하여 데이터를 시각화하는 법을 수행합니다.*
>
>**^^^AWS console을 US-East Region (N.Virginia)로 설정해주세요.^^^**

![alt tag](../images/region.png)

## Database 및 Table 생성

- [AWS Management Console Console](https://console.aws.amazon.com/console/home) 을 열고 'Athena' 서비스 선택
- **Database** 생성하기
- `Query Editor` 에 아래 DDL Query 구문을 입력 후 `Run Query` 클릭

```sql
CREATE DATABASE IF NOT EXISTS awskrug
```

- 다음은 csv 파일로 부터 **external table** 생성하기
- `Query Editor` 에 아래 DDL query 구문을 입력 후 `Run Query` 클릭

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.yellow_trips_csv(
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
         LOCATION 's3://awskrug-athena-workshop/nyc-yellow-trips/csv/'
```

- 'Athena' 서비스에서 상단의 탭의 'Catalog Manager'를 선택후
 생성한 `awskrug` Database 와 `yellow_trips_csv` Table 확인
- 첫 번째 Query를 내릴 준비가 되었습니다.
- 아래 Query를 'Athena'의 `Query Box`에 붙여 넣은뒤 `Format Query` 를 클릭
- `Click Run Query` 클릭
- Run time 실행시간과 Data scanned 값을 기억해 두시기 바랍니다.

```sql
SELECT
from_unixtime(yellow_trips_csv.pickup_timestamp)
as pickup_date,
from_unixtime(yellow_trips_csv.dropoff_timestamp) 
as dropoff_date,
*
FROM awskrug.yellow_trips_csv
LIMIT 100
```

## Interact with AWS Athena using JDBC Driver

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
- Value: ```s3://awskrug-jdbc-staging/```
- Click OK
- Run the following query in the SQL Workbench query window

```sql
SELECT
from_unixtime(yellow_trips_csv.pickup_timestamp) as pickup_date,
from_unixtime(yellow_trips_csv.dropoff_timestamp) as dropoff_date,
*
FROM awskrug.yellow_trips_csv
LIMIT 100
```

## Interact with AWS Athena using AWS QuickSight

- Open QuickSight from [here](https://us-east-1.quicksight.aws.amazon.com)

- Click Manage Data
- Click New Data Set
- Select Athena as your data source
- Enter the name ```awskrug-yellow-trips-csv``` and click ```Create Data Source```
- Select the database with your username , the table ```yellow_trips_csv``` and then click ```Edit/Preview Data```
- Open the 'Tables' panel and click 'Switch to custom SQL tool'
- Enter any name for the Query and copy the following SQL into the 'Custom SQL' text box

```sql
SELECT
*,
greatest(0,trip_distance*3600.0/(dropoff_timestamp-pickup_timestamp)) as avg_speed,
hour(from_unixtime(pickup_timestamp)) as hour
FROM awskrug.yellow_trips_csv
WHERE
pickup_timestamp is not null and
pickup_timestamp is not null and
pickup_timestamp<>dropoff_timestamp
```

- Click 'Finish'
- Click ```Save & Visualize```
- Select ```Vertical Bar Chart``` from the ```Visual Types``` Panel
- Drag ```hour``` into ‘X axis’ box
- Drag ```avg_speed``` into ‘Value’ box, then click the down arrow of the box and select ```Average``` under the  ```Aggregate```

## Interact with Athena from a NodeJS application using JDBC

- Open AWS console at [https://console.aws.amazon.com/athena/](https://console.aws.amazon.com/athena/)

- Enter the following DDL query into the query window
- *Remember to replace `awskrug` with your AWS username. (e.g. shaharf)*

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.yellow_trips_parquet(
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
) STORED AS PARQUET LOCATION 's3://awskrug-athena-workshop/nyc-yellow-trips/parquet/';
```

- Make sure you have Python 2.7, NodeJS and NPM installed on your machine. If not install from [here](https://nodejs.org/en/download/) and [here](https://www.python.org/downloads/).

- Set environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to your AWS key and secret. (Received by Email)
- Clone the workshop git repository into your machine and install:

```bash
git clone https://github.com/doitintl/athena-workshop.git
cd athena-workshop/jdbc
npm i
```

- Run the application to query Athena from NodeJS and get the daily total fare paid:

```bash
npm start
```

- After about 5 seconds the application should terminate after having printed output such as this:

```json
Results: [{"vendor":"VTS","total":66.75000190734863},{"vendor":"CMT","total":14.200000286102295},{"vendor":"DDS","total":6.300000190734863}]
```

## You have successfully completed Lab 2 ;-)
