# Hadoop-Spark

#### Connect to Edge (through VPN)

#### HDFS most common commands

```bash
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

```bash
curl --negotiate -u : http://hdfs....cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw?op=LISTSTATUS

curl --negotiate -L -u : http://hdfs....cloud:50070/webhdfs/v1/user/a.jourdan-dsti/raw/input.txt?op=OPEN
```

#### run YARN command

- using java program

```bash
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar pi 10 100
```

- using python mapper and reducer (wordcount example)

copy mapper and reducer from local to edge:

```bash
scp source <host>:dest
```

run yarn command

```bash
yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
	-files mapper.py, reducer.py \
	-mapper "python mapper.py" \
	-reducer "python reducer.py" \
	-input raw/input.txt \
	-output mr/output
```

#### HIVE

Connection command (on the edge node): 

```bash
beeline -u "jdbc:hive2://zoo-1.au.adaltas.cloud:2181,zoo-2.au.adaltas.cloud:2181,zoo-3.au.adaltas.cloud:2181/dsti;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;"
```

Create external table pointing to drivers.csv

```sql
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

Or Use query stored in file

```
!run hive/drivers_create_external.hql
```

Create ORC table (optimized format)

```sql
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

```sql
INSERT INTO TABLE a_jourdan_orc SELECT * FROM a_jourdan;
```

Joined Query

- never do:

```sql
SELECT * FROM TOTO,TATA WHERE TOTO.TOTOID = TATA.TOTOID
```

- use

```sql
SELECT * FROM TOTO JOIN TATA ON TOTO.TOTOID = TATA.TOTOID
```





### IMDB Queries:

1) Number of titles with duration superior than 2 hours.

```sql
SELECT
count(primarytitle)
FROM
imdb_title_basics
WHERE runtimeminutes>120;
```

RESULT: 60446

2) Average duration of titles containing the string "world".

```sql
SELECT
avg(runtimeminutes)
FROM
imdb_title_basics
WHERE primarytitle like '%world%';
```

RESULT: 43.58105263157895

3) Average rating of titles having the genre "Comedy"

```sql
SELECT
avg(averagerating)
FROM
imdb_title_basics JOIN imdb_title_ratings
ON imdb_title_basics.tconst = imdb_title_ratings.tconst
WHERE array_contains(genres,'Comedy');
```

RESULT: 6.970428788330675

4) Average rating of titles not having the genre "Comedy"

```sql
SELECT
avg(averagerating)
FROM
imdb_title_basics JOIN imdb_title_ratings
ON imdb_title_basics.tconst = imdb_title_ratings.tconst
WHERE NOT array_contains(genres,'Comedy');
```

RESULT: 6.886042545766032

5) Top 10 movies directed by Quentin Tarantino

```sql
SELECT primarytitle,averagerating  
FROM
	(SELECT tconst
	FROM imdb_title_crew
	WHERE array_contains(director,(
        SELECT nconst
		FROM imdb_name_basics
		WHERE primaryname LIKE 'Quentin Tarantino')
        )
    ) AS qt
JOIN 
	imdb_title_basics ON qt.tconst = imdb_title_basics.tconst
JOIN
	imdb_title_ratings ON imdb_title_ratings.tconst = imdb_title_basics.tconst
ORDER BY averagerating DESC
LIMIT 10;
```

RESULT:

```
+-------------------------------------+----------------+
|            primarytitle             | averagerating  |
+-------------------------------------+----------------+
| Pulp Fiction                        | 8.9            |
| Kill Bill: The Whole Bloody Affair  | 8.8            |
| Grave Danger: Part 2                | 8.6            |
| Grave Danger: Part 1                | 8.6            |
| Django Unchained                    | 8.4            |
| Reservoir Dogs                      | 8.3            |
| Inglourious Basterds                | 8.3            |
| Kill Bill: Vol. 1                   | 8.1            |
| Sin City                            | 8.0            |
| Kill Bill: Vol. 2                   | 8.0            |
+-------------------------------------+----------------+
```

For the last query, try it in two queries first if you want.
You'll see that you have to make a join on some array type. Hint: "explode"