import requests
from dotenv import load_dotenv
import os
import pandas as pd

class Nomics:
    #API docs can be found here: https://api.nomics.com/
    ## https://www.youtube.com/watch?v=0ZJwW395viQ&ab_channel=CodePalace
    def __init__(self , base_currency: str='USD', assets: str='BTC,ETH,SHIB', interval: str='1d'):
        self.url = 'https://api.nomics.com/v1/currencies/ticker'
        self.assets = assets
        self.base_currency = base_currency
        self.interval = interval
        self.payload = {
                'key': os.environ['NOMICS_TOKEN'],
                'convert': self.base_currency,
                'ids': self.assets,
                'interval': self.interval
            }
     
    @property
    def get_assets(self):
        reponses = requests.get(self.url, params=self.payload)
        if reponses.status_code == 200:
            return reponses.json()
        else:
            raise ValueError('something went wrong!! please check the doc at https://api.nomics.com/')

    def get_crypto_price(self, columns: list=['symbol', 'name', 'price', 'price_timestamp']):
        df = pd.DataFrame(self.get_assets).loc[:,columns]
        return df.apply(pd.to_numeric, errors='ignore' )


    