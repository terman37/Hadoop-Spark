# Hadoop-Spark

#### Connect to Edge (through VPN)

#### HDFS Commands

```
hdfs dfs -ls
hdfs dfs -put ...
hdfs dfs -get ...
```

#### webHDFS commands.

https://hadoop.apache.org/docs/r1.0.4/webhdfs.html

```
curl --negotiate -u : http://hdfs-nn-1.au.adaltas.cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw?op=LISTSTATUS

curl --negotiate -L -u : http://hdfs-nn-1.au.adaltas.cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw/input.txt?op=OPEN
```

#### run YARN command

```
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar pi 10 100
```

using python mapper and reducer (wordcount example)

copy mapper and reducer from local to edge:

```
scp source <host>:dest
```

run

```
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
  -file mapper.py -mapper "python mapper.py" \
  -file reducer.py -reducer "python reducer.py" \
  -input raw/input.txt \
  -output mr/output
```

