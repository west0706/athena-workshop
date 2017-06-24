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

## EMR에 접속합니다

- You can reuse the EMR cluster created in the 랩 4에서 만들었던 EMR 클러스터를 재사용합니다.
- 로컬 PC로 [job.py](../streaming/job.py) 파일을 다운받습니다.
- 로컬 PC로 [generate.py](../streaming/generate.py) 파일 다운받습니다.
- job.py 파일의 `targetPath`(라인 12) 을 자신의 S3 버킷으로 수정합니다.
- job.py 파일의 `kinesisStreamName`(라인 13) 을 자신이 생성한 Kinesis 이름으로 수정합니다.
- generate.py 파일의 `kinesisStreamName`(라인 14)을 자신이 생성한 Kinesis Stream 이름으로 수정합니다
.- In a bash terminal run the following commands.

>Replace `<PEM FILE>` and `<EMR MASTER>` with the same values used when you connected via SSH

```bash
scp -i <PEM FILE> job.py hadoop@<EMR MASTER>:~/job.py
scp -i <PEM FILE> generate.py hadoop@<EMR MASTER>:~/generate.py
```

- 랩 3에서 생성한 EMR 마스터에 SSH로 접속합니다.
- Kinesis API를 위한 AWS 크레덴셜을 설정합니다. `<your-access-key>` 와 `<your-secret-key>` 를 변경합니다.


```bash
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_KEY=<your-secret-key>
```

- Run the job to push data into Kinesis Stream
- 

```bash
spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 generate.py
```

- Run the job to accept Kinesis Stream messages and save those into PARQUET files at your S3 bucket

```bash
spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 job.py
```

- Wait until the job kicks-in and watch your new PARQUET files as they are written into S3.
