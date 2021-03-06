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
st.markdown('<style>body{background-color: #8fa5ff;}</style>',unsafe_allow_html=True)

li = ['TOP GAINERS IN NIFTY-200','TOP LOOSERS IN NIFTY-200','HIGH DELIVERY PERCENTAGE','LOW DELIVERY PERCENTAGE','STOCKS DRAGGING NIFTY UP','STOCKS DRAGGING NIFTY DOWN','TOP GAINER SECTORS','TOP LOOSER SECTORS']
sel = st.selectbox('Select any one', li)

def plot_bar(df,col1,col2,x_label,y_label):
    st.title(sel)
    fig = plt.figure(figsize = (10, 6))
    plt.bar(df[col1], df[col2], color ='royalblue', width = 0.4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fig.autofmt_xdate()
    st.pyplot(plt)
    
## For NIFTY-200
url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=49'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(class_='tbldata14 bdrtpg')
df = pd.read_html(str(result))
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(class_='tbldata14 bdrtpg')
df = pd.read_html(str(result))[0]
df['Company Name']  = df['Company Name'].str[:-34]
df.sort_values(by=['%Chg'], inplace=True, ascending=False)
gainers=df.head()# Contains top gainers from NIFTY 200
df.sort_values(by=['%Chg'], inplace=True, ascending=True)
loosers = df.head()# contains top loosers from NIFTY 200

#Sector wise

URL = 'https://www.zeebiz.com/market/sectors-nse'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
df = pd.read_html(str(soup))
df = df[0]
df['Change %'] = df['Change %'].str[:-2]
df["Change %"] = pd.to_numeric(df["Change %"])
df.sort_values(by=['Change %'], inplace=True,ascending=False)
s1 = df.head()
s2 = df.tail()

#Stocks dragging NIFTY

URL = 'https://www.moneycontrol.com/indian-indices/nifty-50-9.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='indi_contribute')
df = pd.read_html(str(result))# stocks dragging index(up and don both)
dn1=df[0]# stocks dragging nifty up
dn2=df[1]# stocks dragging nifty dow

#Delivery Percentage
URL = 'https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/cnx-200.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
df = pd.read_html(str(soup))
df=df[1]
dp1 = df[df['5-Day Avg Del %']>60].reset_index(drop=True)
dp2 = df[df['5-Day Avg Del %']<20].reset_index(drop=True)

    
if sel == 'TOP GAINERS IN NIFTY-200':
    plot_bar(gainers,'Company Name','%Chg','Gainers','Change %')
elif sel == 'TOP LOOSERS IN NIFTY-200':
    plot_bar(loosers,'Company Name','%Chg','Loosers','Change %')
elif sel == 'TOP GAINER SECTORS':
    plot_bar(s1,'Sectors','Change %', 'Sector', 'Change %')
elif sel == 'TOP LOOSER SECTORS':
    plot_bar(s2,'Sectors','Change %', 'Sector', 'Change %')
elif sel == 'STOCKS DRAGGING NIFTY UP':
    plot_bar(dn1,'Stock Name','Contribution', 'Stock Name', 'Contribution')
elif sel == 'STOCKS DRAGGING NIFTY DOWN':
    plot_bar(dn2,'Stock Name','Contribution', 'Stock Name', 'Contribution')
elif sel == 'HIGH DELIVERY PERCENTAGE':
    st.write(dp1[['Company Name', 'Chg %', 'Dely %', '5-Day Avg Del %']])
else:
    st.write(dp2[['Company Name', 'Chg %', 'Dely %', '5-Day Avg Del %']])
    
   
