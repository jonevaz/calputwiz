import pandas as pd
import yfinance as yf
import ta
from datetime import datetime
import pytz


def check(ticker: str) -> dict | None:
    df = yf.download(ticker, period="5d", interval="5m", progress=False, auto_adjust=True)
    if df is None or len(df) < 35:
        return None

    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.dropna()

    if len(close) < 35:
        return None

    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    macd_ind = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
    hist = macd_ind.macd_diff()
    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)

    current_price = float(close.iloc[-1])
    current_rsi = float(rsi.iloc[-1])
    prev_hist = float(hist.iloc[-2])
    curr_hist = float(hist.iloc[-1])
    lower_band = float(bb.bollinger_lband().iloc[-1])
    upper_band = float(bb.bollinger_hband().iloc[-1])

    tz = pytz.timezone("America/Sao_Paulo")
    timestamp = datetime.now(tz).strftime("%d/%m/%Y %H:%M")

    # CALL: oversold + MACD bullish crossover + near lower Bollinger Band
    if (
        current_rsi < 35
        and prev_hist < 0 and curr_hist >= 0
        and current_price <= lower_band * 1.01
    ):
        return {"ticker": ticker.replace(".SA", ""), "type": "CALL", "price": current_price, "timestamp": timestamp}

    # PUT: overbought + MACD bearish crossover + near upper Bollinger Band
    if (
        current_rsi > 65
        and prev_hist > 0 and curr_hist <= 0
        and current_price >= upper_band * 0.99
    ):
        return {"ticker": ticker.replace(".SA", ""), "type": "PUT", "price": current_price, "timestamp": timestamp}

    return None
