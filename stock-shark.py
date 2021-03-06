#import the libs
import streamlit as st
import pandas as pd
import base64
import sys, os
import yfinance as yf
import plotly.graph_objects as go

from stratMacd import get_macd
from stratBollinger import get_bollinger
from stratSMA import get_sma

file_ = open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/shark.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# Initial page setup
st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="LHV 2020">',
    unsafe_allow_html=True,
)

st.text("\n")
st.markdown("""
This tool imports historic stock data from finance.yahoo.com :male-detective: (using yfinance) and was created for LHV Börsihai 2020 game with the intention of making technical analysis easier.
""")
st.text("\n")
st.markdown("""
:point_left:Select stock from ***S&P500,Tesla, Alibaba, Snowflake & Moderna***. Try different strategies to help you with your trades. :point_down:
""")


# Create sidebar header
st.sidebar.header('Select stock to investigate')

def get_stock_input():

    stock_symbol = st.sidebar.selectbox("Select Stock Symbol", ("9988.HK","A","AAL","AAP","AAPL","ABBV","ABC","ABMD","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEE","AEP","AES","AFL","AIG","AIV","AIZ","AJG","AKAM","ALB","ALGN","ALK","ALL","ALLE","ALXN","AMAT","AMCR","AMD","AME","AMGN","AMP","AMT","AMZN","ANET","ANSS","ANTM","AON","AOS","APA","APD","APH","APTV","ARE","ATO","ATVI","AVB","AVGO","AVY","AWK","AXP","AZO","BA","BABA","BAC","BAX","BBY","BDX","BEN","BIIB","BIO","BK","BKNG","BKR","BLK","BLL","BMY","BR","BSX","BWA","BXP","C","CAG","CAH","CARR","CAT","CB","CBOE","CBRE","CCI","CCL","CDNS","CDW","CE","CERN","CF","CFG","CHD","CHRW","CHTR","CI","CINF","CL","CLX","CMA","CMCSA","CME","CMG","CMI","CMS","CNC","CNP","COF","COG","COO","COP","COST","CPB","CPRT","CRM","CSCO","CSX","CTAS","CTLT","CTSH","CTVA","CTXS","CVS","CVX","CXO","D","DAL","DD","DE","DFS","DG","DGX","DHI","DHR","DIS","DISCA","DISCK","DISH","DLR","DLTR","DOV","DOW","DPZ","DRE","DRI","DTE","DUK","DVA","DVN","DXC","DXCM","EA","EBAY","ECL","ED","EFX","EIX","EL","EMN","EMR","EOG","EQIX","EQR","ES","ESS","ETFC","ETN","ETR","ETSY","EVRG","EW","EXC","EXPD","EXPE","EXR","F","FANG","FAST","FB","FBHS","FCX","FDX","FE","FFIV","FIS","FISV","FITB","FLIR","FLS","FLT","FMC","FOX","FOXA","FRC","FRT","FTI","FTNT","FTV","GD","GE","GILD","GIS","GL","GLW","GM","GOOG","GOOGL","GPC","GPN","GPS","GRMN","GS","GWW","HAL","HAS","HBAN","HBI","HCA","HD","HES","HFC","HIG","HII","HLT","HOLX","HON","HPE","HPQ","HRL","HSIC","HST","HSY","HUM","HWM","IBM","ICE","IDXX","IEX","IFF","ILMN","INCY","INFO","INTC","INTU","IP","IPG","IPGP","IQV","IR","IRM","ISRG","IT","ITW","IVZ","J","JBHT","JCI","JKHY","JNJ","JNPR","JPM","K","KEY","KEYS","KHC","KIM","KLAC","KMB","KMI","KMX","KO","KR","KSU","L","LB","LDOS","LEG","LEN","LH","LHX","LIN","LKQ","LLY","LMT","LNC","LNT","LOW","LRCX","LUMN","LUV","LVS","LW","LYB","LYV","MA","MAA","MAR","MAS","MCD","MCHP","MCK","MCO","MDLZ","MDT","MET","MGM","MHK","MKC","MKTX","MLM","MMC","MMM","MNST","MO","MOS","MPC","MRK","MRNA","MRNA","MRO","MS","MSCI","MSFT","MSI","MTB","MTD","MU","MXIM","MYL","NBL","NCLH","NDAQ","NEE","NEM","NFLX","NI","NKE","NLOK","NLSN","NOC","NOV","NOW","NRG","NSC","NTAP","NTRS","NUE","NVDA","NVR","NWL","NWS","NWSA","O","ODFL","OKE","OMC","ORCL","ORLY","OTIS","OXY","PAYC","PAYX","PBCT","PCAR","PEAK","PEG","PEP","PFE","PFG","PG","PGR","PH","PHM","PKG","PKI","PLD","PM","PNC","PNR","PNW","PPG","PPL","PRGO","PRU","PSA","PSX","PVH","PWR","PXD","PYPL","QCOM","QRVO","RCL","RE","REG","REGN","RF","RHI","RJF","RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","SBAC","SBUX","SCHW","SEE","SHW","SIVB","SJM","SLB","SLG","SNA","SNOW","SNOW ","SNPS","SO","SPG","SPGI","SRE","STE","STT","STX","STZ","SWK","SWKS","SYF","SYK","SYY","T","TAP","TDG","TDY","TEL","TER","TFC","TFX","TGT","TIF","TJX","TMO","TMUS","TPR","TROW","TRV","TSCO","TSLA","TSLA ","TSN","TT","TTWO","TWTR","TXN","TXT","TYL","UA","UAA","UAL","UDR","UHS","ULTA","UNH","UNM","UNP","UPS","URI","USB","V","VAR","VFC","VIAC","VLO","VMC","VNO","VRSK","VRSN","VRTX","VTR","VZ","WAB","WAT","WBA","WDC","WEC","WELL","WFC","WHR","WLTW","WM","WMB","WMT","WRB","WRK","WST","WU","WY","WYNN","XEL","XLNX","XOM","XRAY","XRX","XYL","YUM","ZBH","ZBRA","ZION","ZTS"))
    time_period = st.sidebar.radio("Select timeframe", ("1mo", "3mo", "6mo", "1y", "5y", "max"))

    return time_period, stock_symbol

# Create a function to get the users input
def get_input():
    details = False

    MACD = False
    BOLLINGER = False
    SMA = False

    st.sidebar.write("Select Strategies")
    if st.sidebar.checkbox('MACD'):
        MACD = True
    if st.sidebar.checkbox('BOLLINGER'):
        BOLLINGER = True
    if st.sidebar.checkbox('SMA'):
        SMA = True

    st.sidebar.write("View more details")
    if st.sidebar.checkbox('Show/Hide'):
        details = True

    budget = st.sidebar.slider("Select trading budget", 1000, 50000, 10000, 1000)

    options = {
        'MACD': MACD,
        'BOLLINGER': BOLLINGER,
        'SMA': SMA
    }

    return options, budget, details

# Get Company name
def get_company_name(symbol):
    path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/game_stocks.csv"
    df = pd.read_csv(path)
    df.set_index('symbol', inplace=True)
    name = df.loc[symbol]['name']

    return name

def load_data(symbol, time):
    data = yf.download(tickers=symbol, period=time)
    return data

#create a function to get the proper company data and the proper timeframe from the users
def get_data(symbol, time):
    if symbol != "":
        with st.spinner('Loading data...'):
            df =load_data(symbol, time)
    else:
        df = pd.DataFrame(columns= ['Date', 'Close', 'Open', 'Volume', 'Adj Close', 'High', 'Low'])

    return df

def get_strats(options, budget, details):
    if options['MACD'] == True:
        get_macd(df, budget, details)
    if options['BOLLINGER'] == True:
        get_bollinger(df, budget, details)
    if options['SMA'] == True:
        get_sma(df, budget, details)

# --- SETUP FROM HERE ---
time, symbol = get_stock_input()
options, budget, details = get_input()

company_name = get_company_name(symbol)

# --- WRITE FROM HERE ---
st.header(company_name)
st.markdown(
    f'<a href="https://finance.yahoo.com/quote/{symbol}">Fundamental Analysis</a> <- don\'t forget',
    unsafe_allow_html=True,
)

df = get_data(symbol, time)

fig = go.Figure()

fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'], name= 'Market data'))

fig.update_layout(
    title="Share price evolutions",
    yaxis_title="Stock Price (USD$ per Shares)"
)

fig.update_xaxes(rangeslider_visible=True)

st.plotly_chart(fig)


# -- Stategies --
get_strats(options, budget, details)

