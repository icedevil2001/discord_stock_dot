import pandas as pd
import requests
from pathlib import Path
import logging

class IndicesList:
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    column_order  = ['Symbol', 'Company_name', 'Sector', 'Sub_industry']

    @property
    def get_sp500(self):
        '''
        pull S&P500 component stock from wikipeda
        '''
        df = pd.read_html(IndicesList.url)[0]
        usecol = ['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']
        df = df.loc[:,usecol]
        df = df.rename(
            columns={
                'Security': 'Company_name',
                'GICS Sector': 'Sector',
                'GICS Sub-Industry': 'Sub_industry'}
        )
        df = df[IndicesList.column_order]
        df.loc[:,['Indices', 'Country']] = 'sp500', 'USA'
        logging.info(f'Downloaded S&P 500, {df.shape} records')
        return df
    
    @property
    def get_ftse100(self):
        url  = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
        df = pd.read_html(url)[3]
        df = df.rename(
            columns={   
                'EPIC': 'Symbol', 
                'Company':'Company_name',
                'FTSE Industry Classification Benchmark sector[13]':'Sector'
            }
        )
        df.loc[:,'Sub_industry'] = pd.NA
        df = df[IndicesList.column_order]
        df.loc[:,['Indices', 'Country']] = 'ftse100', 'UK'
        logging.info(f'Downloaded FTSE 100, {df.shape} records')
        return df

    @property
    def get_ftse250(self):
        url = 'https://en.wikipedia.org/wiki/FTSE_250_Index'
        df = pd.read_html(url)[1]
        df = df.rename(
            columns={   
                'Ticker[4]': 'Symbol', 
                'Company':'Company_name',
            }
        )
        df.loc[:,['Sector', 'Sub_industry']] = pd.NA, pd.NA
        df = df[IndicesList.column_order]
        df.loc[:,['Indices', 'Country']] = 'ftse250', 'UK'
        logging.info(f'Downloaded FTSE 250, {df.shape} records')
        return df

class CryptoList:

    @property
    def get_crpto(self):
        url = 'https://en.bitcoinwiki.org/wiki/Cryptocurrency_list'
        column_order = ['Symbol', 'Name', 'Market Cap', 'Price', 'Circulating Supply']
        df = pd.read_html(url)[0].replace('-', pd.NA)
        df = df[column_order]
        df.loc[:,'Cryptocurrency'] = 'coin'
        logging.info(f'Downloaded Cryptocurrency Coin, {df.shape} records')

        return df

    @property
    def get_tokens(self):
        url = 'https://en.bitcoinwiki.org/wiki/Cryptocurrency_list'
        column_order  = ['Symbol', 'Platform', 'Market Cap', 'Price', 'Circulating Supply']
        df = pd.read_html(url)[1][column_order]
        df.loc[:,'Cryptocurrency'] = 'token'
        logging.info(f'Downloaded Cryptocurrency token, {df.shape} records')
        return df

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("update_asserts.log"),
            logging.StreamHandler()
        ]
    )
    basepath = Path(__file__).parent
    output = basepath / 'assets' 
    indices = IndicesList()
    crypto = CryptoList()
    
    df = pd.concat([getattr(indices, x,) for x in ['get_sp500', 'get_ftse100', 'get_ftse250']])
    df.to_csv(output / 'companylist.csv' , index=False)    
    logging.info(f'Download Stock list and saved {output / "companylist.csv"}')
    crypto.get_crpto.to_csv( output / 'cryptolist.csv', index=False)
    logging.info(f'Download Crypto list and saved {output / "cryptolist.csv"}')


if __name__ == "__main__":
    main()