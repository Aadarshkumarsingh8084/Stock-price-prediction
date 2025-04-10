from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

# Load the pre-trained CNN model
model = load_model('trained_model.h5')

@app.route('/predict', methods=['GET'])
def predict():
    symbol = request.args.get('symbol', 'AAPL')
    days = int(request.args.get('days', 30))
    
    try:
        # Fetch historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days*2)  # Get more data for preprocessing
        
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
        if stock_data.empty:
            return jsonify({'error': 'No data available for this symbol'}), 400
        
        # Preprocess data
        processed_data = preprocess_data(stock_data)
        
        # Make prediction
        prediction = model.predict(processed_data)
        next_day_price = prediction[0][0]
        
        # Generate response
        response = {
            'symbol': symbol,
            'nextDayPrice': float(next_day_price),
            'predictedTrend': 'Up' if next_day_price > stock_data['Close'].iloc[-1] else 'Down',
            'confidence': float(np.max(prediction)),
            'historicalData': {
                'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
                'prices': stock_data['Close'].tolist()
            },
            'predictedData': {
                'dates': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)],
                'prices': [float(next_day_price * (1 + (i * 0.01))) for i in range(7)]  # Simple projection
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def preprocess_data(data):
    """
    Preprocess stock data for the CNN model
    """
    # Normalize data
    close_prices = data['Close'].values
    normalized_prices = (close_prices - np.mean(close_prices)) / np.std(close_prices)
    
    # Create sequences (assuming the model expects 30-day sequences)
    sequence_length = 30
    sequences = []
    
    for i in range(len(normalized_prices) - sequence_length):
        sequences.append(normalized_prices[i:i+sequence_length])
    
    # Reshape for CNN input (samples, time steps, features, channels)
    sequences = np.array(sequences)
    sequences = sequences.reshape((sequences.shape[0], sequences.shape[1], 1, 1))
    
    return sequences

if __name__ == '__main__':
    app.run(debug=True)
