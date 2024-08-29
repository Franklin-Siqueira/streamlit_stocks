# Copyright 2024 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0
import yfinance as yf

from datetime import datetime, timedelta
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults

# Create Yahoo Finance Tool
def fetch_stock_price(cpny_ticker):
    today = datetime.today().date()
    five_years_ago = today - timedelta(days=1825)
    # stock_data = yf.download(cpny_ticker, start="2020-01-01", end="2024-08-15")
    stock_data = yf.download(cpny_ticker, start = five_years_ago.strftime("%Y-%m-%d"), end = today.strftime("%Y-%m-%d"))
    return stock_data

yahoo_finance_tool = Tool(
    name = "Yahoo Finance Tool",
    description = "Fetches stock prices for {cpny_ticker} from past years from a specific company (from Yahoo Finance API).",
    func = lambda cpny_ticker: fetch_stock_price(cpny_ticker)
    )

# Import OpenAI LLM-GPT (LLM = Large Language Model)
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Assign LLM
llm = ChatOpenAI(model = "gpt-3.5-turbo")

# Create Search tool
search_tool = DuckDuckGoSearchResults(backend = 'news', num_results = 10)