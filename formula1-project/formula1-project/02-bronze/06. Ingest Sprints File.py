# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest Sprints.json file
# MAGIC 1. Read the file using Spark dataframe reader API
# MAGIC 1. Define and enforce schema
# MAGIC 1. Add Metadata Columns
# MAGIC     - Source File
# MAGIC     - Ingestion Timestamp
# MAGIC 1. Write to bronze delta table

# COMMAND ----------

# DBTITLE 1,s
# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# MAGIC %run ../00-common/02.Bronze-helpers
# MAGIC

# COMMAND ----------


# Define source_file and table_name
source_file = f"{landing_folder_path}/sprints"
table_name = f"{catalog_name}.{bronze_schema}.sprints"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1 - Read the json file using the dataframe reader API

# COMMAND ----------

# DBTITLE 1,Cell 6
# Define the schema
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType, DateType

results_schema = StructType([
    StructField('date', DateType()),
    StructField('raceName', StringType(),),
    StructField('round', IntegerType()),
    StructField('season', IntegerType(),),
    StructField('url', StringType()),
    StructField('constructorId', StringType(),),
    StructField('driverId', StringType()),
    StructField('grid', IntegerType(),),
    StructField('laps', IntegerType()),
    StructField('number', IntegerType(),),
    StructField('points', FloatType()),
    StructField('position', IntegerType(),),
    StructField('positionText', StringType()),
    StructField('status', StringType(),)
])
    

# COMMAND ----------

# Read data from the sprints file

sprints_df = (
    spark.read
        .format('json')
        .schema(sprints_schema)
        .option('mode','FAILFAST')
        .option('multinLine', True)
        .load(source_file)
)



# COMMAND ----------

display(sprints_df

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2 - Add Metadata Columns
# MAGIC - Source File
# MAGIC - Ingestion Timestamp

# COMMAND ----------

results_final_df = add_ingestion_metadata(results_df)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3 - Write to bronze delta table

# COMMAND ----------

(
    results_final_df
    .write
    .format('delta')
    .mode('overwrite')
    .saveAsTable(table_name)     
)

# COMMAND ----------

display(spark.table(table_name))

# COMMAND ----------

# MAGIC %sql
# MAGIC select season, count(*)
# MAGIC from formula1.bronze.results
# MAGIC where season is not null
# MAGIC group by season
# MAGIC order by season