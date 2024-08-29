# Copyright 2024 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

from crewai import Agent
import yfinance_tools

# Create Agents:
# --------------------------
# stock_price_analyst
# news_analyst
# stock_analyses_writer
stock_price_analyst = Agent(
    role = "Senior stock price Analyst",
    goal = "Find the {yfinance_tools.cpny_ticker} stock price and analyses trends",
    backstory = """You're highly experienced in analyzing the price of an specific stock
    and make predictions about its future price.""",
    verbose = True,
    llm = yfinance_tools.llm,
    max_iter = 5,
    memory = True,
    tools = [yfinance_tools.yahoo_finance_tool],
    allow_delegation = False,
    )

news_analyst = Agent(
    role = "Stock News Analyst",
    goal = """Create a short summary of the market news related to the stock {yfinance_tools.cpny_ticker} company. 
    Specify the current trend - up, down or sideways with
    the news context. For each request stock asset, specify a numbet between 0 and 100, 
    where 0 is extreme fear and 100 is extreme greed.""",
    backstory = """You're highly experienced in analyzing the market trends and news
    and have tracked assest for more then 10 years.

    You're also master level analyts in the tradicional markets and have deep understanding of human psychology.

    You understand news, theirs tittles and information, but you look at those with a health dose of skepticism. 
    You consider also the source of the news articles.""",
    verbose = True,
    llm = yfinance_tools.llm,
    max_iter = 10,
    memory = True,
    tools = [yfinance_tools.search_tool],
    allow_delegation = False,
    )

# allow_delegation -> can delegate Tasks to the other Agents, as it uses them
stock_analyses_writer = Agent(
    role = "Senior Stock Analyts Writer",
    goal = """"Analyze the trends price and news and write an insighfull compelling and informative 3 paragraph long newsletter based on the stock report and price trend. """,
    backstory = """You're widely accepted as the best stock analyst in the market. You understand complex concepts and create compelling stories and narratives that resonate with wider audiences. 

    You understand macro factors and combine multiple theories - eg. cycle theory and fundamental analyses. 
    You're able to hold multiple opinions when analyzing anything.""",
    verbose = True,
    llm = yfinance_tools.llm,
    max_iter = 5,
    memory = True,
    allow_delegation = True,
    )