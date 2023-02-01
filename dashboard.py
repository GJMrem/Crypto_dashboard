import streamlit as st
import pandas as pd
import requests
import altair as alt
import json
from datetime import datetime, timedelta

asset = st.sidebar.selectbox("Select an asset", ["BTC", "ETH", "LTC", "ADA"])

sidebar_left, sidebar_right = st.sidebar.columns(2)
date_from = sidebar_left.date_input("Date from", datetime.today() - timedelta(days = 30))
date_to = sidebar_right.date_input("Date to", datetime.today())


name = {"BTC":"bitcoin", "ETH":"ethereum", "LTC":"litecoin", "ADA":"cardano"}
url = " http://api.coincap.io/v2/assets/" + name[asset] \
        + "/history?interval=d1" \
        + "&start=" + str(datetime.combine(date_from, datetime.min.time()).timestamp()*1000) \
        + "&end=" + str(int(datetime.combine(date_to, datetime.min.time()).timestamp()*1000))

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

df = pd.DataFrame(json.loads(response.text)['data'])
df['priceUsd'] = df['priceUsd'].astype(float)
df['date']= df['date'].astype('datetime64')
df = df.drop(columns='time')
df.set_index('date')

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('date:T', axis=alt.Axis(format = '%d %b', title='Time')),
    y=alt.Y('priceUsd:Q', axis=alt.Axis(format = '$f', title='Price')),
    tooltip=[alt.Tooltip('date:T',format='%Y-%m-%d'), alt.Tooltip('priceUsd:Q', format = '$f')]
).interactive()

st.write(name[asset].capitalize())
st.altair_chart(chart, use_container_width=True)