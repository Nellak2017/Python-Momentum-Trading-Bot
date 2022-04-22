# This is the entry point for the Stock Trading bot. It will analyze a stock, then email me the results
'''
main -> analyze a given stock using a backtested algo, when the stock hits certain indicators, email me the analysis

strategies folder -> a list of strategies to be tested;
    test -> test strategies with Unit Testing and Integration Testing ;
    back_testing -> analyze to see what is best

display folder -> all the display methods;
    test -> test display with Unit and Integration Testing
    ema_list  -> exponential moving average data points for a given dataset and given interval and given precision
    data_collector -> collect stock data for a given stock or crypto and given interval and given precision
    data_generator -> randomly generate a time series and given interval and given precision
    data_display -> display the data using a line graph
    strat_display -> display the effectiveness of different strategies in the terminal (lazy but effective)

'''
import numpy as np
import pandas as pd
import requests