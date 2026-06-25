# Databricks notebook source
# MAGIC %md
# MAGIC #Configure Access to Cloud Storage via Unity Catalog
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC **Access Cloud Storage**

# COMMAND ----------

display(dbutils.fs.ls('abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/'))

# COMMAND ----------

# MAGIC %md
# MAGIC **Create External Location**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS formula1dlharris
# MAGIC URL 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `formula1dlharris_azuremanagedidentity_1782060661052`)
# MAGIC COMMENT 'External location for formula1 raw container';