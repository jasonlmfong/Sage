import discord
import json
import logging


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
    if message.author == client.user:
        return
    else:
        logger.info(message)
##logger.error(f"error happened heres the message {message}")


#run the bot using token
client.run(tokens['bot token'])


