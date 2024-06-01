--database creation
create  or replace database weatherdata;
--data schema creation
create or replace schema weather; 
--table creation
create or replace table weatherdata.weather.forecast(
    DATE TIMESTAMP_NTZ PRIMARY KEY,
    DAY_NAME varchar(15) not null,
    MONTH_NAME VARCHAR(15) not null,
    TEMPERATURE REAL not null,
    FEELS_LIKE REAL not null,
    DESCRIPTION varchar(20) not null,
    PRESSURE int not null,
    HUMIDITY INT not null,
    WINDSPEED REAL not null,
    WIND_DIRECTION int not null,
    CLOUDINESS int not null,
    PRECIPITATION REAL not null
);

--table creation
create or replace table weatherdata.weather.historical_forecast(
    DATE TIMESTAMP_NTZ PRIMARY KEY,
    DAY_NAME varchar(15) not null,
    MONTH_NAME VARCHAR(15) not null,
    TEMPERATURE REAL not null,
    FEELS_LIKE REAL not null,
    DESCRIPTION varchar(20) not null,
    PRESSURE int not null,
    HUMIDITY INT not null,
    WINDSPEED REAL not null,
    WIND_DIRECTION int not null,
    CLOUDINESS int not null,
    PRECIPITATION REAL not null
);

--file format object creation     
CREATE  or replace SCHEMA file_format;
-- creation of file format
CREATE OR REPLACE file format weatherdata.file_format.format_csv
    type = 'CSV'
    field_delimiter = ','
    RECORD_DELIMITER = '\n'
    skip_header = 1



--stage schema creation
CREATE or replace SCHEMA weatherdata.external_stage;
--stage creation
CREATE OR REPLACE STAGE weatherdata.external_stage.weather_ext_stage 
    url="path to folder on s3"
    credentials=(aws_key_id='aws access_key' 
    aws_secret_key='aws secrete key')
    FILE_FORMAT = weatherdata.file_format.format_csv;
;



list @weatherdata.external_stage.weather_ext_stage;


--pipe schema creation
create or replace schema weatherdata.weatherpipe;

--Pipe creation
CREATE OR REPLACE PIPE  weatherdata.weatherpipe.datapipe  
AUTO_INGEST = TRUE
AS
COPY INTO weatherdata.weather.forecast
FROM @weatherdata.external_stage.weather_ext_stage;

desc pipe weatherdata.weatherpipe.datapipe;