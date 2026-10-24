import streamlit as st

st.set_page_config(
    page_title="Trading Ap",
    page_icon="chart_with_downward_trend",
    layout="wide"
)

st.title("Trading Guide App")

st.header("we provide the greatest plateform for collect all information prior to investigate in stocks")

st.image("app_png.webp")

st.markdown("## We provide the following services:")

st.markdown("### :one: Stock Information")
st.write("Through this page you can see all the information about stock")


st.markdown("### :two: Stock Prediction")
st.write("You can explore the 30 days predicted value on historical data and advanced forecasting models")

st.markdown("### :three: CAPM return ")
st.write("Discover how the Capital Assest Pricing Model (CAPM) work calculate the expected return of different stocks based on the its risk")

st.markdown("### :four: CAPM beta")
st.write("Calculates Beta and Expected return for Individual Stocks")


