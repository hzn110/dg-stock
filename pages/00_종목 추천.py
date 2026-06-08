import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="종목 추천",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ 종목 추천")

stocks = {
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

with st.spinner("데이터 분석 중..."):

    result = []

    for name, ticker in stocks.items():

        try:
            df = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if len(df) < 30:
                continue

            start_price = float(df["Close"].iloc[0])
            end_price = float(df["Close"].iloc[-1])

            return_pct = (
                (end_price - start_price)
                / start_price
                * 100
            )

            volatility = (
                df["Close"]
                .pct_change()
                .std()
                * 100
            )

            result.append({
                "종목": name,
                "1년 수익률(%)": round(return_pct, 2),
                "변동성": round(float(volatility), 2)
            })

        except:
            pass

result_df = pd.DataFrame(result)

result_df = result_df.sort_values(
    "1년 수익률(%)",
    ascending=False
)

st.subheader("🏆 최근 1년 수익률 순위")

st.dataframe(
    result_df,
    use_container_width=True
)

if not result_df.empty:

    best = result_df.iloc[0]

    st.success(
        f"""
        추천 종목: {best['종목']}

        최근 1년 수익률:
        {best['1년 수익률(%)']}%
        """
    )

st.subheader("📈 상위 5개 추천")

st.dataframe(
    result_df.head(5),
    use_container_width=True
)

st.caption(
    "※ 단순 과거 수익률 기반 추천이며 투자 권유가 아닙니다."
)
