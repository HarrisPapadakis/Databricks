# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest constructors.json file
# MAGIC 1. Read the file using Spark dataframe reader API
# MAGIC 1. Add Metadata Columns
# MAGIC     - Source File
# MAGIC     - Ingestion Timestamp
# MAGIC 1. Write to bronze delta table

# COMMAND ----------

# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# MAGIC %run ../00-common/02.Bronze-helpers
# MAGIC

# COMMAND ----------


# Define source_file and table_name
source_file = f"{landing_folder_path}/constructors.json"
table_name = f"{catalog_name}.{bronze_schema}.constructors"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1 - Read the json file using the dataframe reader API

# COMMAND ----------

# Define the schema for the DataFrame
constructors_schema = """constructorId STRING,
                         name STRING,
                         nationality STRING,
                        url STRING"""

# COMMAND ----------

# Read data from the constructor file
constructors_df = (
    spark.read
        .format('json')
        .schema(constructors_schema)
        .option('mode','FAILFAST')
        .load(source_file)
)



# COMMAND ----------

display(constructors_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2 - Add Metadata Columns
# MAGIC - Source File
# MAGIC - Ingestion Timestamp

# COMMAND ----------

constructors_final_df = add_ingestion_metadata(constructors_df)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3 - Write to bronze delta table

# COMMAND ----------

(
    constructors_final_df
        .write
        .format('delta')
        .mode('overwrite')
        .saveAsTable(table_name)
)

# COMMAND ----------

display(spark.table(table_name))