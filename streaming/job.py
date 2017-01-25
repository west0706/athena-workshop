from __future__ import print_function
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
from pyspark.sql import HiveContext
import logging
import json

logger = logging.getLogger('py4j')

targetPath="s3://srfrnk-doit/parquet/"
kinesisStreamName='srfrnk_doit'

def write_lines(rdd):
    if not rdd.isEmpty():
        json_rdd=rdd.map(lambda x:json.loads(x))
        rows=sqlContext.createDataFrame(json_rdd, table.schema)
        rows.registerTempTable('temp_rdd');
        rows.write.mode("append").parquet(targetPath)


if __name__ == "__main__":
    appName='KinesisStream2PARQUET'

    sc = SparkContext()

    sqlContext = HiveContext(sc)
    sqlContext.sql("CREATE EXTERNAL TABLE IF NOT EXISTS yellow_trips_schema(" +
                   "pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING) " +
                   "STORED AS parquet " +
                   "LOCATION 's3://nyc-yellow-trips/parquet/'")

    ssc = StreamingContext(sc, 1)

    table=sqlContext.sql("select * from yellow_trips_schema limit 1");

    lines = KinesisUtils.createStream(ssc, appName, kinesisStreamName,
                                      'https://kinesis.us-east-1.amazonaws.com', 'us-east-1',
                                      InitialPositionInStream.LATEST, 2)
    lines.foreachRDD(write_lines)

    ssc.start()
    ssc.awaitTermination()

