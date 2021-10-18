from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd 
from pathlib import Path
from typing import List, Union
import numpy as n

from finvizfinance.quote import finvizfinance
from finvizfinance.news import News
from finvizfinance.insider import Insider
from finvizfinance.screener.overview import Overview
from stocky import config  

basedir  = Path(__file__).parent

def load_symbols(asset_class: str) -> list:
    '''
    load symbols of assets
    '''
    stocklist = basedir / 'assets' / 'companylist.csv'
    cryptolist = basedir / 'assets' / 'cryptolist.csv'
    if not stocklist.exists() or not cryptolist.exists():
        raise ValueError('Please run stocky/update_assets.py first')
    if asset_class == 'stocks':
        return pd.read_csv(stocklist)['Symbol'].values
    elif asset_class == 'crypto':
        return pd.read_csv(cryptolist)['Symbol'].values
    else:
        raise ValueError(f'{asset_class} is an invaided asset_class. Options: ["stocks", "crypto"] ')


def stockprice(symbols: Union[List[str], str], period: str='ytd', 
    inveral: str='1d', prepost: bool=True, rounding: int=2,  **kwargs):
    if isinstance(symbols, list):
        symbols = ' '.join(symbols)
    
    df = yf.download(symbols,period=period, inveral=inveral, prepost=prepost, rounding=rounding, **kwargs)
    return df

def last_stock_price(symbols: list) -> pd.DataFrame:

    df = stockprice(symbols, inveral='1m', period='5d')
    df = df.reset_index()
    if len(symbols) ==1:
        df['symbol'] = symbols[0]
        return df.iloc[-1,][["Date", "Close", 'Volume']].rename(symbols[0]).reset_index()
    df = df[["Date", "Close", 'Volume']].iloc[-1,].unstack() ## get the last row
    return df.reset_index()


def top_owner_trade(option: str='top owner trade') -> pd.DataFrame:
    '''
    Show insider traders
    option: latest, top week, top owner trade
    default: latest
    '''
    return Insider(option='top owner trade').getInsider()


def get_news() -> pd.DataFrame:
    '''
    Get general new 
    '''
    return News().getNews()['news'].head(10)


def get_stock_new(symbol) -> pd.DataFrame:
    '''
    Get news specific to the stock 
    '''
    stock = finvizfinance(symbol)
    return stock.TickerNews()
    
def get_chart(symbol) -> Path:
    '''
    Download chart from finvis
    return: Chart path
    '''
    stock = finvizfinance(symbol)
    stock.TickerCharts(out_dir=config.CHARTPATH)
    
    return Path(config.CHARTPATH) / f'{symbol}.jpg'

def get_stock_description(symbol) -> str:
    stock = finvizfinance(symbol)
    return stock.TickerDescription()

def get_stock_rating(symbol) -> pd.DataFrame:
    stock = finvizfinance(symbol)
    return stock.TickerOuterRatings()

def get_stock_(symbol) -> list:
    stock = finvizfinance(symbol)
    return stock.TickerSignal()


