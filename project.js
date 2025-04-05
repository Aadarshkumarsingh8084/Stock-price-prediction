let stockChart = null;

async function fetchStockData() {
    const stockSymbol = document.getElementById('stockSymbol').value;
    const apiKey = '9SPII8ZJVIN8CSX2'; // Replace with your Alpha Vantage API key
    const apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${stockSymbol}&apikey=${apiKey}`;

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (data['Error Message']) {
            alert('Invalid stock symbol or API error.');
            return;
        }

        const timeSeries = data['Time Series (Daily)'];
        const dates = Object.keys(timeSeries).reverse();
        const prices = dates.map(date => parseFloat(timeSeries[date]['4. close']));

        renderChart(dates, prices);
        predictStockPrice(prices);
    } catch (error) {
        console.error('Error fetching stock data:', error);
    }
}

function renderChart(dates, prices) {
    const ctx = document.getElementById('stockChart').getContext('2d');

    if (stockChart) {
        stockChart.destroy();
    }

    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Stock Price',
                data: prices,
                borderColor: '#007bff',
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price (USD)'
                    }
                }
            }
        }
    });
}

function predictStockPrice(prices) {
    // Simple moving average prediction for demonstration
    const lastPrice = prices[prices.length - 1];
    const prediction = lastPrice + (Math.random() * 10 - 5); // Random prediction for demo
    document.getElementById('predictionResult').innerText = `Predicted Next Day Price: $${prediction.toFixed(2)}`;
}
