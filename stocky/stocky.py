import yfinance as yf
import pandas as pd 
from pathlib import Path
from typing import List, Union
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

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

def last_stock_price(symbols: list):

    df = stockprice(symbols, inveral='1m', period='5d')
    df = df.reset_index()
    if len(symbols) ==1:
        df['symbol'] = symbols[0]
        return df.iloc[-1,][["Date", "Close", 'Volume']].rename(symbols[0]).reset_index()
    df = df[["Date", "Close", 'Volume']].iloc[-1,].unstack() ## get the last row
    return df.reset_index()


class FinVis:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.html = self.scraper(symbol)

    def scraper(self, symbol):
        ## https://medium.datadriveninvestor.com/scraping-live-stock-fundamental-ratios-news-and-more-with-python-a716329e0493
        # Set up scraper
        url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        return soup(webpage, "html.parser")

    def get_fundamentals(self):
        try:
            # Find fundamentals table
            fundamentals = pd.read_html(str(self.html), attrs = {'class': 'snapshot-table2'})[0]
            
            # Clean up fundamentals dataframe
            fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            colOne = []
            colLength = len(fundamentals)
            for k in np.arange(0, colLength, 2):
                colOne.append(fundamentals[f'{k}'])
            attrs = pd.concat(colOne, ignore_index=True)
        
            colTwo = []
            colLength = len(fundamentals)
            for k in np.arange(1, colLength, 2):
                colTwo.append(fundamentals[f'{k}'])
            vals = pd.concat(colTwo, ignore_index=True)
            
            fundamentals = pd.DataFrame()
            fundamentals['Attributes'] = attrs
            fundamentals['Values'] = vals
            fundamentals = fundamentals.set_index('Attributes')
            return fundamentals

        except Exception as e:
            return e
    
    def get_news(self):
        try:
            # Find news table
            news = pd.read_html(str(self.html), attrs = {'class': 'fullview-news-outer'})[0]
            links = []
            for a in self.html.find_all('a', class_="tab-link-news"):
                links.append(a['href'])
            
            # Clean up news dataframe
            news.columns = ['Date', 'News Headline']
            news['Article Link'] = links
            news = news.set_index('Date')
            return news

        except Exception as e:
            return e

    def get_insider(self):
        try:
            # Find insider table
            insider = pd.read_html(str(self.html), attrs = {'class': 'body-table'})[0]
            
            # Clean up insider dataframe
            insider = insider.iloc[1:]
            insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
            insider = insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
            insider = insider.set_index('Date')
            return insider

        except Exception as e:
            return e

fv = FinVis('AAPL')

print(fv.get_fundamentals())
print(fv.get_news())
print(fv.get_insider())