import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="글로벌 주식 비교기",
    page_icon="📈",
    layout="wide"
)

st.title("📈 한국·미국 주식 수익률 비교")

stocks = {
    # 미국
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",

    # 한국
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "현대차": "005380.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "POSCO홀딩스": "005490.KS",
}

period_map = {
    "1개월": "1mo",
    "3개월": "3mo",
    "6개월": "6mo",
    "1년": "1y",
    "2년": "2y",
    "5년": "5y"
}

col1, col2 = st.columns(2)

with col1:
    selected = st.multiselect(
        "종목 선택",
        list(stocks.keys()),
        default=["Apple", "삼성전자"]
    )

with col2:
    period_kor = st.selectbox(
        "기간 선택",
        list(period_map.keys()),
        index=3
    )

period = period_map[period_kor]

if selected:

    tickers = [stocks[name] for name in selected]

    with st.spinner("주가 데이터 불러오는 중..."):
        data = yf.download(
            tickers=tickers,
            period=period,
            auto_adjust=True,
            progress=False
        )

    if len(tickers) == 1:
        close = pd.DataFrame(data["Close"])
        close.columns = selected
    else:
        close = data["Close"]
        close.columns = selected

    close = close.dropna()

    normalized = close / close.iloc[0] * 100

    returns = (
        (close.iloc[-1] / close.iloc[0] - 1) * 100
    ).round(2)

    st.subheader("📊 누적 수익률 비교")

    fig = px.line(normalized)

    fig.update_layout(
        height=600,
        xaxis_title="날짜",
        yaxis_title="기준가 (100)",
        legend_title="종목"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 수익률 순위")

    result_df = pd.DataFrame({
        "종목": returns.index,
        "수익률(%)": returns.values
    })

    result_df = result_df.sort_values(
        "수익률(%)",
        ascending=False
    ).reset_index(drop=True)

    st.dataframe(
        result_df,
        use_container_width=True
    )

    st.success(
        f"최고 수익률 종목: "
        f"{result_df.iloc[0]['종목']} "
        f"({result_df.iloc[0]['수익률(%)']}%)"
    )

    st.subheader("💰 실제 주가 그래프")

    for stock in close.columns:

        st.markdown(f"### {stock}")

        fig_stock = px.line(
            close,
            y=stock
        )

        fig_stock.update_layout(
            height=400,
            xaxis_title="날짜",
            yaxis_title="주가",
            showlegend=False
        )

        st.plotly_chart(
            fig_stock,
            use_container_width=True
        )

else:
    st.info("비교할 종목을 선택하세요.")
    
