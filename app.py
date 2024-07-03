# Importing the necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from newsapi import NewsApiClient
import re

# Setting up the News API
newsapi = NewsApiClient(api_key='b2a3c3ba1d7d496999f014d7313ca511')


# Page configuration
st.set_page_config(
    page_title='Stock Dashboard',
    layout='centered',
    page_icon='📈',
)

# Hide Streamlit style
hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { padding: 0; }
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the app
st.title('Stock Dashboard')

# Setting default ticker
default_ticker = 'MSFT'

# Setting default start and end date - 1 year back
default_end_date = pd.to_datetime('today')
default_start_date = default_end_date - pd.DateOffset(years=1)

max_date = pd.to_datetime('today')

# Main section for entering initial ticker and date range
ticker = st.text_input('Enter Ticker', default_ticker).upper()
start_date = st.date_input('Start Date', default_start_date, max_value=max_date, min_value=pd.Timestamp('1900-01-01'))
end_date = st.date_input('End Date', default_end_date, max_value=max_date, min_value=pd.Timestamp('1900-01-01'))


# Function to fetch and display data for single ticker
def fetch_and_display_data(ticker, start_date, end_date):
    # Fetching the data
    data = yf.download(ticker, start=start_date, end=end_date)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker.upper()))

   # Layout settings
    fig.update_layout(
        title={
            'text': ticker,
            'x': 0.5,  # Set title x-coordinate to center it
            'xanchor': 'center',  # Anchor title to center
            'yanchor': 'top'  # Align title to the top of the plot
        },
        xaxis_title='',  # Remove x-axis title
        yaxis_title='Price'
    )

    # Display the plot
    st.plotly_chart(fig)

# Function to fetch and display comparison data for two tickers
def fetch_and_display_comparison(ticker1, ticker2, start_date, end_date):
    # Fetching the data for both tickers
    data1 = yf.download(ticker1, start=start_date, end=end_date)
    data2 = yf.download(ticker2, start=start_date, end=end_date)

    # Creating traces for each ticker
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data1.index, y=data1['Close'], mode='lines', name=ticker1.upper()))
    fig.add_trace(go.Scatter(x=data2.index, y=data2['Close'], mode='lines', name=ticker2.upper()))


    # Layout settings
    fig.update_layout(
        title={
            'text': f'{ticker1} & {ticker2} Comparison',
            'x': 0.5,  # Set title x-coordinate to center it
            'xanchor': 'center',  # Anchor title to center
            'yanchor': 'top'  # Align title to the top of the plot
        },
        xaxis_title='',  # Remove x-axis title
        yaxis_title='Price'
    )

    
    # Display the plot
    st.plotly_chart(fig)

# Analyze button to trigger main graph display
if st.button('Analyze', key='analyze'):
    fetch_and_display_data(ticker, start_date, end_date)

# Dropdown for Pricing Data section
with st.expander('Pricing Movement'):
   
    data = yf.download(ticker, start=start_date, end=end_date)
    st.header(f'{ticker} Price Movement')
    st.write(data)


# Function to filter relevant news articles
def filter_relevant_news(articles, ticker):
    relevant_articles = []
    for article in articles:
        if article['description'] and re.search(ticker, article['description'], re.IGNORECASE):
            relevant_articles.append(article)
    return relevant_articles

# Dropdown for News section
with st.expander('News'):
    # Fetching the news
    all_news = newsapi.get_everything(q=ticker, language='en', sort_by='relevancy', page_size=50)
    filtered_news = filter_relevant_news(all_news['articles'], ticker)

    if filtered_news:
        st.header(f'Related News')
        for article in filtered_news[:10]:  # Display top 10 relevant articles
            if article['title'] and article['description'] and article['url']:
                st.subheader(article['title'])
                st.write(article['description'])
                st.markdown(f"[Read more]({article['url']})")
            else:
                st.write("Some news articles could not be displayed due to missing information.")
    else:
        st.write(f"No relevant news articles found for {ticker}.")


# Compare section
st.header('Compare Stocks')

ticker2 = st.text_input('Enter Ticker 2', '').upper()

# Compare button
compare_button = st.button('Compare')

# Handle Compare button click
if compare_button:
    if ticker2:
        # Display comparison chart
        fetch_and_display_comparison(ticker, ticker2, start_date, end_date)
    else:
        st.warning('Please enter Ticker 2 to compare.')