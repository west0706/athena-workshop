import org.apache.spark.sql.hive.orc._
import org.apache.spark.sql._

val hiveContext = new org.apache.spark.sql.hive.HiveContext(sc)

hiveContext.sql("CREATE EXTERNAL TABLE IF NOT EXISTS yellow_trips_csv(" +
  "pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING) " +
  "ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' " +
  "LOCATION 's3://nyc-yellow-trips/csv/'")

val data=hiveContext.sql("select *,date_sub(from_unixtime(pickup_timestamp),0) as pickup_date from yellow_trips_csv limit 10000")
data.write.mode("overwrite").partitionBy("pickup_date").parquet("s3://nyc-yellow-trips/parquet-partitioned-1/")

