# Copyright 2024 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0
from crewai import Task
import yfinance_tools
import crew_agents

# Create Tasks:
# get_stock_prices
# get_news
# write_stock_prices_analysis
get_stock_prices = Task(
    description = """Analyzes the stock {yfinance_tools.ticker} price history and creates a trend up, down or sideways analysis""",
    expected_output = """"Specify the current trend stock price - up, down or sideways, eg. stock= 'APPL, price UP'""",
    agent = crew_agents.stock_price_analyst,
    )

get_news = Task(
    description = """Takes the stock and always include BTC to it (if not requested).
    Uses the search tool to search each one individually. 

    The current date is {datetime.now()}.

    Composes the results into a helpfull report.""",
    expected_output = """"A summary of the overall market and one sentence summary for each request asset. 
    Includes a fear/greed score for each asset based on the news. Use format:
    <STOCK ASSET>
    <SUMMARY BASED ON NEWS>
    <TREND PREDICTION>
    <FEAR/GREED SCORE>""",
    agent = crew_agents.news_analyst,
    )

# Pass the context with activities (tasks) employed by the other agents, as described in its description
write_stock_prices_analysis = Task(
    description = """Uses the stock price trend and the stock news report to create an analyses and write the newsletter about the {yfinance_tools.ticker} company that is brief and highlights the most important points.
    Focus on the stock price trend, news and fear/greed score. What are the near future considerations?
    Include the previous analyses of stock trend and news summary.""",
    expected_output = """"An eloquent 3 paragraphs newsletter formated as markdown in an easy readable manner. 
    It should contain:
    - 3 bullets executive summary 
    - Introduction - set the overall picture and spike up the interest
    - Main part provides the meat of the analysis including the news summary and fead/greed scores
    - Summary - key facts and concrete future trend prediction - e.g. up, down or sideways.""",
    agent = crew_agents.stock_analyses_writer,
    context = [get_stock_prices, get_news,],
    )