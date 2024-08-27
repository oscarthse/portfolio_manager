import os
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project="portfolio-manager-433711")


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
    table_ref = "portfolio-manager-433711.macro.macro_data"
    query = f"""
    SELECT *
    FROM {table_ref}
    """

    df = client.query(query).to_dataframe()

    return df
