# Hadoop-Spark

#### Connect to Edge (through VPN)

#### HDFS most common commands

```
hdfs dfs -help
hdfs dfs -ls [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [<path> ...] 
hdfs dfs -cat [-ignoreCrc] <src> ...
hdfs dfs -mv <src> ... <dst>
hdfs dfs -cp [-f] [-p | -p[topax]] <src> ... <dst>
hdfs dfs -mkdir [-p] <path> ...
hdfs dfs -rm [-f] [-r|-R] [-skipTrash] [-safely] <src> ...

hdfs dfs -put [-f] [-p] [-l] <localsrc> ... <dst>
hdfs dfs -get [-p] [-ignoreCrc] [-crc] <src> ... <localdst>
```

#### webHDFS commands.

https://hadoop.apache.org/docs/r1.0.4/webhdfs.html

```
curl --negotiate -u : http://hdfs....cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw?op=LISTSTATUS

curl --negotiate -L -u : http://hdfs....cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw/input.txt?op=OPEN
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

run python scripts as mapper and reducer:

```
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
	-files mapper.py, reducer.py \
	-mapper "python mapper.py" \
	-reducer "python reducer.py" \
	-input raw/input.txt \
	-output mr/output
```

#### HIVE

