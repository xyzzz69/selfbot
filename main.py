import dateutil

from dateutil import parser

from decouple import config

import re

import os

import discord

from discord.ext import commands, tasks

import json

import asyncio 

from pyfiglet import Figlet

from faker import Faker

from discord import Member

from asyncio import sleep 

from decouple import config

import re

import requests

import aiohttp

import random

import uuid

import psutil

import platform

import colorama

from colorama import Fore, Style

colorama.init()

intents = discord.Intents.default()

intents.voice_states = True

auto_messages = {}

def load_autoresponder_data():

    try:

        with open('autoresponder_data.json', 'r') as file:

            return json.load(file)

    except FileNotFoundError:

        return {}

def save_autoresponder_data(data):

    with open('autoresponder_data.json', 'w') as file:

        json.dump(data, file)

infection = int(config("userid"))

AUTHORIZED_USERS = [infection]  

bot = commands.Bot(command_prefix='.', self_bot=True, help_command=None, intents=intents)

fake = Faker()

def is_authorized(ctx):

    return ctx.author.id in AUTHORIZED_USERS

@bot.command()

@commands.check(is_authorized)

async def addar(ctx, trigger, *, response):

    autoresponder_data = load_autoresponder_data()

    autoresponder_data[trigger] = response

    save_autoresponder_data(autoresponder_data)

    await ctx.send(f'Autoresponder added: `{trigger}` -> `{response}`')

@bot.command()

@commands.check(is_authorized)

async def removear(ctx, trigger):

    autoresponder_data = load_autoresponder_data()

    if trigger in autoresponder_data:

        del autoresponder_data[trigger]

        save_autoresponder_data(autoresponder_data)

        await ctx.send(f'Autoresponder removed: `{trigger}`')

    else:

        await ctx.send('Autoresponder not found.')

@bot.command()

@commands.check(is_authorized)

async def listar(ctx):

    autoresponder_data = load_autoresponder_data()

    if autoresponder_data:

        response = 'Autoresponders:\n'

        for trigger, response_text in autoresponder_data.items():

            response += f'`{trigger}` -> `{response_text}`\n'

        await ctx.send(response)

    else:

        await ctx.send('No autoresponders found.')

@bot.command()

@commands.check(is_authorized)

async def spam(ctx, times: int, *, message):

    for _ in range(times):

        await ctx.send(message)

        await asyncio.sleep(0.1)      

@bot.command()

@commands.check(is_authorized)

async def calc(ctx, *, expression):

    try:

        result = eval(expression)

        await ctx.send(f'**{result}**')

    except:

        await ctx.send('Invalid expr')

@bot.command(aliases=['h'])

@commands.check(is_authorized)

async def help(ctx):

    command_list = bot.commands

    sorted_commands = sorted(command_list, key=lambda x: x.name)

    response = "# A L O N E S 3 L F B O T \n\n"

    for command in sorted_commands:

        response += f"_{command.name}_, "

    await ctx.send(response)

@bot.command()

@commands.check(is_authorized)

async def ping(ctx):

    

    latency = round(bot.latency * 1000)  

    

    await ctx.send(f'**~ {latency}ms is ur ping kiddo**')

@bot.command(aliases=['purge'])

@commands.check(is_authorized)

async def clear(ctx, times: int):

    channel = ctx.channel

    def is_bot_message(message):

        return message.author.id == ctx.bot.user.id

    

    messages = await channel.history(limit=times + 1).flatten()

    

    bot_messages = filter(is_bot_message, messages)

    

    for message in bot_messages:

        await asyncio.sleep(0.1)  

        await message.delete()

    await ctx.send(f"Deleted `{times}` messages like u said to.")

@bot.command(aliases=['cltc'])

@commands.check(is_authorized)

async def ltcprice(ctx):

    url = 'https://api.coingecko.com/api/v3/coins/litecoin'

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        price = data['market_data']['current_price']['usd']

        await ctx.send(f"The current price of Litecoin (LTC) is ${price:.2f}")

    else:

        await ctx.send("Failed to fetch Litecoin price")

@bot.command(aliases=['nitro'])

@commands.check(is_authorized)

async def fakenitro(ctx):

    

    nitro_months = random.randint(1, 12)

    

    fake_link = f"discord.gift/fakelinknthgmore-69M"

    

    await ctx.send(f"\n{fake_link}")

@bot.command()

async def bal(ctx, ltcaddress: str):

    # Litecoin blockchain explorer API endpoint for balance

    api_url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance'

    # Litecoin blockchain explorer API endpoint for total received

    total_received_url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}'

    # CoinGecko API endpoint for LTC to USD conversion

    coingecko_url = "https://api.coingecko.com/api/v3/simple/price"

    coingecko_params = {

        "ids": "litecoin",

        "vs_currencies": "usd"

    }

    try:

        # Fetch balance data from BlockCypher

        response = requests.get(api_url)

        balance_data = response.json()

        confirmed_balance_ltc = balance_data['balance'] / 10**8

        unconfirmed_balance_ltc = balance_data['unconfirmed_balance'] / 10**8

        # Fetch total received amount from BlockCypher

        response = requests.get(total_received_url)

        total_received_data = response.json()

        total_received_ltc = total_received_data['total_received'] / 10**8

        # Fetch LTC to USD conversion rate from CoinGecko

        response = requests.get(coingecko_url, params=coingecko_params)

        conversion_data = response.json()

        ltc_to_usd_rate = conversion_data['litecoin']['usd']

        # Calculate values in USD

        confirmed_balance_usd = confirmed_balance_ltc * ltc_to_usd_rate

        unconfirmed_balance_usd = unconfirmed_balance_ltc * ltc_to_usd_rate

        total_received_usd = total_received_ltc * ltc_to_usd_rate

        # Construct response as normal text message

        response_message = (

            f"**Litecoin Balance**\n\n"

            f"**Ltc Address** :- {ltcaddress}\n\n"

            f"**Confirmed Balance**\nLTC  :- {confirmed_balance_ltc:.2f}\nUSD :- ${confirmed_balance_usd:.2f}\n\n"

            f"**Unconfirmed Balance**\nLTC  :- {unconfirmed_balance_ltc:.2f}\nUSD :- ${unconfirmed_balance_usd:.2f}\n\n"

            f"**Total LTC Received**\nLTC  :- {total_received_ltc:.2f}\nUSD :- ${total_received_usd:.2f}\n"

            f"Requested by {ctx.author.name}"

        )

        await ctx.reply(response_message)

    except Exception as e:

        error_message = f"An error occurred: {type(e).__name__} - {e}"

        await ctx.send(error_message)

@bot.command(name='checkpromo', aliases=['promo'], brief="Check promos", usage=".checkpromo <check.promo>")

async def checkpromo(ctx, *, promo_links: str):

    await ctx.message.delete()

    if not isinstance(promo_links, str):

        await ctx.send("Enter promos", delete_after=5)

        return

    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:

        for link in links:

            try:

                promo_code = extract_promo_code(link)

                if promo_code:

                    result = await check_promo(session, promo_code)

                    await ctx.send(result)

                else:

                    await ctx.send(f'Invalid promo link: {link}')

            except Exception as e:

                await ctx.send(f'An error occurred while processing the link: {link}. Error: {str(e)}')

async def check_promo(session, promo_code):

    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    try:

        async with session.get(url) as response:

            if response.status in [200, 204, 201]:

                data = await response.json()

                if "uses" in data and "max_uses" in data and data["uses"] == data["max_uses"]:

                    return f'Already Claimed: {promo_code}'

                elif "expires_at" in data and "promotion" in data and "inbound_header_text" in data["promotion"]:

                    exp_at = data["expires_at"].split(".")[0]

                    parsed = parser.parse(exp_at)

                    unix_timestamp = int(parsed.timestamp())

                    title = data["promotion"]["inbound_header_text"]

                    return f'Valid: {promo_code}\nExpires At: <t:{unix_timestamp}:R>\nOffer: {title}'

            elif response.status == 429:

                retry_after = response.headers.get("retry-after", "Unknown")

                return f'Rate Limited for {retry_after} seconds'

            else:

                return f'Invalid Code Try New one -> {promo_code}'

    except Exception as e:

        return f'An error occurred while checking the promo code: {promo_code}. Error: {str(e)}'

def extract_promo_code(promo_link):

    try:

        promo_code = promo_link.split('/')[-1]

        return promo_code

    except Exception as e:

        return None

@bot.event

async def on_ready():

    print(f'{Fore.GREEN}Selfbot connected as {bot.user.name}{Style.RESET_ALL}')

    print(f'{Fore.YELLOW}Dev: alone_aaroosh {Style.RESET_ALL}')

    print(f'{Fore.CYAN}Version: Ur mom{Style.RESET_ALL}')

    print(f'{Fore.MAGENTA}Server: https://discord.com/invite/7sxtvPXPHk{Style.RESET_ALL}')

@bot.event

async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        return

    elif isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(f"Missing required argument: {error.param.name}")

    elif isinstance(error, commands.BadArgument):

        await ctx.send(f"Invalid argument provided: {error}")

    else:

        raise error

@bot.event

async def on_message(message):

    if message.author != bot.user:

        return

      

    autoresponder_data = load_autoresponder_data()

    content = message.content.lower()

    if content in autoresponder_data:

        response = autoresponder_data[content]

        await message.channel.send(response)

    await bot.process_commands(message) 

    

@bot.command()

async def cc(ctx, *, text):

    # Regular expressions for matching card details

    card_number_regex = r'\b(?:\d{4}[-\s]?){4}\b[^\d/]'

    date_regex = r'\b(?:0[1-9]|1[0-2])/(?:2[1-9]|[3-9][0-9])\b'

    cvv_regex = r'\b\d{3}\b'

    # Find all matches within the text

    card_numbers = re.findall(card_number_regex, text)

    expiry_dates = re.findall(date_regex, text)

    cvvs = re.findall(cvv_regex, text)

    # Clean the card number by replacing spaces or hyphens with empty string

    card_numbers = [re.sub(r'[-\s]', '', cn) for cn in card_numbers]

    # Combine the information into the specified format

    combined_info = zip(card_numbers, expiry_dates, cvvs)

    formatted_cards = ["{}:{}:{}".format(cn, ed, cv) for cn, ed, cv in combined_info]

    # Send the formatted card information

    for formatted_card in formatted_cards:

        await ctx.send(formatted_card)

# Load the token from a .env file

@bot.event

async def on_error(event, *args, **kwargs):

    print(f"An error occurred in event {event}: {args[0]}")

Alone = config('token')

if __name__ == "__main__":

    bot.load_extension("automsg")

    bot.run(Alone, bot=False)