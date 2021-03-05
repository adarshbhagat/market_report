#importing all libraries
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
st.markdown('<style>body{background-color: darkseagreen;}</style>',unsafe_allow_html=True)

# Finding special index
def get_url():
    current_time = datetime.datetime.now()
    s='https://www1.nseindia.com/content/indices/ind_close_all_'
    if current_time.day < 10:
        s=s+'0'+str(current_time.day)
    else:
        s=s+str(current_time.day)
    if current_time.month < 10:
        s=s+'0'+str(current_time.month)
    else:
        s=s+str(current_time.month)
    s=s+str(current_time.year)+'.csv'
    return s

url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=49'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(class_='tbldata14 bdrtpg')
df = pd.read_html(str(result))
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(class_='tbldata14 bdrtpg')
df = pd.read_html(str(result))[0]
df.sort_values(by=['%Chg'], inplace=True, ascending=False)
gainers=df.head()# Contains top gainers from NIFTY 200
df.sort_values(by=['%Chg'], inplace=True, ascending=True)
loosers = df.head()# contains top loosers from NIFTY 200

st.title('NIFTY 200 Performance')

fig = plt.figure(figsize = (10, 5)) 
  
# creating the bar plot 
plt.bar(gainers['Company Name'].str[:-34], gainers['%Chg'], color ='royalblue',  
        width = 0.4) 
  
plt.xlabel("Company Name")
plt.ylabel("% Change")
plt.title("Top Gainers in NIFTY-200")
fig.autofmt_xdate()
st.pyplot(plt)

fig = plt.figure(figsize = (10, 5))
  
# creating the bar plot
plt.bar(loosers['Company Name'].str[:-34], loosers['%Chg'], color ='royalblue',  
        width = 0.4) 
  
plt.xlabel("Company Name") 
plt.ylabel("% Change") 
plt.title("Top Loosers in NIFTY-200")
fig.autofmt_xdate()
st.pyplot(plt)

URL = 'https://www.moneycontrol.com/india/stockmarket/stock-deliverables/marketstatistics/indices/cnx-200.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
df = pd.read_html(str(soup))
df=df[1]
df=df[df['5-Day Avg Del %']>50]
st.title("High Delivery percentage(NIFTY-200)")
st.write(df,backgroundcolor='yellow')

url=get_url()
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))

df.sort_values(by=['Change(%)'], inplace=True, ascending=False)
df=df.head()
df.sort_values(by=['Change(%)'], inplace=True, ascending=True)
fig = plt.figure(figsize = (10, 5))
  
# creating the bar plot
plt.bar(df['Index Name'], df['Change(%)'], color ='royalblue',  
        width = 0.4) 
  
st.title("Top Performing Index")
plt.xlabel("Index") 
plt.ylabel("% Change") 
plt.title("Indices")
fig.autofmt_xdate()
st.pyplot(plt)


URL = 'https://www.moneycontrol.com/indian-indices/nifty-50-9.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='indi_contribute')
df = pd.read_html(str(result))# stocks dragging index(up and don both)
d1=df[0]# stocks dragging nifty up
d2=df[1]# stocks dragging nifty down

fig = plt.figure(figsize = (10, 5))
plt.bar(d1['Stock Name'], d1['Contribution'], color ='royalblue',  width = 0.4) 
st.title("Stocks Lifting NIFTY-50")
plt.xlabel("Stocks Name") 
plt.ylabel("% Change") 
plt.title("Stock influencing NIFTY")
fig.autofmt_xdate()
st.pyplot(plt)

fig = plt.figure(figsize = (10, 5))
plt.bar(d2['Stock Name'], d2['Contribution'], color ='royalblue',  width = 0.4) 
st.title("Stocks Dropping NIFTY-50")
plt.xlabel("Stocks Name") 
plt.ylabel("% Change") 
plt.title("Stock influencing NIFTY")
fig.autofmt_xdate()
st.pyplot(plt)
