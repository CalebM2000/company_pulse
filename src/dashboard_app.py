import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from prophet import Prophet
from streamlit_autorefresh import st_autorefresh

# -----------------------------------------------------------------------------
# Page setup
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Company Pulse Dashboard", layout="wide")
st.title("🏢 Company Pulse – Real-Time BI Dashboard")

# 🔁 Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="data_refresh")

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data_path = Path("data/live_data.jsonl")

if not data_path.exists() or data_path.stat().st_size == 0:
    st.warning("Waiting for live data...")
    st.stop()

# Read JSONL stream into DataFrame
with open(data_path) as f:
    records = [json.loads(line) for line in f]
if not records:
    st.warning("No records yet. Waiting for updates…")
    st.stop()

df = pd.DataFrame(records)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -----------------------------------------------------------------------------
# KPI metrics
# -----------------------------------------------------------------------------
k1, k2, k3 = st.columns(3)
k1.metric("Avg Sales ($)", f"{df.sales.mean():,.2f}")
k2.metric("Avg Transactions", f"{df.transactions.mean():.0f}")
k3.metric("Avg Sentiment", f"{df.sentiment.mean():.2f}")

# -----------------------------------------------------------------------------
# Recent trends chart
# -----------------------------------------------------------------------------
st.subheader("📈 Recent Trends")
fig = px.line(
    df,
    x="timestamp",
    y=["sales", "sentiment"],
    title="Sales & Sentiment Over Time",
    labels={"value": "Metric Value", "timestamp": "Time"},
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Prophet forecast – next hour of sales
# -----------------------------------------------------------------------------
if len(df) > 10:  # need enough data to train
    st.subheader("🔮 Forecast – Next Hour of Sales")

    forecast_df = df[["timestamp", "sales"]].rename(columns={"timestamp": "ds", "sales": "y"})
    model = Prophet(daily_seasonality=True)
    model.fit(forecast_df)

    # predict next hour (12 × 5 min steps)
    future = model.make_future_dataframe(periods=12, freq="5min")
    forecast = model.predict(future)

    # combine actual + forecast
    fig2 = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Forecasted Sales (Next Hour)",
        labels={"ds": "Time", "yhat": "Predicted Sales"},
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Need more data points to generate a forecast yet.")
