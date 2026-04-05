import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="AI台股選股系統V5",layout="wide")

st.title("📊 AI台股選股系統 V5")

mode = st.radio(
"選擇投資模式",
["B 成長爆發型","A 穩健投資型"]
)

st.write("目前模式:",mode)

stocks = {
"2330.TW":"台積電",
"2317.TW":"鴻海",
"2454.TW":"聯發科",
"3017.TW":"奇鋐",
"2303.TW":"聯電",
"2382.TW":"廣達",
"3037.TW":"欣興"
}

ai_industry=[
"2330.TW","2454.TW","3017.TW","2382.TW"
]

results=[]

progress=st.progress(0)

for i,(ticker,name) in enumerate(stocks.items()):

    try:

        df=yf.download(ticker,period="6mo",progress=False)

        if df.empty
