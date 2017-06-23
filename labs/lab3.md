# Lab 2 - 지원되는 형식 및 SerDes(serializer/deserializers)

>*이번 랩에서는 다양한 파일 포맷으로 EXTERNAL 테이블을 정의하는 방법에 대해서 살펴보겠습니다.*
>
>**^^^AWS console을 US-East Region (N.Virginia)로 설정해주세요.^^^**

![alt tag](../images/region.png)

- AWS console 열기 [https://console.aws.amazon.com/athena/](https://console.aws.amazon.com/athena/)
- Query 창에 다음의 DDL 쿼리를 입력하세요
## CSV파일로 부터 테이블 생성

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.big_yellow_trips_csv(
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
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
  LOCATION 's3://awskrug-athena-workshop/nyc-yellow-trips/csv/';
```

## Pargquet 파일로 부터 테이블 생성


```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.big_yellow_trips_parquet(
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

## ORC 파일로 테이블 생성

- Query 창에 다음의 DDL 쿼리를 입력하세요

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.big_yellow_trips_orc(
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
) STORED AS ORC LOCATION 's3://awskrug-athena-workshop/nyc-yellow-trips/orc/';
```

## 쿼리 성능 비교하기

- 아래의 쿼리를 하나씩 실행하고, 아무 데이터도 나오지 않을 때의 쿼리 성능을 비교해 보세요.

```sql
SELECT COUNT(*) FROM awskrug.big_yellow_trips_csv;
SELECT COUNT(*) FROM awskrug.big_yellow_trips_parquet;
SELECT COUNT(*) FROM awskrug.big_yellow_trips_orc;
```

```sql
SELECT max(passenger_count) FROM awskrug.big_yellow_trips_csv WHERE vendor_id <> 'VTS';
SELECT max(passenger_count) FROM awskrug.big_yellow_trips_parquet WHERE vendor_id <> 'VTS';
SELECT max(passenger_count) FROM awskrug.big_yellow_trips_orc WHERE vendor_id <> 'VTS';
```

## 사용자 정의 포맷으로 텍스트 파일로 테이블을 생성

- Query 창에 다음의 DDL 쿼리를 입력하세요

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.elb_logs_raw_native (
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

- 쿼리 실행이 끝났을 때 아래의 쿼리를 실행해 보세요

```sql
SELECT * FROM awskrug.elb_logs_raw_native WHERE elb_response_code <> '200' LIMIT 100;
```

## 이전 쿼리의 결과값으로 테이블 생성

- ‘Settings’으로 들어가보세요.
- ‘Query results location’에 아이디를 하위폴더로 하여 설정하세요.
- 아래의 쿼리를 실행해보세요.

```sql
SELECT *
FROM awskrug.big_yellow_trips_csv
limit 10000;
```

- S3 bucket에 쿼리 결과가 있는지 확인해보세요. 그리고 Setting에서 추가한 폴더가 있는지 확인하세요.(경로는 다음과 비슷합니다 .../Unsaved/2017/01/24/aa9...fbb.csv)
- 재사용을 위하여 S3의 다른 하위 폴더에 결과값을 복사해주세요.
- Query 창에 다음의 DDL 쿼리를 입력하세요. `<RESULTS PATH>`의 값을 수정해주세요.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.big_yellow_trips_csv_query_result(
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

- 아래의 쿼리를 실행해보세요.

```sql
select count(*) from awskrug.big_yellow_trips_csv_query_result
```

## You have sucessully completed Lab 2 :-)
