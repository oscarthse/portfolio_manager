from logic.supporting_functions import *

def create_x_y(df_data, df_technical, df_macroeconomic):
    df_macroeconomic = rename_macroeconomic(df_macroeconomic)
    df_technical = rename_technical(df_technical)
    df_data = rename_columns(df_data)
    df_data = df_data.sort_values(by="datetime")
    df_technical = df_technical.sort_values(by="datetime")
    df_macroeconomic = df_macroeconomic.sort_values(by="datetime")
    df_technical = clean_data(df_technical)
    df_data = convert_datetime(df_data)
    df_technical = convert_datetime(df_technical)
    df_macroeconomic = convert_datetime(df_macroeconomic)
    df_technical = merge_macroeconomic(df_technical, df_macroeconomic)
    df_merged = merge_columns(df_data, df_technical)
    df_target = create_target(df_merged, "close")
    df_final = target_drop(df_target)
    df_time = convert_time_sin_cos(df_final)
    X = df_time.drop(columns = "Target")
    X = X.drop(columns = "datetime")
    y_initial = df_time[["Target"]]
    y = split_into_categories(y_initial, "Target")
    y = y.drop(columns = "Target")
    log_df = log_divide_next(df_data).dropna()
    return X, y, log_df
