import pandas as pd
from table2ascii import preset_style, table2ascii, PresetStyle,  Alignment
from pathlib import Path
from typing import List, Union
import logging

## https://table2ascii.readthedocs.io/en/latest/usage.html

def to_ascii(df,first_col_heading: bool=True, style=PresetStyle.double_compact, **kwargs):
    '''
    discord friendly table 
    '''
    data = df.to_dict(orient = 'split')
    table = table2ascii(
        header=data['columns'],
        body=[list(map(str, x)) for x in data['data']],
        first_col_heading=first_col_heading,
        style=style,
        **kwargs
    ) 
    return f"```\n{table}\n```"
    
def validate_symbols(symbols: Union[str, list], valid_list:list ) -> List:
    validated_list = []
    if isinstance(symbols, str):
        symbols = [symbols]
    for symbol in map(str.upper, symbols):
        if symbol in valid_list:
            validated_list.append(symbol)
        else:
            logging.info(f'{symbol} is not validated symbol')
    return validated_list

   