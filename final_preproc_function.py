from supporting_functions import *

def create_x_y_logdf(df_data, df_technical, df_macroeconomic):
    df_macroeconomics = rename_macroeconomic(df_macroeconomic)
    df_technical = rename_technical(df_technical)
    df_data = rename_columns(df_data)
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
    y = df_time[["Target"]]
    log_df = log_divide_next(df_data["close"])
    return X, y, log_df
