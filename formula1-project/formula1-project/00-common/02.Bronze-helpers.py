# Databricks notebook source
# Helper function t oadd the file metadata for ingestion (source file and ingestion timestamp)

from pyspark.sql import functions as f

def add_ingestion_metadata(df):
    return (
        df
        .withColumn("ingestion_timestamp", f.current_timestamp())
        .withColumn("source_file", f.input_file_name())
)

  