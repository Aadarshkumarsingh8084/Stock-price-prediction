import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to prepare data for prediction
def prepare_data(stock_data):
    stock_data['Date'] = stock_data.index
    stock_data['Date_ordinal'] = stock_data['Date'].apply(lambda x: x.toordinal())
    X = stock_data[['Date_ordinal']]
    y = stock_data['Close']
    return X, y

# Function to train and predict stock prices
def predict_stock_price(X, y, future_days=30):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Predict future prices
    last_date = X.iloc[-1, 0]
    future_dates = [last_date + i for i in range(1, future_days + 1)]
    future_X = pd.DataFrame(future_dates, columns=['Date_ordinal'])
    future_prices = model.predict(future_X)

    return y_test, y_pred, future_X, future_prices, model

# Function to plot results
def plot_results(stock_data, y_test, y_pred, future_X, future_prices):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['Close'], label='Actual Price', color='blue')
    plt.plot(y_test.index, y_pred, label='Predicted Price (Test)', color='green')
    future_dates = pd.to_datetime([pd.Timestamp.fromordinal(d) for d in future_X['Date_ordinal']])
    plt.plot(future_dates, future_prices, label='Future Prediction', color='red', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.title('Stock Price Prediction')
    plt.legend()
    plt.grid()
    plt.show()

# Main execution
if __name__ == "__main__":
    # Input parameters
    ticker = "AAPL"  # Stock symbol (e.g., AAPL for Apple)
    start_date = "2020-01-01"
    end_date = "2023-01-01"

    # Fetch stock data
    stock_data = fetch_stock_data(ticker, start_date, end_date)

    # Prepare data
    X, y = prepare_data(stock_data)

    # Train model and predict
    y_test, y_pred, future_X, future_prices, model = predict_stock_price(X, y)

    # Print model accuracy (R-squared score)
    print(f"Model R-squared score: {model.score(X, y):.2f}")

    # Plot results
    plot_results(stock_data, y_test, y_pred, future_X, future_prices)
