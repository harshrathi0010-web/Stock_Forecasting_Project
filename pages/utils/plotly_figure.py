import plotly.graph_objects as go
import dateutil

def plotly_table(dataframe):
    headerColor = '#0078ff'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    # Alternate row colors for all rows in dataframe
    cell_colors = [rowOddColor, rowEvenColor] * (len(dataframe) // 2 + 1)
    cell_colors = cell_colors[:len(dataframe)]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b></b>"] + [f"<b>{str(col)[:10]}</b>" for col in dataframe.columns],
            line_color='#0078ff',
            fill_color=headerColor,
            align='center',
            font=dict(color='white', size=15),
            height=35,
        ),
        cells=dict(
            values=[[f"<b>{str(i)}</b>" for i in dataframe.index]] + [dataframe[col] for col in dataframe.columns],
            fill_color=[cell_colors],
            align='left',
            line_color=['white'],
            font=dict(color=["black"], size=15),
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def Moving_average_forecast(dataframe):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['Close'],
        mode='lines',
        name='Close Price'
    ))
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        xaxis_title='Date',
        yaxis_title='Price'
    )
    return fig


def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = dataframe.index[-1].replace(month=1, day=1, hour=0, minute=0, second=0)
    else:
        date = dataframe.index[0]

    reset_dataframe = dataframe.reset_index()
    return reset_dataframe[reset_dataframe['Date'] > date]


def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], 
        y=dataframe['Open'],
        mode='lines',
        name='Open',
        line=dict(width=2, color='#5ab7ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], 
        y=dataframe['Close'],
        mode='lines',
        name='Close',
        line=dict(width=2, color='black')
    ))
    
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], 
        y=dataframe['High'],
        mode='lines', 
        name='High',
        line=dict(width=2, color='#0078ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], 
        y=dataframe['Low'],
        mode='lines', 
        name='Low',
        line=dict(width=2, color='red')
    ))
    
    fig.update_xaxes(rangeslider_visible=True)
    
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            yanchor="top",
            xanchor="right"
        )
    )
    
    return fig



def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close']
    ))

    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff'
    )
    return fig



def RSI(dataframe, num_period):
    dataframe = dataframe.copy()
    price_change = dataframe['Close'].diff()
    average_gain = price_change.clip(lower=0).ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    average_loss = -price_change.clip(upper=0).ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    relative_strength = average_gain / average_loss
    dataframe['RSI'] = 100 - (100 / (1 + relative_strength))
    dataframe.loc[(average_gain == 0) & (average_loss == 0), 'RSI'] = 50
    dataframe.loc[(average_gain > 0) & (average_loss == 0), 'RSI'] = 100
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    
    # RSI Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, 
        name='RSI', 
        marker_color='orange', 
        line=dict(width=2, color='orange')
    ))
    
    # Overbought Line (70)
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70] * len(dataframe), 
        name='Overbought', 
        marker_color='red', 
        line=dict(width=2, color='red', dash='dash')
    ))

    # Oversold Line (30) with fill
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30] * len(dataframe), 
        fill='tonexty', 
        name='Oversold', 
        marker_color='#79da84', 
        line=dict(width=2, color='#79da84', dash='dash')
    ))

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200, 
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff', 
        margin=dict(l=0, r=0, t=0, b=0), 
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def MACD(dataframe, num_period):
    dataframe = dataframe.copy()
    fast_ema = dataframe['Close'].ewm(span=12, adjust=False).mean()
    slow_ema = dataframe['Close'].ewm(span=26, adjust=False).mean()
    dataframe['MACD'] = fast_ema - slow_ema
    dataframe['MACD Signal'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
    dataframe['MACD Hist'] = dataframe['MACD'] - dataframe['MACD Signal']

    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    # MACD Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'], 
        name='MACD',  # In video shown as 'RSI' due to copy-paste
        marker_color='orange', 
        line=dict(width=2, color='orange')
    ))

    # MACD Signal Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'], 
        name='Signal',  # In video shown as 'Overbought' due to copy-paste
        marker_color='red', 
        line=dict(width=2, color='red', dash='dash')
    ))

    # (Optional: Add histogram bar chart if you want it displayed)
    # fig.add_trace(go.Bar(
    #     x=dataframe['Date'], 
    #     y=dataframe['MACD Hist'], 
    #     marker_color=c, 
    #     name='MACD Hist'
    # ))

    fig.update_layout(
        height=200,
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig