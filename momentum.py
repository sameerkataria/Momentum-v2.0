import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import seaborn as sns
import monthdelta as md
from dateutil.relativedelta import relativedelta
import scipy.optimize as sco
import portfolio_metrics as pm
from tabulate import tabulate

class MomentumInvesting:
    def __init__(self, return_data, lookback_period, investment_period, buckets, weight_arg):
        self.lookback_period = lookback_period
        self.return_data = return_data
        self.investment_period = investment_period
        self.buckets = buckets
        self.weight_arg = weight_arg

    def generate_past_fut_ret(self):
        self.return_data.sort_values(["Ticker", "Date"], inplace = True)
        self.return_data['Date'] = pd.to_datetime(self.return_data['Date'])
        self.return_data['past_return'] = self.return_data.groupby('Ticker')['Return'].shift(1).rolling(self.lookback_period).mean()
        self.return_data['fut_return'] = self.return_data.groupby('Ticker')['Return'].transform(lambda x: (1+x).rolling(self.investment_period).apply(lambda y: y.prod()))-1
        self.return_data.dropna(inplace = True)
        self.return_data.reset_index(drop = True, inplace = True)
        self.return_data['investing_time_frame'] = self.return_data.groupby("Ticker").cumcount()+1
        self.return_data['investing_filter'] = self.return_data['investing_time_frame'] % self.investment_period
        if self.investment_period == 1:
            pass
        else:
            self.return_data = self.return_data[self.return_data['investing_filter']==1].copy(deep=True)
        self.return_data.dropna(inplace = True)
        self.return_data.reset_index(drop = True, inplace = True)
        self.return_data.drop(['investing_time_frame', 'investing_filter'], axis = 1, inplace = True)


    def bucketing_fun(self):
        self.return_data['buckets'] = self.return_data.groupby('Date')['past_return'].transform(lambda x: pd.qcut(x, self.buckets, duplicates='drop', labels=False))
        self.return_data_top = self.return_data[self.return_data["buckets"] == self.buckets-1].reset_index(drop=True)
        self.return_data_top.drop(['buckets'], axis = 1, inplace = True)
        
    def weight_fun(self):
        if self.weight_arg == 'Eq':
            self.mom_ret_data = pd.DataFrame(self.return_data_top.groupby("Date")["fut_return"].mean()).reset_index()
            self.mom_ret_data.rename(columns={"fut_return" :"Return" }, inplace=True)

        
    def mom_weight_fun(self):
        pass

    def plot_cumulative_returns(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.mom_ret_data["Date"], ((1 + self.mom_ret_data["Return"]).cumprod() - 1))
        plt.xticks(rotation=45, ha='right') 
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.title('Cumulative Returns Over Time')
        plt.show()

    def calculate_final_return(self):
        return ((1 + self.mom_ret_data["Return"]).cumprod() - 1).iloc[-1]

    def run_strategy(self):
        self.generate_past_fut_ret()
        self.bucketing_fun()
        self.weight_fun()
        print(tabulate(pm.tear_sheet(self.mom_ret_data, "M"), headers='keys', tablefmt='psql', showindex=False))
        self.plot_cumulative_returns()
        final_return = self.calculate_final_return()
        return final_return