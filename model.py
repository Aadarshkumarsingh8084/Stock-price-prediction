import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def fetch_and_prepare_data(symbol='AAPL', days=365*5):
    """
    Fetch stock data and prepare it for training
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Download historical data
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    # Use only closing prices
    close_prices = stock_data['Close'].values.reshape(-1, 1)
    
    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(close_prices)
    
    return scaled_prices, scaler

def create_sequences(data, sequence_length=30):
    """
    Create input sequences and corresponding targets
    """
    X, y = [], []
    
    for i in range(len(data) - sequence_length - 1):
        X.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length])
    
    return np.array(X), np.array(y)

def build_cnn_model(input_shape):
    """
    Build a CNN model for stock price prediction
    """
    model = Sequential([
        Conv2D(32, (3, 1), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 1)),
        Conv2D(64, (3, 1), activation='relu'),
        MaxPooling2D((2, 1)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    
    return model

def train_model():
    # Fetch and prepare data
    data, scaler = fetch_and_prepare_data()
    
    # Create sequences
    X, y = create_sequences(data)
    
    # Reshape for CNN (samples, time steps, features, channels)
    X = X.reshape((X.shape[0], X.shape[1], 1, 1))
    
    # Split into train and test sets
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Build and train model
    model = build_cnn_model((X.shape[1], X.shape[2], X.shape[3]))
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, 
                        validation_data=(X_test, y_test), verbose=1)
    
    # Save the model
    model.save('trained_model.h5')
    
    # Plot training history
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.savefig('training_history.png')
    plt.close()
    
    return model, scaler

if __name__ == '__main__':
    print("Training CNN model...")
    model, scaler = train_model()
    print("Model training complete and saved as 'trained_model.h5'")
