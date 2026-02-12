import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_stock_data(symbol):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=4*365)  # ~4 years
    df = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'),
                     end=end_date.strftime('%Y-%m-%d'), auto_adjust=True)
    return df

def calculate_drawdowns(prices):
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max

    # Max drawdown value and date
    min_drawdown = drawdown.min()
    if isinstance(min_drawdown, pd.Series):
       min_drawdown = float(min_drawdown.iloc[0])
    else:
       min_drawdown = float(min_drawdown)

    trough_date = drawdown.idxmin()
    if isinstance(trough_date, pd.Series):
        trough_date = trough_date.iloc[0]

    # Peak is max before the trough
    peak_date = prices.loc[:trough_date].idxmax()
    if isinstance(peak_date, pd.Series):
        peak_date = peak_date.iloc[0]

    # Get peak price, fallback if peak_date is missing in index
    peak_price = prices.get(peak_date, prices.asof(peak_date))

    # Recovery: when price recovers to or exceeds previous peak
    recovery_series = prices.loc[trough_date:]
    recovery_date = recovery_series[recovery_series >= peak_price]
    recovery_date = recovery_date.index[0] if not recovery_date.empty else None

    return drawdown, min_drawdown, peak_date, trough_date, recovery_date


def plot_drawdown(prices, drawdown, symbol, peak, trough):
    # Ensure drawdown is a 1D Series
    drawdown = drawdown.squeeze()  # Converts any multi-dimensional structures to 1D

    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax[0].plot(prices, label="Price", color='blue')
    ax[0].axvline(peak, color='green', linestyle='--', label='Peak')
    ax[0].axvline(trough, color='red', linestyle='--', label='Trough')
    ax[0].set_title(f"{symbol} Price")
    ax[0].legend()

    ax[1].plot(drawdown, label="Drawdown", color='orange')
    ax[1].fill_between(drawdown.index, drawdown, 0, color='orange', alpha=0.3)
    ax[1].axhline(0, color='gray', linestyle='--')
    ax[1].set_title(f"{symbol} Drawdown")
    ax[1].legend()

    plt.tight_layout()
    plt.show()


def main():
    symbol = input("Enter the stock symbol (e.g., AAPL, MSFT, TSLA): ").strip().upper()
    print(f"\nFetching data for: {symbol}")

    df = get_stock_data(symbol)

    if df.empty:
        print("No data found. Please check the symbol and try again.")
        return

    prices = df['Close'].dropna()
    drawdown, max_dd, peak, trough, recovery = calculate_drawdowns(prices)

    print(f"\n🔻 Maximum Drawdown for {symbol}: {float(max_dd):.2%}")

    print(f"📈 Peak Date: {peak.date()}")
    print(f"📉 Trough Date: {trough.date()}")
    if recovery:
        print(f"🔁 Recovery Date: {recovery.date()}")
        print(f"⏱️ Drawdown Duration: {(recovery - peak).days} days")
    else:
        print("⚠️ Stock has not yet recovered to previous peak.")

    plot_drawdown(prices, drawdown, symbol, peak, trough)

if __name__ == "__main__":
    main()
