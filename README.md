# Courses

# 1. Financial Analytics 
The following assignments were part of the Executive Development Program offered from XLRI, Jamshedpur.
   
1. Assignment - 1 : Create an optimum portfolio of stocks from a group of 25 to 30 stocks after doing cluster analysis on their monthly returns, 
   assuming a five year time-frame, a risk free rate of 7 % and that short-selling is not allowed. 

2. Assignment - 2 : Write a function in R which accepts an xts-vector and relevant arguments and performs backtesting of any specific trading rule 
   ( Relative Strength Index or Bollinger Bands ) and returns the Sharpe Ratio as output. 

3. Assignment - 3 : Build a probability of default model using logistic or k-nearest neighbourbood algorithm, post exploratory data analysis on a 
   on a loan dataset. 

# 2. Business Statistics and Analysis 
The following assignments were part of the Capstone Project from the Business Statistics and Analysis Specialization 
offered by Rice University through Coursera. 

1. Capstone Assignment 1 : Develop a Regression Model for Market Value of Housing Units based on data provided for the year 2013. 

2. Capstone Assignment 2 : Use the model developed in the previous capstone assignment with modifications to variables ( if required ) and predict
   market value of housing units for the year 2013. 

# 3. Computational Investing 
The following problems were part of various quizzes from the Computational Investing course offered 
by Georgia Institute of Technology through Coursera. Please note that many functions have been re-used 
from the QSTK codebase ( https://pypi.org/project/QSTK/ )

1. Assignment - 1 : 
   This assignment has two parts to it - 

   a. Simulate the performance of a 4 stock portfolio in an excel spreadsheet and compare it to index returns. The stocks 
      to be taken are AAPL, XOM, GOOG and GLD. The index to be selected is S & P 500. Try out different weights for allocations and 
      display metrics for portfolio after assigning allocation weights. 

   b. Convert the above spreadsheet into a Python script and extend it to identify optimal allocations for any 4 stock portfolio. 

2. Assignment - 2
   Create an event study profile of a specific 'known' event on S & P 500 stocks and compare its impact on two groups of stocks. The 
   event is defined when the actual close of the stock price drops below $x, more specifically, when:
   
   price[t-1] >= $x
   price[t] < $x

   Evaluate this event for the time period, January 1, 2008 to December 31, 2009. Compare the results on two lists of S & P 500 stocks:
   a. Stocks that were in S & P 500 in 2008
   b. Stocks that were in S & P 500 in 2012

3. Assignment - 3 
   This assignment has two parts to it - 

   a. Create a market simulation tool, marketsim.py, that takes a command line like this - 
      python marketsim.py investment orders.csv values.csv
 
      where, 
      investment = Initial Investment
      orders.csv = List of orders with fields - Year, Month, Day, Symbol, Buy or Sell, No. of Shares
      values.csv = List of dates with corresponding portfolio value

   b. Create a portfolio analysis tool, analyze.py that takes a command like this - 
      python analyze.py values.csv $SPX

      The tool should read in daily values ( cumulative portfolio value) from values.csv and plot them. It should use the symbol on 
      the command line as a benchmark for comparison. Using this information, analyze.py should :
      i. Plot the price history over the trading period 
      ii. Output the following metrics - 
          a. Standard deviation of daily returns of the portfolio 
          b. Average daily returns of the total portfolio
          c. Sharpe Ratio of the portfolio ( Assuming 252 trading days and risk free rate = 0 )
          d. Cumulative return of the portfolio 
      

4. Assignment - 5 :
   This assignment has two parts to it - 

   a. Implment Bollinger Bands as an indicator using 20 days look back. The code should generate charts showing the rolling mean, the stock 
      price and upper and lower bands. The upper band should represent the mean plus one standard deviation and lower band is mean minus 
      one standard deviation. 

   b. The code should output the indicator value in a range of -1 to 1. +1 represents the situation where the price is at +1 standard deviations
      above the mean and -1 indicates the situation where the price is -1 standard deviations below the mean. 

5. Assignment - 6 :
   This assignment has two parts to it - 
   
   a. Implement Bollinger bands as an indicator using a 20 day look back. The upper band should represent mean plus one standard deviation and 
      the lower band is the mean minus one standard deviation. 

   b. Create an event study with the signal being:
      Bollinger value for equity today < x
      Bollinger value for equity yesterday >= y
      Bollinger value for SPY today >= z
   