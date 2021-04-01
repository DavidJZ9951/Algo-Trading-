#!/usr/bin/env python
# coding: utf-8

# In[62]:


import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np
# import modules 


# In[4]:


# get the asset : case example: Tesla
asset = 'TSLA'


# In[12]:


tsla_ret = yf.download(asset)
#- TSLA: 1m data not available for startTime=1277818200 and endTime=1617219632. 
#Only 7 days worth of 1m granularity data are allowed to be fetched per request.


# In[10]:


tsla_ret
# the total life span of tesla data


# In[47]:


# now choose a specific range of date that we want for the back testing 
tsla_int = yf.download(asset,start = '2021-03-02', end = '2021-03-30', interval = '1h')
# given that the data was not definable given the already downloaded format, we have to reassign the value of the return.
#TSLA: Invalid input - interval=1s is not supported. 
#Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
# the above notification given that the smallest time frame that we can use for backtesting is the 1m
# also for the one minutes return data only the last 30 days of data is avaliable for the use


# In[48]:


tsla_int


# In[49]:


tsla_int.iloc[120:,]# example of using the iloc funtion to find the first row of data


# In[50]:


tsla_int.iloc[0].Open# we can use ".VariableName" to assign the specific value that we want from the data sample


# In[72]:


## define the function for trend
def Intradaytrend(df,entry, exit):#df: dataframe( containing the intrady return), entry: entry condition, exit: exit condition)#
    T = df.shape[0]
    for t in [0,T]:
    # get the return after two hours which is 120 minutes
        ret_4h = df.iloc[t].Open/df.iloc[t-4].Open - 1 # get the return 
    #take the data frame, find the 120th row, find its opening price
    
    # now we need to have the relative changes in every minutes
        tickret = df.Open.pct_change()
    
    #now set the buying condition
        if ret_4h > entry:
            buyprice = df.iloc[t+1].Open
            buytime = df.iloc[t+1].name# as the name is the timestamp of the data
        
        # now we need to cummulated the return of the asset
            cummulated = (tickret.loc[buytime:]+1).cumprod() - 1
        # take all the return from the buytime on
        # logic of the cummulate return
        
        # now set the exit position
            exittime = cummulated[(cummulated < -exit) | (cummulated > exit)].first_valid_index()
        #  "|" means "or" , "first_valid_index" means to get the first valid index given the boolean condition in the front
        # exit is a condition that we assign for the function.
        # for this fucntion we need to defined level of entry point and exit point
        
        
        # there will be a situation that there will not be exit time, eg: a case where the asset is not moving
            if exittime == None:
                exitprice = df.iloc[-1].Open
            # given the case that the stock is not moving, so by the end of the day, given the intraday trading strategy
            # we will have to exit the postition
            else:
                exitprice = df.loc[exittime + dt.timedelta(hours = 1)].Open
            # this is the case when the stock price does move, (given the boolean condition that we don't have a nontype)
            # so for this situation, it means , when the exit situation satisifies, exit the position in the next minute bar 
            # open price
            profit = exitprice - buyprice
            profitrel = profit/buyprice
            return profitrel
        else:
            return None


# In[73]:


profit = Intradaytrend(tsla_int, 0.01, 0.01)
# as the entry point shows, what we have here is the entry condition that has 0.01 which is 1%, 
# as we also have the 0.01 , 1% as the exit point
# so far out strategy is the long only strategy


# In[74]:


print(profit)


# In[119]:


# test the strategy ( backtesting) over a month
# first create a frames that we store the data
frames = []


# In[124]:


# insert value for the frame
# first we need to get the value
# obtain the asset data from 03-08 to 03-31
dataframes = yf.download(asset, start= '2021-03-08', end = '2021-04-01')


# In[125]:


dataframes


# In[126]:


# for the time in the dataframes
# we can obatin it through indentrifing the index
dataframes.index


# In[128]:


# given that we have specify the frames that we want to use
# inser the value from the dataframes to the frames 
# using loop
for i in dataframes.index:
    frames.append(yf.download(asset, start = i, end = i+dt.timedelta(days = 1),interval = '1m'))


# In[129]:


frames


# In[134]:


# now we calculate the return given the dataframe
returns = []
for i in frames:
    returns.append(Intradaytrend(i,0.01,0.02))


# In[135]:


returns


# In[136]:


pd.DataFrame(returns).mean()# calculate the mean return over every day


# In[137]:


pd.DataFrame(returns).sum()


# In[ ]:




