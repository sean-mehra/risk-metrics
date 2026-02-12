import yfinance as yf
import numpy as np
import pandas as pd

def safe_float_conversion(value):
    """Safely convert various numeric types to float"""
    if hasattr(value, 'iloc'):  # For pandas Series
        return float(value.iloc[0])
    elif hasattr(value, 'item'):  # For numpy arrays
        return float(value.item())
    elif isinstance(value, (np.ndarray, list)) and len(value) == 1:
        return float(value[0])
    return float(value)

def calculate_sortino_ratio(ticker, years=5, risk_free_rate=0.0):
    try:
        # Download data
        data = yf.download(ticker, period=f"{years}y", auto_adjust=True)
        
        # Data validation
        if data.empty or 'Close' not in data.columns:
            return np.nan
        
        # Calculate returns
        daily_returns = data['Close'].pct_change().dropna()
        if len(daily_returns) < 5:  # Minimum 5 days of data
            return np.nan
        
        # Calculate components using safe conversion
        avg_return = safe_float_conversion(daily_returns.mean())
        downside_returns = daily_returns[daily_returns < 0]
        
        if len(downside_returns) < 3:  # Minimum 3 downside days
            return np.nan
        
        # Calculate and convert downside deviation
        downside_std = safe_float_conversion(downside_returns.std(ddof=0))
        
        # Final checks
        if np.isnan(downside_std) or downside_std == 0.0:
            return np.nan
        
        # Calculate ratio
        sortino_ratio = (avg_return - risk_free_rate) / downside_std
        return sortino_ratio * np.sqrt(252)  # Annualized
        
    except Exception as e:
        print(f"Debug error for {ticker}: {str(e)}")
        return np.nan

# Get input and process
tickers = input("Enter stock tickers separated by commas (e.g. AAPL,MSFT,SPY): ").split(",")

for ticker in [t.strip().upper() for t in tickers if t.strip()]:
    ratio = calculate_sortino_ratio(ticker)
    if np.isnan(ratio):
        print(f"{ticker}: Sortino Ratio could not be calculated.")
    else:
        print(f"{ticker}: Sortino Ratio 5-year Data = {ratio:.2f}")