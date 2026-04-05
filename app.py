import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📊 AI台股選股系統 V5")

mode = st.radio(
    "選擇投資模式",
    ["B 成長爆發型","A 穩健投資型"]
)

stocks = [
"2330.TW","2317.TW","2454.TW","3017.TW",
"2303.TW","2382.TW","3037.TW"
]

data=[]

for s in stocks:

    df = yf.download(s, period="6mo", progress=False)

    if df.empty:
        continue

    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA20"] = df["Close"].rolling(20).mean()

    latest = df.iloc[-1]

    close = float(latest["Close"])
    ma5 = float(latest["MA5"]) if not pd.isna(latest["MA5"]) else None
    ma20 = float(latest["MA20"]) if not pd.isna(latest["MA20"]) else None

    signal = "觀察"

    if ma5 and ma20:
        if close > ma20 and close > ma5:
            signal = "📈 可考慮進場"

    data.append({
        "股票": s,
        "現價": round(close,2),
        "訊號": signal
    })

df = pd.DataFrame(data)

st.subheader("AI選股結果")

st.dataframe(df)

st.subheader("ETF現金流計算")

etf1 = st.number_input("00878 投入金額",0,10000000,100000)
etf2 = st.number_input("00919 投入金額",0,10000000,100000)
etf3 = st.number_input("0056 投入金額",0,10000000,100000)

income = (etf1*0.06 + etf2*0.07 + etf3*0.05) / 12

st.success(f"預估每月現金流：{round(income)} 元")
