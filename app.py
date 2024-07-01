# Importing the necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title = 'Stock Dashboard',
    layout = 'centered',
    page_icon = '📈'
    )


# Title of the app
st.title('Stock Dashboard')

# Setting default ticker
default_ticker = 'MSFT'

# Setting default start and end date - 1 year back
default_end_date = pd.to_datetime('today')
default_start_date = default_end_date - pd.DateOffset(years=1)


# Sidebar
ticker = st.sidebar.text_input('Ticker', default_ticker)
start_date = st.sidebar.date_input('Start Date', default_start_date)
end_date = st.sidebar.date_input('End Date', default_end_date)

# Fetching the data
data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x = data.index, y = data['Close'], title=ticker)

# Centering the title
fig.update_layout(
    title={
        'text': ticker,
        'x': 0.5,  # Set title x-coordinate to center it
        'xanchor': 'center',  # Anchor title to center
        'yanchor': 'top'  # Align title to the top of the plot
    }
)

# Removing the x-axis label
fig.update_xaxes(title_text='')

st.plotly_chart(fig)



# creating tab
pricing_data = st.tabs(['Pricing Data'])

# Information under pricing data tab
with pricing_data[0]:
    st.header('Price Movement')
    
    # Creating a copy of the data
    data2 = data

    # Adding a new column for % change
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)
    data2.dropna(inplace=True)
    st.write(data2)

    # Annual return
    # annual_return = data2['% Change'].mean() * 252 * 100
    # st.write('Annual Return: ', annual_return, '%')
    

# Information under news data tab
# with news_data:
#     st.header(f'News of {ticker}')
#     sn = StockNews(ticker, save_news = False)
#     df_news = sn.read_rss()

#     df_news
#     for i in range(15):
#         st.subheader(f'News {i+1}')
#         st.write(df_news['published'][i])
#         st.write(df_news['title'][i])
#         st.write(df_news['summary'][i])
#         st.write(df_news['link'][i])