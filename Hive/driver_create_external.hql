CREATE EXTERNAL TABLE IF NOT EXISTS a_jourdan(
  driverId INT, name STRING, ssn INT,    
  location STRING, certified STRING, wageplan STRING)
  COMMENT 'a.jourdan-dsti table from drivers.csv'
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  STORED AS TEXTFILE
  LOCATION '/user/a.jourdan-dsti/drivers_raw'
  TBLPROPERTIES ('skip.header.line.count' = '1');