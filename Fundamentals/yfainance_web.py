import yfinance as yf

df = yf.download("RELIANCE.NS", start="2024-01-01", end="2024-02-01")
print(df)