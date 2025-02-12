import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class BreakoutScanner:
  def __init__(self, df, 
               min_breakout_hold = 5, 
               min_consolidation_period = 9,
               maximum_consolidation_range = 5,
               min_increase_from_range = 10,
               n_preceeding_days = 65,
               n_succeeding_days = 10
               ):
    self.history = df
    self.min_breakout_hold = min_breakout_hold
    self.min_consolidation_period = min_consolidation_period
    self.maximum_consolidation_range = maximum_consolidation_range
    self.min_increase_from_range = min_increase_from_range
    self.n_preceeding_days = n_preceeding_days
    self.n_succeeding_days = n_succeeding_days
    
  def is_consolidating(self, current_df):
    recent_candlesticks = current_df[-self.min_consolidation_period:]
    
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()
    
    treshold = 1 - (self.maximum_consolidation_range / 100)
    if min_close > (max_close * treshold):
      return True
    
    return False
  
  def is_breaking_out(self, current_df, ahead_df):
    last_close = ahead_df[['Close']].mean()[0]
    
    treshold = 1 + (self.min_increase_from_range / 100)
    if self.is_consolidating(current_df[:-1]):
      recent_closes = current_df
      if last_close > (recent_closes['Close'].max() * treshold):
        return True
      
    return False

  def get_breakouts(self):
    df = self.history    
    to_return = []

    for i in range((self.min_consolidation_period + 1), len(df)):
      current_window = df[i-self.min_consolidation_period:i-1]
      ahead_window = df[i:i+self.min_breakout_hold]
      
      if self.is_breaking_out(current_window, ahead_window):
        breakout_day = df[['Close']].iloc[[i-1]].values[0][0]
        preceding_day = df[['Close']].iloc[[i-2]].values[0][0]
        
        to_return.append(
            df[['Close', 'Open', 'Low', 'High', 'Volume']][i-self.n_preceeding_days:i+self.n_succeeding_days]
          )
        
    return to_return