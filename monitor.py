import numpy as np
import yfinance as yf
import pandas as pd
import signals
import options
from tickers import IBOVESPA

_socketio = None


def init(socketio_instance):
    global _socketio
    _socketio = socketio_instance


def _historical_vol(ticker: str) -> float:
    df = yf.download(ticker, period="30d", interval="1d", progress=False, auto_adjust=True)
    if df is None or len(df) < 5:
        return 0.30
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    log_returns = np.log(close / close.shift(1)).dropna()
    return float(log_returns.std() * np.sqrt(252))


def run_scan():
    print("[monitor] Iniciando varredura...")
    for ticker in IBOVESPA:
        try:
            signal = signals.check(ticker)
            if signal:
                vol = _historical_vol(ticker)
                payload = options.price(signal, vol)
                print(f"[monitor] Sinal: {payload}")
                if _socketio:
                    _socketio.emit("new_signal", payload)
        except Exception as e:
            print(f"[monitor] Erro em {ticker}: {e}")
    print("[monitor] Varredura concluída.")
