# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest circuits.csv file
# MAGIC 1. Read the file using Spark dataframe reader API
# MAGIC 1. Add Metadata Columns
# MAGIC     - Source File
# MAGIC     - Ingestion Timestamp
# MAGIC 1. Write to bronze delta table

# COMMAND ----------

# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# MAGIC %run ../00-common/02.Bronze-helpers

# COMMAND ----------

source_file = f"{landing_folder_path}/circuits.csv"
table_name = f"{catalog_name}.{bronze_schema}.circuits"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1 - Read the CSV file using the dataframe reader API

# COMMAND ----------

from pyspark.sql.types import StructType, StructField,  StringType, DoubleType

circuits_schema = StructType([
    StructField('circuitId',       StringType()),
    StructField('url',             StringType()),
    StructField('circuitName',     StringType()),
    StructField('lat',             DoubleType()),
    StructField('long',            DoubleType()),
    StructField('locality',        StringType()),
    StructField('country',         StringType())
])
 

# COMMAND ----------

# DBTITLE 1,Cell 6
circuits_df = (
    spark.read
        .format('csv')
        .option('header', True)
#        .option('inferSchema', True)
        .option('mode', 'failFast')
        .schema(circuits_schema)
        .load(source_file)
)

# COMMAND ----------

display(circuits_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2 - Add Metadata Columns
# MAGIC - Source File
# MAGIC - Ingestion Timestamp

# COMMAND ----------

circuits_final_df = add_ingestion_metadata(circuits_df)


# COMMAND ----------

display(circuits_final_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Step 3 - Write to bronze delta table

# COMMAND ----------

(
    circuits_final_df
        .write
        .format('delta')
        .mode('overwrite')
        .saveAsTable(table_name)
)

# COMMAND ----------

display(spark.table(table_name))