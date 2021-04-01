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

li = ['TOP GAINERS IN NIFTY-200','TOP LOOSERS IN NIFTY-200','HIGH DELIVERY PERCENTAGE','LOW DELIVERY PERCENTAGE','STOCKS DRAGGING NIFTY UP','STOCKS DRAGGING NIFTY DOWN','TOP GAINER SECTORS','TOP LOOSER SECTORS','RSI SCANS']
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
    st.write("RSI crossing above 60 in daily chart :- [Link](https://chartink.com/screener/rsi-crossed-above-60)")
    st.write("RSI crossing below 40 in daily chart :- [Link](https://chartink.com/screener/rsi-crossed-below-40)")
    st.write("RSI crossing above 40 in weekly chart :- [Link](https://chartink.com/screener/weekly-rsi-cross-40)")
    
else:
    #Delivery Percentage
    URL = 'https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/cnx-200.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    df = pd.read_html(str(soup))
    df=df[1]
    dp2 = df[df['5-Day Avg Del %']<20].reset_index(drop=True)
    st.write(dp2[['Company Name', 'Chg %', 'Dely %', '5-Day Avg Del %']].style.set_properties(**{'background-color': 'white','color': '#04c922'}))
    
   
