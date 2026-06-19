import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


# =========================
# CONFIG
# =========================

PAIRS = [
    ("MA", "V"),
    ("AMZN", "META"),
    ("ICE", "V"),
    ("BARC.L", "LLOY.L"),
]

START_DATE = "2018-01-01"
ROLLING_WINDOW = 252

ENTRY_Z = -2.0
EXIT_Z = -0.5
STOP_Z = -3.5

EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "your_email@gmail.com"
EMAIL_APP_PASSWORD = "your_gmail_app_password"


# =========================
# FUNCTIONS
# =========================

def calculate_hedge_ratio(y, x):
    model = sm.OLS(y, sm.add_constant(x)).fit()
    return model.params.iloc[1]


def calculate_half_life(spread):
    spread = spread.dropna()
    lagged = spread.shift(1).dropna()
    delta = spread.diff().dropna()
    lagged = lagged.loc[delta.index]

    model = sm.OLS(delta, sm.add_constant(lagged)).fit()
    beta = model.params.iloc[1]

    if beta >= 0:
        return np.nan

    return -np.log(2) / beta


def analyse_pair(pair_1, pair_2):
    prices = yf.download(
        [pair_1, pair_2],
        start=START_DATE,
        auto_adjust=True,
        progress=False
    )["Close"]

    prices = prices.dropna()
    prices.columns = [pair_1, pair_2]

    hedge_ratio = calculate_hedge_ratio(
        prices[pair_1],
        prices[pair_2]
    )

    spread = prices[pair_1] - hedge_ratio * prices[pair_2]

    rolling_mean = spread.rolling(ROLLING_WINDOW).mean()
    rolling_std = spread.rolling(ROLLING_WINDOW).std()

    zscore = (spread - rolling_mean) / rolling_std

    current_z = zscore.iloc[-1]
    previous_z = zscore.iloc[-2]

    half_life = calculate_half_life(spread)

    if current_z <= STOP_Z:
        signal = "STOP LOSS"
    elif current_z <= ENTRY_Z and previous_z > ENTRY_Z:
        signal = "NEW ENTRY"
    elif current_z >= EXIT_Z and previous_z < EXIT_Z:
        signal = "EXIT / TAKE PROFIT"
    elif current_z <= ENTRY_Z:
        signal = "ENTRY ZONE"
    else:
        signal = "NO ACTION"

    return {
        "pair": f"{pair_1}/{pair_2}",
        "hedge_ratio": round(hedge_ratio, 4),
        "previous_z": round(previous_z, 2),
        "current_z": round(current_z, 2),
        "z_change": round(current_z - previous_z, 2),
        "half_life_days": round(half_life, 2),
        "signal": signal,
        "model_trade": f"Long {pair_1}, Short {pair_2}" if current_z < 0 else f"Short {pair_1}, Long {pair_2}"
    }


def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_APP_PASSWORD)
        server.send_message(msg)


# =========================
# RUN MONITOR
# =========================

results = []

for pair_1, pair_2 in PAIRS:
    try:
        results.append(analyse_pair(pair_1, pair_2))
    except Exception as e:
        results.append({
            "pair": f"{pair_1}/{pair_2}",
            "signal": "ERROR",
            "error": str(e)
        })

df = pd.DataFrame(results)

alerts = df[df["signal"].isin([
    "NEW ENTRY",
    "EXIT / TAKE PROFIT",
    "STOP LOSS",
    "ENTRY ZONE"
])]

report = f"""
Pair Trading Monitor
Run time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{df.to_string(index=False)}
"""

print(report)

if len(alerts) > 0:
    send_email(
        subject="Pair Trading Alert",
        body=report
    )
