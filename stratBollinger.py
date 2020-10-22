import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def get_signal(data, df):
    buy_signal = []
    sell_signal = []

    for i in range(len(data['Close'])):
        if data['Close'][i] > data['Upper'][i]:
            buy_signal.append(np.nan)
            sell_signal.append(df['Close'][i])
        elif data['Close'][i] < data['Lower'][i]:
            buy_signal.append(df['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)

    return (buy_signal, sell_signal)

def profit_loss(data, budget):
    shares = 0
    last_transaction = 'Sell'

    for i in range(0, len(data)):

        if last_transaction == 'Sell' and not np.isnan(data['Buy'][i]):
            buy = data['Buy'][i]
            shares = budget / buy
            last_transaction = 'Buy'

        if last_transaction == 'Buy' and not np.isnan(data['Sell'][i]):
            sell = data['Sell'][i]
            budget = sell * shares
            last_transaction = 'Sell'

    budget = data['Close'].iloc[-1] * shares
    return budget

def get_bollinger(df, budget, details):
    period = 20
    df['Middle'] = df['Close'].rolling(window=20).mean()
    df['Lower'] = df['Middle'] - 1.96 * df['Close'].rolling(window=20).std()
    df['Upper'] = df['Middle'] + 1.96 * df['Close'].rolling(window=20).std()

    new_df = df[period-1:]

    new_df['Buy'] = get_signal(new_df, df)[0]
    new_df['Sell'] = get_signal(new_df, df)[1]

    x = profit_loss(new_df, budget)
    st.write('________________________')
    st.write('***Bollinger***')
    st.write('Using only Bollinger with budget: ***', "{0:,.2f}".format(budget), '*** your gain/loss would be: ***', "{0:,.2f}".format(x), '*** however don\'t forget the service fees and inflation.')


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=new_df.index, y=new_df['Close'], line=dict(color='rgba(0,0,255,0.2)', width=1.5), name='Close price'))
    fig.add_trace(go.Scatter(
        x=new_df.index,
        y=new_df['Buy'],
        mode='markers',
        marker=dict(size=8,
                    color='green',
                    symbol='triangle-up'),
        name='Buy'))
    fig.add_trace(go.Scatter(
        x=new_df.index,
        y=new_df['Sell'],
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