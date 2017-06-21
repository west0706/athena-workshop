# Lab 3 - 데이터 파티셔닝

>*이 Lab에서는 어떻게 파티션된 테이블을 만들고 쿼리하는 지 배웁니다.*
>
>**^^^이번 실습은 모두 US East(N.Virginia)리전에서 진행됩니다.^^^**

![alt tag](../images/region.png)

## Spark EMR cluster 만들기

- 미리 EC2 Console에서 Keypair을 생성합니다.[at this link](http://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-access-ssh.html)
- EMR Console에서 'Create cluster'를 클릭합니다.
- Cluster name을 입력합니다 : workshop-athena
- Applications을 선택합니다 : Spark
- Instance type을 선택합니다 : r3.xlarge
- EC2 key pair에 아까 생성한 키파일을 선택합니다
- 마지막으로 Create cluster를 클릭하여 Cluster를 생성합니다.


## Spark EMR cluster master 접속하기

- EC2 (Security Group) console에서 ElasticMapReduce-master 를 찾습니다.
- 해당 SG에서 Inbound – edit - Add Rule 클릭, 자신의 IP를 SSH 허용합니다.
- 아까 생성한 EMR cluster의 상태가 ready가 되면, 클릭하여 Master public DNS을 이용하여 SSH 접속합니다.
- 접속이 되면 `screen` command를 한번 입력한다.
  $screen

## 파티셔닝 batch job 만들기

- Spark Shell을 로드합니다.
  $spark-shell
- 다음의 command을 Spark Shell 프롬프트에서 실행합니다.

```java
import org.apache.spark.sql.hive.orc._
import org.apache.spark.sql._

val hiveContext = new org.apache.spark.sql.hive.HiveContext(sc)
```

- 읽을 external CSV table을 정의합니다.
 **이때`<BUCKET NAME>`은 아까 생성한 버킷 이름으로 바꿔서 입력합니다.**
 
```java
hiveContext.sql("CREATE EXTERNAL TABLE IF NOT EXISTS yellow_trips_csv(" +
  "pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING) " +
  "ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' " +
  "LOCATION 's3://<BUCKET NAME>/csv/'")
```

- CSV hive table로부터 데이터를 읽습니다.

```java
val data=hiveContext.sql("select *,date_sub(from_unixtime(pickup_timestamp),0) as pickup_date from yellow_trips_csv limit 100")
```

- 데이터를 쓰는 곳을 지정합니다.
**이때 `<BUCKET NAME>`은 수정합니다.**
```java
data.write.mode("overwrite").partitionBy("pickup_date").parquet("s3://<BUCKET NAME>/parquet-partitioned/")
```

- 작업이 끝나길 기다립니다.
- s3 버킷에 PARQUET file이 생성된 것을 확인합니다.

## 파티션된 파일을 Athena에서 쿼리하기

- Athena console 을 엽니다.
- Create an external table from the partitioned PARQUET files.

>**이때 `<BUCKET NAME>`은 수정합니다.**

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.yellow_trips_parquet_partitioned(pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING)
PARTITIONED BY (pickup_date TIMESTAMP)
STORED AS parquet
LOCATION 's3://<BUCKET NAME>/parquet-partitioned/'
```

- table partition을 로드합니다.

```sql
MSCK REPAIR TABLE yellow_trips_parquet_partitioned
```

- 파티션된 테이블에 쿼리를 실행시킵니다.

```sql
select *
from
(
  select date_trunc('day',from_unixtime(pickup_timestamp)) as pickup_date1,*
  from awskrug.yellow_trips_parquet_partitioned
  where pickup_date between timestamp '2016-05-12' and timestamp '2016-05-22'
)
where pickup_date1 between timestamp '2016-05-12' and timestamp '2016-05-22'
```

#- 파티셔닝되지 않은 parquet external table을 만듭니다. ##lab1에 진행완료

```sql
# CREATE EXTERNAL TABLE IF NOT EXISTS awskrug.yellow_trips_parquet(pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING)
# STORED AS parquet
# LOCATION 's3://<BUCKET NAME>/parquet/';
```

- 아까의 실행 결과와 다음의 쿼리 실행결과에서 시간과 스캔하는 데이터를 비교해봅니다.

```sql
select *
from
(
  select date_trunc('day',from_unixtime(pickup_timestamp)) as pickup_date1,*
  from awskrug.yellow_trips_parquet
)
where pickup_date1 between timestamp '2016-05-12' and timestamp '2016-05-22'
```
