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

- using java program

```
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar pi 10 100
```

- using python mapper and reducer (wordcount example)

copy mapper and reducer from local to edge:

```
scp source <host>:dest
```

run yarn command

```
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
	-files mapper.py, reducer.py \
	-mapper "python mapper.py" \
	-reducer "python reducer.py" \
	-input raw/input.txt \
	-output mr/output
```

#### HIVE

Connection command (on the edge node): 

```
beeline -u "jdbc:hive2://zoo-1.au.adaltas.cloud:2181,zoo-2.au.adaltas.cloud:2181,zoo-3.au.adaltas.cloud:2181/dsti;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;"
```

Create external table pointing to drivers.csv

```
CREATE EXTERNAL TABLE IF NOT EXISTS a_jourdan(
  driverId INT, name STRING, ssn INT,    
  location STRING, certified STRING, wageplan STRING)
  COMMENT 'a.jourdan-dsti table from drivers.csv'
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  STORED AS TEXTFILE
  LOCATION '/user/a.jourdan-dsti/drivers_raw'
  TBLPROPERTIES ('skip.header.line.count' = '1');
```

Use query stored in file

```
!run hive/driver_create_external.hql
```

Create ORC table

```
CREATE TABLE IF NOT EXISTS a_jourdan_orc(
  driverId INT, name STRING, ssn INT,    
  location STRING, certified STRING, wageplan STRING)
  COMMENT 'a.jourdan-dsti table from drivers.csv'
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  STORED AS ORC
  LOCATION '/user/a.jourdan-dsti/drivers_orc';
```

Insert data from external table

```
INSERT INTO TABLE a_jourdan_orc SELECT * FROM a_jourdan;
```

