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
import momentum as mom
import processing as pr

def main():
    startdate = "2015-01-01"
    enddate = "2023-10-31"
    data = pr.processing_data(startdate, enddate)
    df = data.get_data()
    lookback_period =  6 # Customize the lookback period here
    investment_period =  1 # Customize the lookback period here
    n_securities = 15
    momentum = mom.MomentumInvesting(df, lookback_period,
                                     investment_period, int(50/n_securities),
                                     "Eq"
                                     )
    abba = momentum.run_strategy()
    print(f"Cumulative Return from {startdate}"
          f" to {enddate} is {round(abba,2)*100}%"
          )
    

main()


