import math
from datetime import date, timedelta
from scipy.stats import norm

SELIC_RATE = 0.105  # 10.5% a.a.


def _next_b3_expiry() -> date:
    """Returns the nearest upcoming B3 monthly expiry (3rd Friday), at least 7 days out."""
    today = date.today()
    for offset in range(4):
        year = today.year + (today.month + offset - 1) // 12
        month = (today.month + offset - 1) % 12 + 1
        first_day = date(year, month, 1)
        days_to_friday = (4 - first_day.weekday()) % 7
        third_friday = first_day + timedelta(days=days_to_friday + 14)
        if third_friday >= today + timedelta(days=7):
            return third_friday
    return today + timedelta(days=21)


def _black_scholes(S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "CALL":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def price(signal: dict, hist_vol: float) -> dict:
    S = signal["price"]
    option_type = signal["type"]

    K = round(S * 1.03, 2) if option_type == "CALL" else round(S * 0.97, 2)
    expiry = _next_b3_expiry()
    T = (expiry - date.today()).days / 365.0

    premium = _black_scholes(S, K, T, SELIC_RATE, hist_vol, option_type)

    return {
        **signal,
        "strike": round(float(K), 2),
        "premium": round(float(premium), 2),
        "expiry": expiry.strftime("%d/%m/%Y"),
        "current_price": round(float(S), 2),
        "volatility": round(float(hist_vol) * 100, 1),
    }
