import os
import discord
from keep_alive import keep_alive
import logging

keep_alive()

my_secret = os.environ['token']

logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(my_secret)