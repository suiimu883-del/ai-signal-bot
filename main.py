from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import random

app = FastAPI()

# -----------------------------
# SETTINGS
# -----------------------------
TARGET_WIN_RATE = 90

# Demo history
results = []


# -----------------------------
# SIGNAL ENGINE
# -----------------------------
def generate_signal():
    ema = random.randint(0, 20)
    rsi = random.randint(0, 20)
    macd = random.randint(0, 20)
    trend = random.randint(0, 20)
    support_resistance = random.randint(0, 20)

    score = (
        ema
        + rsi
        + macd
        + trend
        + support_resistance
    )

    if score >= 75:
        signal = "CALL"
    elif score <= 25:
        signal = "PUT"
    else:
        signal = "NO SIGNAL"

    return {
        "signal": signal,
        "score": score
    }


# -----------------------------
# RECORD RESULT
# -----------------------------
def add_result(win: bool):
    results.append("WIN" if win else "LOSS")


def statistics():
    total = len(results)
    wins = results.count("WIN")
    losses = results.count("LOSS")

    if total == 0:
        win_rate = 0
    else:
        win_rate = round((wins / total) * 100, 2)

    return total, wins, losses, win_rate


# -----------------------------
# DASHBOARD
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():

    signal = generate_signal()

    total, wins, losses, win_rate = statistics()

    if win_rate >= TARGET_WIN_RATE:
        status = "🔥 TARGET ACHIEVED"
    else:
        status = "⚠️ TARGET NOT ACHIEVED"

    signal_color = "#00ff88"

    if signal["signal"] == "PUT":
        signal_color = "#ff4444"

    if signal["signal"] == "NO SIGNAL":
        signal_color = "#ffaa00"

    return f"""
<!DOCTYPE html>
<html>

<head>

<title>AI Market Signal Bot</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {{
    margin:0;
    background:#080808;
    color:white;
    font-family:Arial;
}}

.container {{
    max-width:450px;
    margin:auto;
    padding:20px;
}}

.card {{
    background:#151515;
    padding:22px;
    margin-top:15px;
    border-radius:18px;
    box-shadow:0 0 15px #000;
}}

.title {{
    text-align:center;
    font-size:28px;
    font-weight:bold;
}}

.signal {{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:{signal_color};
    margin:25px 0;
}}

.score {{
    text-align:center;
    font-size:22px;
}}

.stats {{
    display:flex;
    justify-content:space-between;
    margin-top:15px;
}}

.stat {{
    text-align:center;
    width:30%;
}}

.number {{
    font-size:25px;
    font-weight:bold;
}}

button {{
    width:100%;
    padding:15px;
    margin-top:20px;
    border:0;
    border-radius:12px;
    background:#ffffff;
    color:#000;
    font-size:18px;
    font-weight:bold;
}}

.target {{
    text-align:center;
    font-size:20px;
    margin-top:15px;
}}

.warning {{
    color:#aaa;
    font-size:13px;
    text-align:center;
    margin-top:25px;
}}

</style>

</head>


<body>

<div class="container">

<div class="title">
🤖 AI MARKET SIGNAL
</div>


<div class="card">

<div class="signal">
{signal["signal"]}
</div>

<div class="score">
Confidence Score:
<b>{signal["score"]}%</b>
</div>

</div>


<div class="card">

<h2>📊 Performance</h2>

<div class="stats">

<div class="stat">
<div class="number">{total}</div>
Total
</div>

<div class="stat">
<div class="number">{wins}</div>
Wins
</div>

<div class="stat">
<div class="number">{losses}</div>
Losses
</div>

</div>


<div class="target">

Actual Win Rate:
<b>{win_rate}%</b>

<br><br>

Target:
<b>{TARGET_WIN_RATE}%</b>

<br><br>

{status}

</div>

</div>


<div class="card">

<h3>🧠 Strategy</h3>

<p>EMA</p>
<p>RSI</p>
<p>MACD</p>
<p>Trend</p>
<p>Support / Resistance</p>

</div>


<button onclick="location.reload()">
🔄 Generate New Signal
</button>


<div class="warning">

⚠️ Demo / Paper Trading Only<br>
No guaranteed profit or win rate.

</div>

</div>

</body>

</html>
"""


# -----------------------------
# API
# ----------------
