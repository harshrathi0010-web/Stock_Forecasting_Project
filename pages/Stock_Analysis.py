import streamlit as st
import yfinance as yf 
import plotly.graph_objects as go
import datetime
import pandas as pd
from pages.utils.plotly_figure import plotly_table,close_chart,candlestick,RSI,MACD


def moving_average_chart(dataframe, period):
    chart_data = dataframe.copy()
    chart_data["MA20"] = chart_data["Close"].rolling(window=20).mean()
    chart_data["MA50"] = chart_data["Close"].rolling(window=50).mean()
    chart_data["MA200"] = chart_data["Close"].rolling(window=200).mean()

    last_date = chart_data.index[-1]
    if period == "5d":
        cutoff = last_date - pd.Timedelta(days=5)
    elif period == "1mo":
        cutoff = last_date - pd.DateOffset(months=1)
    elif period == "6mo":
        cutoff = last_date - pd.DateOffset(months=6)
    elif period == "ytd":
        cutoff = last_date.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif period == "1y":
        cutoff = last_date - pd.DateOffset(years=1)
    elif period == "5y":
        cutoff = last_date - pd.DateOffset(years=5)
    else:
        cutoff = chart_data.index[0]

    chart_data = chart_data.loc[chart_data.index >= cutoff].reset_index()
    chart_data.rename(columns={chart_data.columns[0]: "Date"}, inplace=True)

    figure = go.Figure()
    for column, label, color in (
        ("Close", "Close", "black"),
        ("MA20", "20-day average", "#0078ff"),
        ("MA50", "50-day average", "orange"),
        ("MA200", "200-day average", "red"),
    ):
        figure.add_trace(
            go.Scatter(
                x=chart_data["Date"],
                y=chart_data[column],
                mode="lines",
                name=label,
                line={"color": color, "width": 2},
            )
        )

    figure.update_layout(
        height=500,
        margin={"l": 0, "r": 20, "t": 20, "b": 0},
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
    )
    return figure


# Set page config
st.set_page_config(
    page_title="Stock_Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

st.title("Stock Analysis")
today=datetime.date.today()

col1,col2,col3=st.columns(3)

with col1:
    ticker=st.text_input("STOCK TICKER","TSLA")

with col2:
    start_date=st.date_input("Choose Start Date",datetime.date(today.year-1,today.month,today.day))


with col3:
    end_date=st.date_input("Choose end date",datetime.date(today.year,
    today.month,today.day))


st.subheader(ticker)

stock=yf.Ticker(ticker)

st.write(stock.info["longBusinessSummary"])
st.write("**sector:**",stock.info["sector"])
st.write("Full time employee:**",stock.info["fullTimeEmployees"])
st.write("**website**",stock.info["website"])

col1,col2=st.columns(2)

with col1:
    df=pd.DataFrame(index=["Market Cap","Beta","EPS","PE Ratio"])
    df['']=[stock.info["marketCap"],stock.info["beta"],stock.info["trailingEps"],stock.info["trailingPE"]]

    fig_df=plotly_table(df)

    st.plotly_chart(fig_df,use_container_width=True)

with col2:
    df=pd.DataFrame(index=["Quick Ratio","Revenue per share","Profit Margins","Debt to Equity","Return on Equity"])

    df['']=[stock.info["quickRatio"],stock.info["revenuePerShare"],stock.info["profitMargins"],stock.info["debtToEquity"],stock.info["returnOnEquity"]]

    fig_df=plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

data=yf.download(ticker,start=start_date,end=end_date)

col1,col2,col3=st.columns(3)

close = data["Close"]
if isinstance(close, pd.DataFrame):
    close = close[ticker]

daily_change = close.iloc[-1] - close.iloc[-2]

col1.metric(
    "Daily Changes",
    f"{close.iloc[-1]:.2f}",
    f"{daily_change:.2f}",
)

last_10_df=data.tail(10).sort_index(ascending=False).round(3)
fig_df=plotly_table(last_10_df)

st.write("#### Historical Data (last 10 Days)")
st.plotly_chart(fig_df,use_container_width=True)


col1,col2,col3,col4,col5,col6,col7=st.columns(7)

num_period="1y"

with col1:
    if st.button("5D"):
        num_period="5d"

with col2:
    if st.button("1M"):
        num_period="1mo"

with col3:
    if st.button("6M"):
        num_period="6mo"

with col4:
    if st.button("YTD"):
        num_period="ytd"

with col5:
    if st.button("1Y"):
        num_period="1y"

with col6:
    if st.button("5Y"):
        num_period="5y"

with col7:
    if st.button("MAX"):
        num_period="max"


col1,col2,col3=st.columns(3)

with col1:
    chart_type=st.selectbox('',('Candle','Line'))

with col2:
    if chart_type=="Candle":
     
   

        indicators=st.selectbox('',("RSI","MACD"))
    else: 

        indicators=st.selectbox('',("RSI","Moving Average","MACD"))



data1 = yf.Ticker(ticker).history(period="max")
if data1.empty:
    st.error(f"No historical price data was found for {ticker}. Check the ticker and try again.")
    st.stop()

if chart_type == "Candle" and indicators == "RSI":
    st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
    st.plotly_chart(RSI(data1, num_period), use_container_width=True)
elif chart_type == "Candle" and indicators == "MACD":
    st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
    st.plotly_chart(MACD(data1, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "RSI":
    st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
    st.plotly_chart(RSI(data1, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "Moving Average":
    st.plotly_chart(moving_average_chart(data1, num_period), use_container_width=True)
elif chart_type == "Line" and indicators == "MACD":
    st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
    st.plotly_chart(MACD(data1, num_period), use_container_width=True)












                                                           
