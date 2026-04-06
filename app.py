import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="AI台股選股系統", layout="wide")

st.title("📊 AI台股選股系統 Ultimate")

# 投資模式
st.subheader("🧭 投資模式")

growth = st.checkbox("成長爆發型", value=True)
stable = st.checkbox("穩健投資型")

stocks = {
"2330.TW":"台積電",
"2317.TW":"鴻海",
"2454.TW":"聯發科",
"3017.TW":"奇鋐",
"2303.TW":"聯電",
"2382.TW":"廣達",
"3037.TW":"欣興"
}

ai_industry = [
"2330.TW","2454.TW","3017.TW","2382.TW"
]

results=[]

for ticker,name in stocks.items():

    try:

        df = yf.download(ticker, period="6mo", progress=False)

        if df.empty:
            continue

        df["MA5"]=df["Close"].rolling(5).mean()
        df["MA20"]=df["Close"].rolling(20).mean()

        latest=df.iloc[-1]

        close=float(latest["Close"])
        ma5=latest["MA5"]
        ma20=latest["MA20"]

        score=0
        signal="觀察"

        if pd.notna(ma5) and pd.notna(ma20):

            if close>ma20:
                score+=20

            if close>ma5:
                score+=10

            if close>ma20 and close>ma5:
                signal="📈 建議進場"

        # AI產業加分
        if ticker in ai_industry and growth:
            score+=10

        # 穩健型調整
        if stable:
            score+=5

        results.append({
        "股票":name,
        "代碼":ticker,
        "現價":round(close,2),
        "評分":score,
        "訊號":signal
        })

    except:
        continue

df_result=pd.DataFrame(results)

st.subheader("📈 AI選股結果")

if df_result.empty:
    st.warning("目前沒有可顯示的股票資料")
else:
    st.dataframe(df_result.sort_values("評分",ascending=False))

# 法人資金
st.subheader("🏦 三大法人資金流")

flow_data={
"股票":["台積電","奇鋐","聯電"],
"外資":["連續買超3天","買超","買超"],
"投信":["買超","買超","-"],
"自營商":["-","買超","-"]
}

st.table(pd.DataFrame(flow_data))

# ETF現金流
st.subheader("💰 ETF現金流")

etf1=st.number_input("00878 投入金額",0,10000000,100000)
etf2=st.number_input("00919 投入金額",0,10000000,100000)
etf3=st.number_input("0056 投入金額",0,10000000,100000)

annual_income=etf1*0.06+etf2*0.07+etf3*0.05
monthly_income=annual_income/12

st.success(f"預估每年股息：{round(annual_income)} 元")
st.success(f"預估每月現金流：{round(monthly_income)} 元")

# 退休現金流
st.subheader("🏝️ 退休現金流規劃")

target=st.number_input("每月想領多少",0,100000,20000)

need_asset=target*12/0.06

st.info(f"約需要資產：{round(need_asset)} 元")
