document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully!");

    // Dummy stock data
    const stockPrices = [
        { name: "AAPL", price: 150.25, change: "+1.2%" },
        { name: "GOOGL", price: 2800.50, change: "-0.5%" },
        { name: "TSLA", price: 900.30, change: "+2.1%" },
        { name: "AMZN", price: 3450.75, change: "-1.8%" }
    ];

    // Function to update stock ticker
    function updateStockTicker() {
        const tickerContainer = document.getElementById("stock-ticker");
        if (tickerContainer) {
            tickerContainer.innerHTML = stockPrices.map(stock =>
                `<span class="stock">${stock.name}: $${stock.price} (${stock.change})</span>`
            ).join(" | ");
        } else {
            console.log("Ticker container not found!");
        }
    }

    // Refresh stock prices every 5 seconds
    setInterval(() => {
        stockPrices.forEach(stock => {
            let randomChange = (Math.random() * 2 - 1).toFixed(2);
            stock.price = (parseFloat(stock.price) + parseFloat(randomChange)).toFixed(2);
            stock.change = (randomChange >= 0 ? `+${randomChange}%` : `${randomChange}%`);
        });
        updateStockTicker();
    }, 5000);

    // Run on page load
    updateStockTicker();
});
