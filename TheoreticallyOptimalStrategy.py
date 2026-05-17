import datetime as dt
import pandas as pd

from util import get_data

def author():
    return 'ablanc6'

def study_group():
    return "ablanc6"

def testPolicy(symbol='JPM',
               sd=dt.datetime(2008,1,1),
               ed=dt.datetime(2009,12,31),
               sv=100000):
    """
    Generate a theoretically optimal set of trades.

    Parameters
    symbol : str
        Stock symbol to trade.
    sd : datetime
        Start date.
    ed : datetime
        End date.
    sv : int
        Starting portfolio value (not directly used in TOS logic,
        but included to match the required API).
    Returns
    df_trades : pandas.DataFrame
        Single-column DataFrame indexed by date.
        Values represent trades:
        +1000 = buy 1000 shares
        -1000 = sell 1000 shares
        +2000 / -2000 = flip position
        0 = do nothing
    """
    #Get price data for the date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)

    #Keep only the symbol column
    prices = prices_all[[symbol]].copy()

    #Create holdings DataFrame: desired position each day
    holdings = pd.DataFrame(index=prices.index, columns=[symbol], data=0)

    #Decide target holdings based on tomorrow's price
    for i in range(len(prices.index) - 1):
        today = prices.index[i]
        tomorrow = prices.index[i + 1]

        today_price = prices.loc[today, symbol]
        tomorrow_price = prices.loc[tomorrow, symbol]

        if tomorrow_price > today_price:
            holdings.loc[today, symbol] = 1000
        elif tomorrow_price < today_price:
            holdings.loc[today, symbol] = -1000
        else:
            holdings.loc[today, symbol] = 0
    #Last day: no future information, so go to cash
    holdings.iloc[-1, 0] = 0

    #Convert holdings to trades
    df_trades = holdings.copy()
    df_trades.iloc[0,0] = holdings.iloc[0,0]

    for i in range(1, len(holdings.index)):
        df_trades.iloc[i, 0] = holdings.iloc[i, 0] - holdings.iloc[i - 1, 0]
    return df_trades

if __name__ == "__main__":
    trades = testPolicy()

