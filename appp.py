import numpy as np 
import pandas as pd 
import yfinance as yf 
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt



model = load_model(r"C:\Users\Rahul\Downloads\Stock Prediction Model.keras")
print(model)

st.header('Stock Market Prediction')

stock =st.text_input('Enter Stock Symbol', 'GOOG')
start = '2012-01-01'
end = '2024-03-31'

data = yf.download(stock, start, end)

st.subheader('Stock Data')   
st.write(data)

data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

pas_100_days = data_train.tail(100)
data_test = pd.concat([pas_100_days,data_test], ignore_index=100)
data_test_scale = scaler.fit_transform(data_test)



st.subheader('Price vs MA50')
ma_50_days = data.Close.rolling(50).mean()
fig1 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r')
plt.plot(data.Close, 'g')
plt.show()
st.pyplot(fig1)

st.subheader('Price vs MA50 vs MA100')
ma_100_days = data.Close.rolling(100).mean()
fig2 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r')
plt.plot(ma_100_days, 'b')
plt.plot(data.Close, 'g')
plt.show()
st.pyplot(fig2)



scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(data_test)

x = []
y = []

for i in range(100, data_test_scale.shape[0]):
    x.append(data_test_scale[i-100: i])
    y.append(data_test_scale[i, 0])

x, y = np.array(x), np.array(y)



predict = model.predict(x)
scaler = scaler.scale_

predict = predict * scaler

y = y * scaler

st.subheader('Original Price vs Predicted Price')
fig4 = plt.figure(figsize=(8,6))
plt.plot(y, 'g', label = 'Predicted Price')
plt.plot(predict, 'r', label = 'Original Price')
plt.legend()

st.pyplot(fig4)


