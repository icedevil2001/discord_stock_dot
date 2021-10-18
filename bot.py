from re import A
import discord
from discord import embeds
from dotenv import load_dotenv
from discord.ext import commands
from os import environ
from finvizfinance.quote import finvizfinance
import pandas as pd
from pandas._config import config
from stocky.config import EMBED_COLOR

from stocky.misc import to_ascii, validate_symbols
# from stocky.stocky import load_symbols, last_stock_price
from stocky.cryptopy import Nomics 
# from stocky import config
from stocky import stocky

## https://github.com/gordwest/DiscordStockBot/blob/master/bot.py

## Example of background task:
## https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py
## https://stackoverflow.com/questions/63769685/discord-py-how-to-send-a-message-everyday-at-a-specific-time

## https://realpython.com/how-to-make-a-discord-bot-python/ 
print(dir(stocky))
stock_list = stocky.load_symbols('stocks')
crypto_list = stocky.load_symbols('crypto')
# EMBED_COLOR = 0x32a0a8

load_dotenv()
bot = commands.Bot('.')
## remove default help. will make own one
bot.remove_command('help') 


@bot.command()
async def help(ctx):
    '''
    List the helper functions
    '''
    msg = discord.Embed(title='Bot commands', color=0xCDCDCD)
    msg.add_field(name='!search <symbol>', value='Stock information', inline=False)
    
    msg.add_field(
        name='!watch <symbol> <gt|ls> <price> <tag|prefix>',
        value='Get an alet when stock or alert is greater/less than set price',
        inline=False)
    msg.add_field(
        name='!price <symbols>',
        value='Price of stock/crypto. More than on symbol can be given',
        inline=False)
    msg.add_field(
        name='!create ',
        value='Create portfolio',
        inline=False)
    msg.add_field(
        name='!add <symbol> <price> <unit>',
        value='Add a stock/crypo to your portfolio',
        inline=False)
    msg.add_field(
        name='!show ',
        value='Show your portfolio',
        inline=False)
    await ctx.send(embed=   msg)

# @bot.command
# async def get(ctx, *, symbols):
#     pass 

## https://stackoverflow.com/questions/52343245/python-dm-a-user-discord-bot
@bot.command()
async def dm(ctx, user: discord.User, *, message=None):
    if message == None:
      message = "Hi!"
    embed = discord.Embed(title=f"Sent by {user}", desc=message)
    print(user, dir(user))
    await user.send(embed=embed)
    await ctx.send("Message sent!")

@bot.command()
async def price(ctx, *, symbols):
    stocksymbols = validate_symbols(symbols.strip().split(), stock_list)
    cryptlist = validate_symbols(symbols.strip().split(), crypto_list)
    print(symbols, type(symbols))
    if len(stocksymbols)>=1:
        data = stocky.last_stock_price(stocksymbols)
        await ctx.send(to_ascii(data))
    elif len(cryptlist) >=1:
        data = Nomics(assets=','.join(cryptlist)).get_crypto_price()
        print(data)
        await ctx.send(to_ascii(data))
    else:
        await ctx.send(f'No assets found!')

def fv_checker(symbol: str) -> str:
    symbol = symbol.upper()
    stocksymbols = validate_symbols(symbol, stock_list)
    return (stocksymbols[0])

@bot.command()
async def chart(ctx, symbol):
    symbol = fv_checker(symbol)
    chart_path = stocky.get_chart(symbol)
    await ctx.send(file=discord.File(chart_path))
    
@bot.command(name='desc')
async def description(ctx, symbol):
    symbol = fv_checker(symbol)
    desc = stocky.get_stock_description(symbol)
    msg = discord.Embed(
        title=f'Stock description: {symbol}', 
        type='rich',
        description=desc,
        inline=True, 
        color=stocky.config.EMBED_COLOR)
    await ctx.send(embed=msg)

@bot.command()
async def all_news(ctx):
    msg = discord.Embed(
        title = 'Recent First 10 News',
        color=stocky.config.EMBED_COLOR
    )
    for _, dfx in stocky.get_news().iterrows():
        msg.add_field(
            name = dfx['Title'],
            value= f'[Click here!]({dfx["Link"]})',
            inline =False
        )

    await ctx.send(embed=msg)

@bot.command()
async def test(ctx):
    msg = discord.Embed(
        title = f'General news',
        type='rich',
        url='https://google.com',
        color=stocky.config.EMBED_COLOR
    )
    msg.add_field(
        name ='[awesome news](http://google.com)',
        value=' ..',
        # value='[chick here](http://google.com)',
        inline=False
    )
    msg.add_field(
        name ='awesome news 1',
        value = 'http://google.com',
        inline=False
    )

    # d= '```[google](http://google.com)```'
    await ctx.send(embed=msg)
    # df = pd.DataFrame({'A': range(3), "B": list('ABC')})
    # msg = discord.Embed(title='Stock', color=0xCDCDCD)
    # table = to_ascii(df)

    # await ctx.send(table)

@bot.event
async def on_ready():
    '''
    let use know when the bot it ready
    '''
    print(f'Bot {bot.user.name} is online!')


bot.run(environ['DISCORD_TOKEN'])
    