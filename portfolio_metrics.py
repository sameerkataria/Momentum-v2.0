import numpy as np
import pandas as pd


def mean_ret_A(data,duration):
    """
    Function returns tha annualized mean of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
        
    if duration == "M":
        return 12*np.mean(data)
    elif duration == "D":
        return 252*np.mean(data)
    elif duration == "W":
        return 52*np.mean(data)
    elif duration == "Y":
        return np.mean(data)
    


def sd_ret_A(data,duration):
    """
    Function returns tha annualized standard deviation of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
    if duration == "M":
        return np.sqrt(12)*np.std(data, ddof=1)
    elif duration == "D":
        return np.sqrt(252)*np.std(data,ddof=1)
    elif duration == "W":
        return np.sqrt(52)*np.std(data,ddof=1)
    elif duration == "Y":
        return np.std(data,ddof=1)

def sharpe_ratio_a(data,duration, rf=0):
    """
    Function returns tha annualized sharpe ratio of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    rf: Risk free rate for the period
    
    """
    return (mean_ret_A(data,duration)-rf)/sd_ret_A(data,duration)


def max_ddwn(data):
    
    """
    Function returns tha maximum drawdown of a strategy for a given time period
    Parameters:
    data: Time series of the return data    
    """
    
    wealth_indx = np.cumprod(1+data)
    previous_peaks = np.maximum.accumulate(wealth_indx)
    drawdown = (wealth_indx-previous_peaks)/previous_peaks
    ddn= min(drawdown)
    return abs(ddn)


def sd_ret_neg_A(data,duration):
    """
    Function returns tha annualized standard deviation of the negative returns in data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
    ret_neg=[ x for x in data if x<0]
    
    if duration == "M":
        return np.sqrt(12)*np.std(ret_neg,ddof=1)
    elif duration == "D":
        return np.sqrt(252)*np.std(ret_neg,ddof=1)
    elif duration == "W":
        return np.sqrt(52)*np.std(ret_neg,ddof=1)
    elif duration == "Y":
        return np.std(ret_neg,ddof=1)



def sortino_ratio(data,duration,rf=0):
    """
    Function returns tha annualized sortino ratio of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    rf: Risk free rate for the period
    
    """
    return (mean_ret_A(data,duration)-rf)/sd_ret_neg_A(data,duration)


def holding_return(data):
    """
    Function returns the holding period retun of the data
    Parameters:
    data: Time series of the return data
    
    """
    return((1+data).cumprod()[-1]-1)


def tear_sheet(data,freq="M", rf=0):

    """
    
    Function returns a dataframe of tear sheet on an annual basis
    Parameters:
    data: Time series of the return data. Date shoulld be datetime series
    freq: Frequency of the time series. Default steup as Monthly. Use "M" for monthly
    
    
    """
    
    data_n=data.copy(deep=True)

    data_n.loc[:,"year"]=data_n.iloc[:,0].apply(lambda x : x.year)

    unique_years=data_n["year"].unique().tolist()

    tear_sheet=[]
    
    for x in unique_years:
        yrs_data=data_n[data_n["year"]==x].iloc[:,1].values
        ## Assigning Variables to Components of tear sheet
        a = mean_ret_A(yrs_data, freq)
        b = sd_ret_A(yrs_data, freq )
        c = holding_return(yrs_data)
        d = sharpe_ratio_a(yrs_data,freq, rf)
        e = sortino_ratio(yrs_data, freq, rf)
        f = max_ddwn(yrs_data)

        tear_sheet.append([x,a,b,c,d,e,f])
    
    tear_sheet=np.array(tear_sheet)

    tear_sheet_disp=pd.DataFrame(data=tear_sheet, columns=["Year", "Avg Ret", "Volatility", "Cumulative Return", "Sharpe", "Sortino", "Max Drawdown"],)

    tear_sheet_disp["Year"]=tear_sheet_disp["Year"].astype("int64")

    return tear_sheet_disp


    


