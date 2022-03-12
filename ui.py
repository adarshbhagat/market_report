import pandas as pd
import io
import getpass
import requests
import datetime
from bs4 import BeautifulSoup
import smtplib
import streamlit as st
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
st.markdown('<style>body{background-color: #95db70;}</style>',unsafe_allow_html=True)

li = ['TOP GAINERS IN NIFTY-200','TOP LOOSERS IN NIFTY-200','HIGH DELIVERY PERCENTAGE','LOW DELIVERY PERCENTAGE','STOCKS DRAGGING NIFTY UP','STOCKS DRAGGING NIFTY DOWN','TOP DECISIVE STOCKS','TOP INDECISIVE STOCKS','TOP GAINER SECTORS','TOP LOOSER SECTORS','RSI SCANS']
sel = st.selectbox('Select any one', li)

def plot_bar(df,col1,col2,x_label,y_label):
    st.title(sel)
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize = (9, 6))
    plt.bar(df[col1], df[col2], color ='royalblue', width = 0.4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fig.autofmt_xdate()
    st.pyplot(plt)
    

    

    
if sel == 'TOP GAINERS IN NIFTY-200':
    url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=49'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='tbldata14 bdrtpg')
    df = pd.read_html(str(result))[0]
    df['Company Name']  = df['Company Name'].str[:-34]
    df.sort_values(by=['%Chg'], inplace=True, ascending=False)
    gainers=df.head()# Contains top gainers from NIFTY 200
    plot_bar(gainers,'Company Name','%Chg','Gainers','Change %')
elif sel == 'TOP LOOSERS IN NIFTY-200':
    url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=49'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='tbldata14 bdrtpg')
    df = pd.read_html(str(result))[0]
    df['Company Name']  = df['Company Name'].str[:-34]
    df.sort_values(by=['%Chg'], inplace=True, ascending=True)
    loosers = df.head()# contains top loosers from NIFTY 200
    plot_bar(loosers,'Company Name','%Chg','Loosers','Change %')
elif sel == 'TOP GAINER SECTORS':
    URL = 'https://www.zeebiz.com/market/sectors-nse'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))
    df = df[0]
    df['Change %'] = df['Change %'].str[:-2]
    df["Change %"] = pd.to_numeric(df["Change %"])
    df.sort_values(by=['Change %'], inplace=True,ascending=False)
    s1 = df.head()
    plot_bar(s1,'Sectors','Change %', 'Sector', 'Change %')
elif sel == 'TOP LOOSER SECTORS':
    URL = 'https://www.zeebiz.com/market/sectors-nse'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))
    df = df[0]
    df['Change %'] = df['Change %'].str[:-2]
    df["Change %"] = pd.to_numeric(df["Change %"])
    df.sort_values(by=['Change %'], inplace=True,ascending=False)
    s2 = df.tail()
    plot_bar(s2,'Sectors','Change %', 'Sector', 'Change %')
elif sel == 'STOCKS DRAGGING NIFTY UP':
    URL = 'https://www.moneycontrol.com/indian-indices/nifty-50-9.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(id='indi_contribute')
    df = pd.read_html(str(result))# stocks dragging index(up and don both)
    plot_bar(df[0],'Stock Name','Contribution', 'Stock Name', 'Contribution')
elif sel == 'STOCKS DRAGGING NIFTY DOWN':
    URL = 'https://www.moneycontrol.com/indian-indices/nifty-50-9.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(id='indi_contribute')
    df = pd.read_html(str(result))# stocks dragging index(up and don both)
    plot_bar(df[1],'Stock Name','Contribution', 'Stock Name', 'Contribution')
elif sel == 'HIGH DELIVERY PERCENTAGE':
    URL = 'https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/cnx-200.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))
    df=df[1]
    dp1 = df[df['5-Day Avg Del %']>60].reset_index(drop=True)
    st.write(dp1[['Company Name', 'Chg %', 'Dely %', '5-Day Avg Del %']].style.set_properties(**{'background-color': 'white','color': '#04c922'}))
    
elif sel == 'RSI SCANS':
    st.write("RSI crossing above 60 in daily+weekly+monthly chart :- [Link](https://chartink.com/screener/copy-main-7-star-setup)")
    st.write("RSI near 40 in daily chart with daily+weekly RSI>60 :- [Link](https://chartink.com/screener/5-star-40-support)")
    st.write("3 Candle Triangle in daily chart :- [Link](https://chartink.com/screener/3-candle-triangle-in-daily-chart)")
    
    
elif sel == 'TOP DECISIVE STOCKS':
    url = 'https://www.moneycontrol.com/markets/indian-indices/reDrawColData?deviceType=web&exName=N&indicesID=49&selTab=o&subTabOT=d&subTabOPL=cl&selPage=marketTerminal&classic=true&o=chg,opn,hg,lw,precl'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))[0]
    df['Body Length'] = df['Open']-df['Prev. Close']
    df['Body Length'] = df['Body Length'].abs()
    df['Wick Length'] = df['High']-df['Low']
    df['Indecision Intensity'] = df['Wick Length']/df['Body Length']
    df=df[['Name','Indecision Intensity']]
    df.sort_values(by=['Indecision Intensity'], inplace=True, ascending=True)
    data = df.head()
    plot_bar(data,'Name','Indecision Intensity','Company Name','Indecision Intensity')
    
    
    
elif sel == 'TOP INDECISIVE STOCKS':
    url = 'https://www.investing.com/indices/cnx-200-components'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #result = soup.find(class_='genTbl closedTbl crossRatesTbl elpTbl elp25')
    df = pd.read_html(str(soup))[0]
    df=df.reset_index(drop=True)
    df['Open']=df['Last']+df['Chg.']
    df['Body Length'] = df['Open']-df['Last']
    df['Body Length'] = df['Body Length'].abs()
    df['Wick Length'] = df['High']-df['Low']
    df['Indecision Intensity'] = df['Wick Length']/df['Body Length']
    df=df[['Name','Indecision Intensity']]
    df.sort_values(by=['Indecision Intensity'], inplace=True, ascending=True)
    data = df.tail()
    plot_bar(data,'Name','Indecision Intensity','Company Name','Indecision Intensity')    
    
else:
    #Delivery Percentage
    URL = 'https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/cnx-200.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))
    df=df[1]
    dp2 = df[df['5-Day Avg Del %']<20].reset_index(drop=True)
    st.write(dp2[['Company Name', 'Chg %', 'Dely %', '5-Day Avg Del %']].style.set_properties(**{'background-color': 'white','color': '#04c922'}))
    
   
