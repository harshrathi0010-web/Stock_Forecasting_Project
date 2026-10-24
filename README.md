# Stock Forecasting Project

## The problem

Looking into a stock often means switching between different sources to find its
price history, company information, and indicators. This project brings several
of those research tools together in one small web app. It is intended to make
exploring stock data and a basic forecast more convenient; it is not a trading
platform or a source of investment advice.

## How the app helps

The app is built with Streamlit and gets market data from Yahoo Finance through
`yfinance`. It currently has two interactive pages:

- **Stock Analysis** — Enter a ticker and date range to view company details,
  selected financial statistics, recent prices, and historical charts. Charts
  include line and candlestick views, along with RSI, MACD, and moving averages.
  The available date ranges include 5 days, 1 month, 6 months, year to date,
  1 year, 5 years, and maximum history.
- **Stock Prediction** — View a forecast of the next 30 model steps based on
  recent closing prices. The page applies a 7-observation rolling mean, checks
  for stationarity with the Augmented Dickey-Fuller test, scales the data, and
  fits an ARIMA model. It also displays a basic RMSE score.

The prediction is experimental. It is generated from historical data and should
not be treated as a reliable indication of future market performance.

## Project structure

```text
.
├── Trading_App.py              # Streamlit home page and app entry point
├── app_png.webp                # Image displayed on the home page
└── pages/
    ├── Stock_Analysis.py       # Company information and historical charts
    ├── Prediction.py           # Forecast interface
    └── utils/
        ├── model_train.py      # Data preparation, ARIMA, scaling, evaluation
        ├── __init__.py         # Marks utils as a Python package
        └── plotly_figure.py    # Plotly tables and chart helpers
```

## Requirements

- Python 3.10 or newer
- An internet connection to retrieve data from Yahoo Finance

The project does not currently include a dependency lockfile or
`requirements.txt`. Install the packages used by the app with:

```bash
python -m pip install streamlit yfinance pandas numpy plotly python-dateutil statsmodels scikit-learn
```

On Windows, if `python` is not available in PowerShell, use the Python launcher:

```powershell
py -m pip install streamlit yfinance pandas numpy plotly python-dateutil statsmodels scikit-learn
```

## Run the app

From the project root, start the Streamlit home page:

```bash
streamlit run Trading_App.py
```

On Windows, you can also run:

```powershell
py -m streamlit run Trading_App.py
```

Streamlit prints a local URL in the terminal. Open that URL in your browser to
use the app. Use the sidebar to switch between **Stock Analysis** and
**Prediction**.

## Using the pages

### Stock Analysis

1. Enter a valid Yahoo Finance ticker, such as `AAPL` or `TSLA`.
2. Choose a start and end date.
3. Review the company information, financial statistics, and recent historical
   prices.
4. Choose a chart type, indicator, and time period to explore the available
   price history.

### Stock Prediction

1. Enter a valid Yahoo Finance ticker. The default is `AAPL`.
2. Allow the app to download historical data and fit the model.
3. Review the RMSE value, forecast table, and chart.

The forecast dates and model behavior depend on the data returned and the
forecasting implementation. The displayed RMSE is a simple evaluation score and
should not be used on its own to assess a trading strategy.

## Troubleshooting

- **No data or an error during analysis:** Check the ticker spelling and make
  sure it is supported by Yahoo Finance. For example, Apple is `AAPL`, not
  `APPL`.
- **Download or connection errors:** Check your internet connection and try
  again later. The data provider may be unavailable or may limit requests.
- **The forecast takes time or fails:** ARIMA fitting can take time, especially
  with longer histories. The forecasting page requires enough valid historical
  observations for its rolling mean, stationarity check, and model.
- **A package cannot be imported:** Install the dependencies using the command
  above in the same Python environment used to run Streamlit.

## Important note

Stock prices are uncertain, and a model trained on past prices cannot guarantee
future results. This project is for learning and exploration only. It does not
provide personalized financial advice, and forecasts should not be the sole
basis for investment decisions.
