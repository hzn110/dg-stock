import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="종목 추천",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ 종목 추천")

st.write(
    "최근 1년간의 수익률을 기준으로 주요 한국·미국 종목을 분석합니다."
)

STOCKS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "현대차": "005380.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "POSCO홀딩스": "005490.KS",
}

result = []

with st.spinner("종목 분석 중..."):

    for name, ticker in STOCKS.items():

        try:
            df = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if df.empty:
                continue

            # yfinance 버전별 대응
            if "Close" not in df.columns:
                continue

            close = df["Close"]

            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]

            close = close.dropna()

            if len(close) < 2:
                continue

            start_price = float(close.iloc[0])
            end_price = float(close.iloc[-1])

            return_pct = (
                (end_price - start_price)
                / start_price
                * 100
            )

            volatility = (
                close.pct_change()
                .std()
                * 100
            )

            result.append({
                "종목": name,
                "1년 수익률(%)": round(return_pct, 2),
                "변동성(%)": round(float(volatility), 2)
            })

        except Exception:
            continue

if len(result) == 0:
    st.error(
        "주가 데이터를 가져오지 못했습니다. requirements.txt에 yfinance가 포함되어 있는지 확인하세요."
    )
    st.stop()

result_df = pd.DataFrame(result)

result_df = result_df.sort_values(
    by="1년 수익률(%)",
    ascending=False
).reset_index(drop=True)

best_stock = result_df.iloc[0]

st.success(
    f"""
추천 종목: {best_stock['종목']}

최근 1년 수익률: {best_stock['1년 수익률(%)']}%
"""
)

st.subheader("🏆 전체 순위")

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("📈 TOP 5 추천 종목")

st.dataframe(
    result_df.head(5),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "※ 과거 수익률 기반 추천이며 투자 권유가 아닙니다."
)
