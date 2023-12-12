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

class processing_data:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_nifty = pd.read_csv("nifty50_tickers.csv")
        self.ticker_list = [s + '.NS' for s in self.tickers_nifty['Ticker'].to_list()]
    
    def download_data(self):
        self.df = yf.download(" ".join(self.ticker_list), start=self.start_date,
                              end=self.end_date, interval="1d", ignore_tz=True)["Adj Close"]
        self.df.index = pd.to_datetime(self.df.index)
    
    def preprocess_data(self):
        self.df = self.df.resample("M", label="right").last()
        self.daily_data = pd.melt(self.df, ignore_index=False).reset_index()
        self.daily_data.rename(columns={"value": "Adj Close", "variable": "Ticker"}, inplace=True)
        self.daily_data["Return"] = self.daily_data.groupby("Ticker")["Adj Close"].pct_change()
        self.daily_data = self.daily_data.drop(columns=['Adj Close'])
        self.daily_data = self.daily_data.dropna()
        self.daily_data = self.daily_data.reset_index(drop=True)

    def get_data(self):
        self.download_data()
        self.preprocess_data()
        return self.daily_data