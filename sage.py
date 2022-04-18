from asyncio import queues
import discord
import json
import logging
import random
import psycopg2
from datetime import datetime
import requests
from serpapi import GoogleSearch


# open json file for the auth tokens
with open('auth.json') as auth:
    tokens = json.load(auth)

# create client
client = discord.Client()

# message upon launch
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# PostgreSQL db connection
conn = psycopg2.connect(database="postgres", user = tokens['pguser'], password = tokens['pgpw'], host = "127.0.0.1", port = "5432")

if conn:
    print("Opened database successfully")

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Users (\
            User_ID int PRIMARY KEY, \
            Username VARCHAR NOT NULL, \
            Wealth int NOT NULL, \
            Created_on TIMESTAMP NOT NULL\
            );')
conn.commit()
print("Table Users created successfully")

# logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

## for other logs use the following
## logger.error(f"error happened heres the message {message}")

@client.event
async def on_message(message):
    # log all messages
    logger.info(message)
    # do nothing on ignore bot messages
    if message.author == client.user:
        return
    
    #react to user saying hello
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #roll a n sided die
    if message.content.startswith('$d'):
        max = message.content[2:]
        if max.isnumeric() and int(max) > 0:
            outcome = random.randint(1, int(max))
            await message.channel.send(f'rolled a d{max}, outcome is {outcome}')
        else:
            await message.channel.send(f'{max} is not a value number of sides of a die')

    #flip a coin
    if message.content.startswith('$coin'):
        outcome = random.randint(1, 2)
        coin = {1: 'heads', 2: 'tails'}
        await message.channel.send(f'Coin returned {coin[outcome]}')
    
    #get a user's roles
    if message.content.startswith('$roles'):
        await message.channel.send(message.author.roles)

    #get weather using weather API
    if message.content.startswith('$weather'):
        weather_key = tokens['weather']
        location = message.content[9:]
        if location == '': #default weather location to toronto
            location = 'toronto'
        response = requests.get('http://api.weatherapi.com/v1/current.json?key='+weather_key+'&q='+location)
        weather = response.json()

        loc_name = weather['location']['name']
        loc_count = weather['location']['country']
        cond = weather['current']['condition']['text']
        temp = weather['current']['temp_c']
        wind_dr = weather['current']['wind_dir']
        wind_spd = weather['current']['wind_kph']
        percip = weather['current']['precip_mm']
        
        embedmsg=discord.Embed(title="Weather Report", description=f"{loc_name}, {loc_count} ```Weather is {cond}, with temperature at {temp}C. \
                                With wind at {wind_spd} kmph blowing {wind_dr}. \
                                total percipitation is {percip}mm.```" , color=0xFF5733)

        await message.channel.send(embed=embedmsg)

    #get the top google image using serp API
    if message.content.startswith('$img'):
        quer = message.content[5:]
        if quer == '': 
            await message.channel.send('invalid search result')
            return
        params = {
            "q": quer,
            "tbm": "isch",
            "ijn": "0",
            "api_key": tokens['serp']
            }
        search = GoogleSearch(params)
        results = search.get_dict()
        images_results = results['images_results']

        embedmsg=discord.Embed(title=f"Image search for: {quer}", description=f"{message.author} \
            {images_results[0]['original']}" , color=0xFF5733)

        await message.channel.send(embed=embedmsg)

    #get a random google image among the top 100 images using serp API 
    if message.content.startswith('$rimg'):
        quer = message.content[6:]
        if quer == '': 
            await message.channel.send('invalid search result')
            return
        params = {
            "q": quer,
            "tbm": "isch",
            "ijn": "0",
            "api_key": tokens['serp']
            }
        search = GoogleSearch(params)
        results = search.get_dict()
        images_results = results['images_results']
        outcome = random.randint(0, 99)

        embedmsg=discord.Embed(title=f"Image search for: {quer}", description=f"{message.author} \
            {images_results[outcome]['original']}" , color=0xFF5733)

        await message.channel.send(embed=embedmsg)

#run the bot using token
client.run(tokens['bot token'])