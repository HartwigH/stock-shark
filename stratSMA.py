import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

def buy_sell(data):
    Buy = []
    Sell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                Buy.append(data['SYMBOL'][i])
                Sell.append(np.nan)
                flag = 1
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                Buy.append(np.nan)
                Sell.append(data['SYMBOL'][i])
                flag = 0
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return (Buy, Sell)

def show_details(df, SMA30, SMA100):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], line=dict(color='rgba(0,0,255)', width=1.5), name='Close price'))
    fig.add_trace(
        go.Scatter(x=SMA30.index, y=SMA30['Adj Close'], line=dict(color='rgba(0,255,255)', width=1.5), name='SMA30'))
    fig.add_trace(
        go.Scatter(x=SMA100.index, y=SMA100['Adj Close'], line=dict(color='rgba(255,0,255)', width=1.5), name='SMA100'))


    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        title='SMA 30&100 - Close Price Buy & Sell Signals',
        yaxis_title='Close price USD ($)'
    )

    st.plotly_chart(fig)

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

    budget = data['SYMBOL'].iloc[-1] * shares
    return budget

def get_sma(df, budget, details):
    SMA30 = pd.DataFrame()
    SMA30['Adj Close'] = df['Adj Close'].rolling(window=30).mean()

    SMA100 = pd.DataFrame()
    SMA100['Adj Close'] = df['Adj Close'].rolling(window=100).mean()

    data = pd.DataFrame()
    data['SYMBOL'] = df['Adj Close']
    data['SMA30'] = SMA30['Adj Close']
    data['SMA100'] = SMA100['Adj Close']

    a = buy_sell(data)
    data['Buy_Signal_Price'] = a[0]
    data['Sell_Signal_Price'] = a[1]

    x = profit_loss(data, budget)
    st.write('________________________')
    st.write('***SMA30 & SMA100***')
    st.write('Using only MACD with budget: ***', "{0:,.2f}".format(budget), '*** your gain/loss would be: ***', "{0:,.2f}".format(x), '*** however don\'t forget the service fees and inflation.')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=df['Adj Close'], line=dict(color='rgba(0,0,255, 0.2)', width=1.5), name='Close price'))
    fig.add_trace(
        go.Scatter(x=data.index, y=SMA30['Adj Close'], line=dict(color='rgba(0,255,255, 0.2)', width=1.5), name='SMA30'))
    fig.add_trace(
        go.Scatter(x=data.index, y=SMA100['Adj Close'], line=dict(color='rgba(255,0,255, 0.2)', width=1.5), name='SMA100'))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Buy_Signal_Price'],
        mode='markers',
        marker=dict(size=8,
                    color='green',
                    symbol='triangle-up'),
        name='Buy'))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Sell_Signal_Price'],
        mode='markers',
        marker=dict(size=8,
                    color='red',
                    symbol='triangle-down'),
        name='Sell'))

    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        title='SMA 30&100 - Close Price Buy & Sell Signals',
        yaxis_title='Close price USD ($)'
    )

    st.plotly_chart(fig)

    if details == True:
        show_details(df, SMA30, SMA100)