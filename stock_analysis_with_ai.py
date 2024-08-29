#!/usr/bin/env python
# coding: utf-8
# Rocketseat - IA na Pratica | 08/2024
import json
import os
from datetime import datetime, timedelta

# import yfinance as yf
# from yfinance_tools import [yahoo_finance_tool, llm, search_tool]
import yfinance_tools
import crew_agents
import crew_tasks
from crewai import Crew, Process
# from langchain.tools import Tool
# from langchain_openai import ChatOpenAI
# from langchain_community.tools import DuckDuckGoSearchResults
import streamlit as st

# Create Yahoo Finance Tool
# def fetch_stock_price(ticker):
#     today = datetime.today().date()
#     five_years_ago = today - timedelta(days=1825)
#     # stock_data = yf.download(ticker, start="2020-01-01", end="2024-08-15")
#     stock_data = yf.download(ticker, start = five_years_ago.strftime("%Y-%m-%d"), end = today.strftime("%Y-%m-%d"))
#     return stock_data

# yahoo_finance_tool = Tool(
#     name = "Yahoo Finance Tool",
#     description = "Fetches stock prices for {ticker} from past years from a specific company (from Yahoo Finance API).",
#     func = lambda ticker: fetch_stock_price(ticker)
#     )

# # Import OpenAI LLM-GPT (LLM = Large Language Model)
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# # Assign LLM
# llm = ChatOpenAI(model = "gpt-3.5-turbo")

# # Create Search tool
# search_tool = DuckDuckGoSearchResults(backend = 'news', num_results = 10)

# # Create Agents:
# # --------------------------
# # stock_price_analyst
# # news_analyst
# # stock_analyses_writer
# stock_price_analyst = Agent(
#     role = "Senior stock price Analyst",
#     goal = "Find the {ticker} stock price and analyses trends",
#     backstory = """You're highly experienced in analyzing the price of an specific stock
#     and make predictions about its future price.""",
#     verbose = True,
#     llm = yfinance_tools.llm,
#     max_iter = 5,
#     memory = True,
#     tools = [yfinance_tools.yahoo_finance_tool],
#     allow_delegation = False,
#     )

# news_analyst = Agent(
#     role = "Stock News Analyst",
#     goal = """Create a short summary of the market news related to the stock {ticker} company. 
#     Specify the current trend - up, down or sideways with
#     the news context. For each request stock asset, specify a numbet between 0 and 100, 
#     where 0 is extreme fear and 100 is extreme greed.""",
#     backstory = """You're highly experienced in analyzing the market trends and news
#     and have tracked assest for more then 10 years.

#     You're also master level analyts in the tradicional markets and have deep understanding of human psychology.

#     You understand news, theirs tittles and information, but you look at those with a health dose of skepticism. 
#     You consider also the source of the news articles.""",
#     verbose = True,
#     llm = yfinance_tools.llm,
#     max_iter = 10,
#     memory = True,
#     tools = [yfinance_tools.search_tool],
#     allow_delegation = False,
#     )

# # allow_delegation -> can delegate Tasks to the other Agents, as it uses them
# stock_analyses_writer = Agent(
#     role = "Senior Stock Analyts Writer",
#     goal = """"Analyze the trends price and news and write an insighfull compelling and informative 3 paragraph long newsletter based on the stock report and price trend. """,
#     backstory = """You're widely accepted as the best stock analyst in the market. You understand complex concepts and create compelling stories and narratives that resonate with wider audiences. 

#     You understand macro factors and combine multiple theories - eg. cycle theory and fundamental analyses. 
#     You're able to hold multiple opinions when analyzing anything.""",
#     verbose = True,
#     llm = yfinance_tools.llm,
#     max_iter = 5,
#     memory = True,
#     allow_delegation = True,
#     )

# # Create Tasks:
# # get_stock_prices
# # get_news
# # write_stock_prices_analysis
# get_stock_prices = Task(
#     description = """Analyzes the stock {ticker} price history and creates a trend up, down or sideways analysis""",
#     expected_output = """"Specify the current trend stock price - up, down or sideways, eg. stock= 'APPL, price UP'""",
#     agent = stock_price_analyst,
#     )

# get_news = Task(
#     description = """Takes the stock and always include BTC to it (if not requested).
#     Uses the search tool to search each one individually. 

#     The current date is {datetime.now()}.

#     Composes the results into a helpfull report.""",
#     expected_output = """"A summary of the overall market and one sentence summary for each request asset. 
#     Includes a fear/greed score for each asset based on the news. Use format:
#     <STOCK ASSET>
#     <SUMMARY BASED ON NEWS>
#     <TREND PREDICTION>
#     <FEAR/GREED SCORE>""",
#     agent = news_analyst,
#     )

# # Pass the context with activities (tasks) employed by the other agents, as described in its description
# write_stock_prices_analysis = Task(
#     description = """Uses the stock price trend and the stock news report to create an analyses and write the newsletter about the {ticker} company that is brief and highlights the most important points.
#     Focus on the stock price trend, news and fear/greed score. What are the near future considerations?
#     Include the previous analyses of stock trend and news summary.""",
#     expected_output = """"An eloquent 3 paragraphs newsletter formated as markdown in an easy readable manner. 
#     It should contain:
#     - 3 bullets executive summary 
#     - Introduction - set the overall picture and spike up the interest
#     - Main part provides the meat of the analysis including the news summary and fead/greed scores
#     - Summary - key facts and concrete future trend prediction - e.g. up, down or sideways.""",
#     agent = stock_analyses_writer,
#     context = [get_stock_prices, get_news,],
#     )

# Create Crew
crew = Crew(
    agents = [crew_agents.stock_price_analyst, crew_agents.news_analyst, crew_agents.stock_analyses_writer],
    tasks = [crew_tasks.get_stock_prices, crew_tasks.get_news, crew_tasks.write_stock_prices_analysis],
    verbose = 2,
    process = Process.hierarchical,
    full_output = True,
    share_crew = False,
    manager_llm = yfinance_tools.llm,
    max_iter = 15
    )

# results = crew.kickoff(inputs={'ticker': 'BBAS3.SA'})

with st.sidebar:
    st.header('Research Stock by Ticker')

    with st.form(key = 'research_form'):
        topic = st.text_input("Select the ticker")
        submit_button = st.form_submit_button(label = "Research")
if submit_button:
    if not topic:
        st.error("Please, fill in the ticker field...")
    else:
        results = crew.kickoff(inputs = {'cpny_ticker': topic})

        st.subheader("Research Results:")
        st.write(results['final_output'])