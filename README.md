# Simple Asynchronous Crypto Parser
The parser gets the data about cryptocurrencies from three markets - Binance, Kucoin and Bybit. It looks for the best margin (max - min) sum for each cryptocurrency, and prints these found margins in the terminal.

## Key Features in Code
- The market clients are divided into classes
- Easy to add one more client for market API
- Most of general errors are catched
- Fully asynchronous requests
- Dialects (full crypto symbols & short crypto symbols supported), each market client decides which dialect to use.

## Installation
1. Clone the repository using `git clone`
2. Make a virtual environment in the repository folder, using `python -m venv .venv`, and activate it.
3. Install the necessary dependencies:
   ```python
   pip install httpx colorama pydantic
   ```
## Usage
1. Open the `settings.py` file and set the cryptocurrencies symbols you would like to check in the `CHECK_CRYPTO` property. Please write the **full symbol** seperated by backslash (/), like BTC/USDT or ETH/USDT, and seperate these pairs by comma if you want to add more. Even if you want to check only BTC, without specific additional currency, you must write a full symbol because of each market differently accepts crypto-symbols.
2. Run the application using `python -m app.main`. After each 60 seconds, there will be printed the following information in the terminal:
   - The market it's required to buy on (green color)
   - The market it's required to sell on (red color)
   - The difference between buying and selling as a sum and a percent. (also green)
  3. If you have written the wrong crypto symbol, the parser will not work and will print an error message.