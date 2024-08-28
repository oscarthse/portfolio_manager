from sklearn.preprocessing import MinMaxScaler

def initialize_scaler(X_train):
    mm_scaler = MinMaxScaler().set_output(transform="pandas")
    scaler_trained = mm_scaler.fit(X_train)
    return scaler_trained

def transform_scaler(scaler_trained, X):
    scaled_data = scaler_trained.transform(X)
    return scaled_data
