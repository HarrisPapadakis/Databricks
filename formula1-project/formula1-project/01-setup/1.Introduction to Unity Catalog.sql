-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Set-up the project environment for Formula1 Project
-- MAGIC
-- MAGIC 1. Create External Location databricks-course-ext-dl1-formula1
-- MAGIC 1. Create Catalog formula1
-- MAGIC 1. Create Schemas landing,bronze,silver and gold
-- MAGIC 1. Create Volume Files in the landing schema
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Access Cloud Storage**

-- COMMAND ----------

-- DBTITLE 1,Cell 3
-- MAGIC %fs ls 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/'

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC **Create External Location**

-- COMMAND ----------

-- DBTITLE 1,Cell 5
-- The external location already exists but uses the wrong credential.
-- Run this once to switch it to the managed identity credential:
ALTER EXTERNAL LOCATION formula1dlharris
  SET STORAGE CREDENTIAL `formula1dlharris_azuremanagedidentity_1782060661052`;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Create Catalog formula1

-- COMMAND ----------

show catalogs;

-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS formula1
    MANAGED LOCATION 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/'
    COMMENT 'This is the main catalog for the formula1 project' ;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Create Schemas landing,bronze,silver and gold

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS formula1.landing;

CREATE SCHEMA IF NOT EXISTS formula1.bronze
     MANAGED LOCATION 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/bronze';

CREATE SCHEMA IF NOT EXISTS formula1.silver
     MANAGED LOCATION 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/silver';

CREATE SCHEMA IF NOT EXISTS formula1.gold
     MANAGED LOCATION 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/gold';

-- COMMAND ----------

select current_catalog();

-- COMMAND ----------

use catalog formula1

-- COMMAND ----------

show schemas;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC # Create Volume Files 

-- COMMAND ----------

CREATE EXTERNAL VOLUME formula1.landing.files
LOCATION 'abfss://formula1-raw@formula1dlharris.dfs.core.windows.net/landing';

-- COMMAND ----------

-- MAGIC %fs ls /Volumes/formula1/landing/files