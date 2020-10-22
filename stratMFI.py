import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

def show_details(df2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.index, y=df2['MFI'], line=dict(color='rgba(0,0,255)', width=1.5), name='Close price'))

    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        title='MFI Plotly.....',
        yaxis_title='MFI Values'
    )

    st.plotly_chart(fig)


# create a function to get the buy and sell signals
def get_signal(data, high, low):
    buy_signal = []
    sell_signal = []

    for i in range(len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['MFI'][i] < low:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            sell_signal.append(np.nan)
            buy_signal.append(np.nan)

    return (buy_signal, sell_signal)

def get_mfi(df, budget, details):
    # calculate the typical price
    typical_price = (df['Close'] + df['High'] + df['Low']) / 3
    period = 14
    # calculate the money flow
    money_flow = typical_price * df['Volume']

    # get all of the positive and negative money flows
    positive_flow = []
    negative_flow = []

    # loop through the typical price
    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i - 1]:
            positive_flow.append(money_flow[i - 1])
            negative_flow.append(0)
        elif typical_price[i] < typical_price[i - 1]:
            negative_flow.append(money_flow[i - 1])
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)

    # get all of the positive and negative money flows with time period
    positive_mf = []
    negative_mf = []

    for i in range(period - 1, len(positive_flow)):
        positive_mf.append(sum(positive_flow[i + 1 - period: i + 1]))
    for i in range(period - 1, len(negative_flow)):
        negative_mf.append(sum(negative_flow[i + 1 - period: i + 1]))

    # calculate the money flow index
    mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

    # visually show the MFI
    df2 = pd.DataFrame()
    df2['MFI'] = mfi

    # create a new data frame
    new_df = pd.DataFrame()
    new_df = df[period:]
    new_df['MFI'] = mfi

    # add new columns (Buy & Sell)
    new_df['Buy'] = get_signal(new_df, 80, 20)[0]
    new_df['Sell'] = get_signal(new_df, 80, 20)[1]

    st.write(new_df)

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

    if details == True:
        show_details(df2)