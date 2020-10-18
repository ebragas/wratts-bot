# !/bin/python
import logging
import os

import discord
from dotenv import load_dotenv


class WrattBot(discord.Client):

    async def on_ready(self):
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} has connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    async def on_member_join(self, member):
        logging.info('on_member_join')
        channel = client.get_channel(ID)
        await channel.edit(name = 'Member count: {}'.format(channel.guild.member_count))

    # async def on_member_join(self, member):
    #     logging.info('on_member_join')
    #     await member.create_dm()
    #     await member.dm_channel.send(
    #         f'Hi {member.name}, welcome to my Discord server!'
    #     )

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    logging.info('Starting bot...')
    client = WrattBot()
    client.run(TOKEN)
