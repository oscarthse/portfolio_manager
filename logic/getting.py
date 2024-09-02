import os
from google.cloud import bigquery, storage
import pandas as pd
import tensorflow as tf
import tempfile
import io

def get_price_data_raw(ticker):
    client = bigquery.Client(project="portfolio-manager-433711")
    table_ref = f"portfolio-manager-433711.raw.{ticker}_raw"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()

    return df

def get_technical_analysis(ticker):
    client = bigquery.Client(project="portfolio-manager-433711")
    table_ref = f"portfolio-manager-433711.technical_analysis.{ticker}_technical_analysis"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()

    return df

def get_macro_data():
    client = bigquery.Client(project="portfolio-manager-433711")
    table_ref = "portfolio-manager-433711.macro.macro"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()

    return df

def get_neural_nets(ticker):
    storage_client = storage.Client()
    bucket = storage_client.bucket('model-bucket-portfolio')
    blob_name = f'model_{ticker}.keras'
    blob = bucket.blob(blob_name)
    model_bytes = blob.download_as_bytes()

    # Create a temporary file to store the model bytes
    with tempfile.NamedTemporaryFile(suffix='.keras') as temp_model_file:
        temp_model_file.write(model_bytes)
        temp_model_file.flush()  # Ensure all data is written

        # Load the model from the tempora file
        model = tf.keras.models.load_model(temp_model_file.name)
    return model

def get_price_data_test_raw(ticker):
    client = bigquery.Client(project="portfolio-manager-433711")
    table_ref = f"portfolio-manager-433711.raw_test.{ticker}_raw_price_data"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()
    df = df.sort_values(by='datetime')

    return df

def get_technical_analysis_test(ticker):
    client = bigquery.Client(project="portfolio-manager-433711")
    table_ref = f"portfolio-manager-433711.technical_analysis_test.{ticker}_test_data_technical_analysis"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()
    df = df.sort_values(by='timestamp_field_0')

    return df
