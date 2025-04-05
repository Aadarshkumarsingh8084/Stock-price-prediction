const apiKey = "9SPII8ZJVIN8CSX2"; // Replace with your actual API key
// script.js
document.getElementById('predictButton').addEventListener('click', async () => {
    const stockSymbol = document.getElementById('stockSymbol').value.toUpperCase();
    const predictionDays = parseInt(document.getElementById('predictionDays').value);

    if (!stockSymbol) {
        alert('Please enter a stock symbol.');
        return;
    }

    try {
        const predictionData = await predictStock(stockSymbol, predictionDays);
        if(predictionData && predictionData.labels && predictionData.predictions){
            displayChart(predictionData.labels, predictionData.predictions, stockSymbol);
            displayResults(predictionData.predictions);
        } else {
            alert("Could not retrieve prediction data. Check the console for errors.");
        }

    } catch (error) {
        console.error('Error fetching prediction:', error);
        alert('An error occurred. Please try again later.');
    }
});

async function predictStock(symbol, days) {
    // Replace with your actual prediction logic (e.g., using an API or machine learning model)
    // This is a placeholder for demonstration purposes.
    // In a real project, you would use a backend service or a trained model.
    // For demonstration, we'll simulate some random data.

    const labels = [];
    const predictions = [];
    const today = new Date();

    for (let i = 0; i < days; i++) {
        const nextDay = new Date(today);
        nextDay.setDate(today.getDate() + i);
        labels.push(nextDay.toLocaleDateString());
        predictions.push(Math.random() * 100 + 100); // Simulate random stock prices
    }

    return { labels, predictions };
}

function displayChart(labels, predictions, symbol) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    if (window.myChart) {
        window.myChart.destroy(); // Destroy previous chart if it exists.
    }
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${symbol} Stock Price Prediction`,
                data: predictions,
                borderColor: 'blue',
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function displayResults(predictions) {
    const resultsDiv = document.getElementById('predictionResults');
    resultsDiv.innerHTML = '<h3>Predicted Prices:</h3>';
    predictions.forEach((price, index) => {
        resultsDiv.innerHTML += `<p>Day ${index + 1}: $${price.toFixed(2)}</p>`;
    });
}
