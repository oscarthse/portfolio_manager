import numpy as np

def create_lstm_windows(X_scaled, y, window_size):

    X_windows = []
    y_windows = []

    for i in range(len(X_scaled) - window_size):
        X_windows.append(X_scaled.iloc[i:i + window_size].values)
        y_windows.append(y.iloc[i + window_size])

    return np.array(X_windows), np.array(y_windows)
