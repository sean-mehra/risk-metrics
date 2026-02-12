import numpy as np
import pandas as pd
import yfinance as yf

def download_stock_data(symbol, years=3):
    """Download historical stock data from Yahoo Finance."""
    try:
        end_date = pd.Timestamp.today()
        start_date = end_date - pd.DateOffset(years=years)
        stock_data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)  # Auto-adjust prices
        
        if stock_data.empty:
            print(f"Failed to retrieve data for {symbol}. Please check the stock symbol and try again.")
            return None
        
        return stock_data['Close']  # Use 'Close' instead of 'Adj Close'
    
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

def calculate_cvar(returns, confidence_level=0.95):
    """Calculate Conditional Value at Risk (CVaR)."""
    if returns.empty:
        print("No return data available. Cannot compute CVaR.")
        return None, None

    var_threshold = np.percentile(returns, (1 - confidence_level) * 100)
    cvar = returns[returns <= var_threshold].mean()

    return float(var_threshold), float(cvar)  # Ensure these are floats

def main():
    stock_symbol = input("Enter stock symbol: ").upper()
    stock_prices = download_stock_data(stock_symbol)

    if stock_prices is None:
        return

    returns = stock_prices.pct_change().dropna()

    if returns.empty:
        print("No valid return data. Cannot compute CVaR.")
        return

    var_95, cvar_95 = calculate_cvar(returns, confidence_level=0.95)

    if var_95 is not None and cvar_95 is not None:
    	print(f"Stock: {stock_symbol}")
    	print(f"95% VaR: {var_95*100:.2f}%")
    	print(f"95% CVaR: {cvar_95*100:.2f}%")  # No more TypeError

if __name__ == "__main__":
    main()
