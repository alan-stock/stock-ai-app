import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="AI台股選股系統 V5", layout="wide")

st.title("📊 AI台股選股系統 V5")

mode = st.radio(
    "選擇投資模式",
    ["B 成長爆發型", "A 穩健投資型"]
)

stocks = {
    "2330.TW": "台積電",
    "2317.TW": "鴻海",
    "2454.TW": "聯發科",
    "3017.TW": "奇鋐",
    "2303.TW": "聯電",
    "2382.TW": "廣達",
    "3037.TW": "欣興"
}

results = []

for ticker, name in stocks.items():

    try:
        df = yf.download(ticker, period="6mo", progress=False)

        if df.empty:
            continue

        df["MA5"] = df["Close"].rolling(5).mean()
        df["MA20"] = df["Close"].rolling(20).mean()

        latest = df.iloc[-1]

        close = float(latest["Close"])
        ma5 = latest["MA5"]
        ma20 = latest["MA20"]

        score = 0
        signal = "觀察"

        if pd.notna(ma5) and pd.notna(ma20):

            if close > ma20:
                score += 20

            if close > ma5:
                score += 10

            if close > ma20 and close > ma5:
                signal = "📈 建議進場"

        results.append({
            "股票": name,
            "代碼": ticker,
            "現價": round(close, 2),
            "評分": score,
            "訊號": signal
        })

    except:
        continue

df_result = pd.DataFrame(results)

st.subheader("📈 AI選股結果")
st.dataframe(df_result.sort_values("評分", ascending=False))

st.subheader("💰 ETF現金流")

etf1 = st.number_input("00878 投入金額", 0, 10000000, 100000)
etf2 = st.number_input("00919 投入金額", 0, 10000000, 100000)
etf3 = st.number_input("0056 投入金額", 0, 10000000, 100000)

income = (etf1 * 0.06 + etf2 * 0.07 + etf3 * 0.05) / 12

st.success(f"預估每月現金流：{round(income)} 元")
