import numpy as np
import pandas as pd

def rename_macroeconomic(df_macroeconomic):
    df_macroeconomic = df_macroeconomic.drop(columns = "int64_field_0")
    columns_macroeconomic = ["datetime", "interest_rate", "GDP", "inflation"]
    df_macroeconomic.columns = columns_macroeconomic
    return df_macroeconomic

def merge_macroeconomic(df_technical, df_macroeconomic):
    df_merged = df_technical.merge(df_macroeconomic, on="datetime", how="inner")
    return df_merged

def rename_columns(df):
    columns = ["datetime", "open", "high", "low", "close", "volume"]
    df.columns = columns
    return df

def rename_technical(df_technical):
    df_technical = df_technical.rename(columns = {"timestamp_field_0": "datetime"})
    return df_technical

def convert_datetime(df):
    data = df.copy()
    data["datetime"] = pd.to_datetime(data["datetime"])
    return data

def merge_columns(df_values, df_technical):
    df_merged = df_values.merge(df_technical, how="inner", on="datetime")
    return df_merged

def clean_data(df):
    df_inter = df.interpolate(method='linear')
    df_clean = df_inter.dropna()
    return df_clean

def create_target(df, column_name, new_column_name='Target'):
    result = []
    for i in range(len(df) - 1):
        if df[column_name].iloc[i] > df[column_name].iloc[i-1]:
            result.append(1)
        else:
            result.append(0)
    result.append(float('nan'))
    df[new_column_name] = pd.Series(result, index=df.index)
    return df

def target_drop(df_final):
    df_final = df_final.dropna()
    return df_final

def convert_time_sin_cos(df):
    data = df.copy()
    data['day_of_year'] = data['datetime'].dt.dayofyear
    data['time_of_day'] = data['datetime'].dt.hour * 3600 + data['datetime'].dt.minute * 60 + data['datetime'].dt.second
    data['day_of_year_norm'] = data['day_of_year'] / 365.0
    data['time_of_day_norm'] = data['time_of_day'] / 86400.0
    data['cos_time_of_day'] = np.cos(2 * np.pi * data['time_of_day_norm'])
    data['sin_time_of_day'] = np.sin(2 * np.pi * data['time_of_day_norm'])
    data["cos_day_of_year"] = np.cos(2 * np.pi * data['day_of_year_norm'])
    data["sin_day_of_year"] = np.sin(2 * np.pi * data['day_of_year_norm'])
    df_converted = data.drop(columns = ["day_of_year", "time_of_day", "day_of_year_norm", "time_of_day_norm", "datetime"])
    return df_converted

def log_divide_next(df):
    log_returns = np.log(df['close'] / df['close'].shift(1))
    return log_returns
