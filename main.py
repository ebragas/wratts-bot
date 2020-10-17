# !/bin/python
import os

import discord
from dotenv import load_dotenv

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    client = discord.Client()

    client.run(TOKEN)

