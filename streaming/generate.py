from __future__ import print_function
import logging
import json
from pyspark import SparkContext
from pyspark.sql import SparkSession
from boto import kinesis

logger = logging.getLogger('py4j')

kinesisStreamName='srfrnk_doit'

def write_partition(partition):
        kinesisClient = kinesis.connect_to_region("us-east-1")
        for row in partition:
            kinesisClient.put_record(kinesisStreamName, json.dumps(row),"partitionKey")

if __name__ == "__main__":
    appName='Send2KinesisStream'

    sc = SparkContext()

    sqlContext = SparkSession.builder.enableHiveSupport().getOrCreate();
    sqlContext.sql("CREATE EXTERNAL TABLE IF NOT EXISTS yellow_trips_parquet(" +
                    "pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING) " +
                    "STORED AS parquet " +
                    "LOCATION 's3://nyc-yellow-trips/parquet/'")



    lines=sqlContext.sql("select * from yellow_trips_parquet limit 100")
    lines.foreachPartition(write_partition)


