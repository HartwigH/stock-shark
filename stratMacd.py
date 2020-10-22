import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return (Buy, Sell)

def profit_loss(data, budget):
    shares = 0
    last_transaction = 'Sell'

    for i in range(0, len(data)):

        if last_transaction == 'Sell' and not np.isnan(data['Buy_Signal_Price'][i]):
            buy = data['Buy_Signal_Price'][i]
            shares = budget / buy
            last_transaction = 'Buy'

        if last_transaction == 'Buy' and not np.isnan(data['Sell_Signal_Price'][i]):
            sell = data['Sell_Signal_Price'][i]
            budget = sell * shares
            last_transaction = 'Sell'

    budget = data['Close'].iloc[-1] * shares
    return budget

def show_details(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='red', width=1.5), name='MACD'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Signal Line'], line=dict(color='green', width=1.5), name='Signal Line'))

    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        title='Signal Line and MACD',
        yaxis_title=''
    )

    st.plotly_chart(fig)

def get_macd(df, budget, details):

    ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
    LongEMA = df.Close.ewm(span=26, adjust=False).mean()

    MACD = ShortEMA - LongEMA
    signal = MACD.ewm(span=9, adjust=False).mean()

    df['MACD'] = MACD
    df['Signal Line'] = signal

    a = buy_sell(df)
    df['Buy_Signal_Price'] = a[0]
    df['Sell_Signal_Price'] = a[1]

    x = profit_loss(df, budget)
    st.write('________________________')
    st.write('***MACD***')
    st.write('Using only MACD with budget: ***', "{0:,.2f}".format(budget), '*** your gain/loss would be: ***', "{0:,.2f}".format(x), '*** however don\'t forget the service fees and inflation.')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], line=dict(color='rgba(0,0,255,0.2)', width=1.5), name='Close price'))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Buy_Signal_Price'],
        mode='markers',
        marker=dict(size=8,
                    color='green',
                    symbol='triangle-up'),
        name='Buy'))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Sell_Signal_Price'],
        mode='markers',
        marker=dict(size=8,
                    color='red',
                    symbol='triangle-down'),
        name='Sell'))

    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        title='MACD - Close Price Buy & Sell Signals',
        yaxis_title='Close price USD ($)'
    )

    st.plotly_chart(fig)

    if details == True:
        show_details(df)