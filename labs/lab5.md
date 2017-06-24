# Lab 4 - 컬럼형식 변환하기

>*이번 랩에서는 CSV 와 JSON 같은 row기반 파일형식을 Kinesis Stream 을 통해 실시간으로 ORC 와 PARQUET 컬럼 형식으로 변환하는 방법에 대해 알아봅니다.*
>
>**^^^AWS 매니지먼트 콘솔을 US-East Region (N.Virginia)로 맞춰주세요.^^^**

![alt tag](../images/region.png)

## Kinesis Stream 만들기

- Kinesis 콘솔을 열어주세요 [this link](https://console.aws.amazon.com/kinesis/home?region=us-east-1#/streams/create)
- **Stream Name** 을 입력합니다.
- **Number of shards** 에 1을 넣습니다
- **Create Stream** 을 클릭합니다.

## Connect to EMR

- You can reuse the EMR cluster created in the lab 4.
- Download the file [job.py](../streaming/job.py) into your local machine
- Download the file [generate.py](../streaming/generate.py) into your local machine
- Edit the file job.py - set `targetPath`(line 12) to the path to your S3 bucket.
- Edit the file job.py - set `kinesisStreamName`(line 13) to the name of the Kinesis Stream you created.
- Edit the file generate.py - set `kinesisStreamName`(line 14) to the name of the Kinesis Stream you created.
- In a bash terminal run the following commands.

>Replace `<PEM FILE>` and `<EMR MASTER>` with the same values used when you connected via SSH

```bash
scp -i <PEM FILE> job.py hadoop@<EMR MASTER>:~/job.py
scp -i <PEM FILE> generate.py hadoop@<EMR MASTER>:~/generate.py
```

- SSH Connect into the EMR master as you have in lab 4.
- Set AWS credentials for Kinesis API. Replace `<your-access-key>` and `<your-secret-key>`

```bash
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_KEY=<your-secret-key>
```

- Run the job to push data into Kinesis Stream

```bash
spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 generate.py
```

- Run the job to accept Kinesis Stream messages and save those into PARQUET files at your S3 bucket

```bash
spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 job.py
```

- Wait until the job kicks-in and watch your new PARQUET files as they are written into S3.
