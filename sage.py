import discord
import json
import logging
import random

#open json file for the auth tokens
with open('auth.json') as auth:
    tokens = json.load(auth)

#create client
client = discord.Client()

#message upon launch
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#react to user saying hello
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

#logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_message(message):
    logger.info(message)

##for other logs use the following
##logger.error(f"error happened heres the message {message}")


#roll a die
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$d'):
        max = message.content[2:]
        if max.isnumeric() and int(max) > 0:
            outcome = random.randint(1, int(max))
            await message.channel.send(f'rolled a d{max}, outcome is {outcome}')
        else:
            await message.channel.send(f'{max} is not a value number of sides of a die')

#flip a coin
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$coin'):
        outcome = random.randint(1, 2)
        coin = {1: 'heads', 2: 'tails'}
        await message.channel.send(f'Coin returned {coin[outcome]}')



#run the bot using token
client.run(tokens['bot token'])


