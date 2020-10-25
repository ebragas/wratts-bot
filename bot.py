"""A bot for fun and profit!"""

import logging
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv # TODO: not sure I want to keep this


# class WrattBot(discord.Client):
#     """Chef Wratts!"""

#     async def on_ready(self):
#         guild = discord.utils.get(self.guilds, name=GUILD)
#         print(
#             f'{self.user} has connected to the following guild:\n'
#             f'{guild.name}(id: {guild.id})\n'
#         )

#         members = '\n - '.join([member.name for member in guild.members])
#         print(f'Guild Members:\n - {members}')

#     async def on_member_join(self, member):
#         # TODO: not working lol
#         logging.info('on_member_join')
#         await member.create_dm()
#         await member.dm_channel.send(
#             f'Hi {member.name}, welcome to my Discord server!'
#         )

#     async def on_message(self, message):
#         print(f'Message from {message.author}: {message.content}')

#         if message.author == client.user: # avoids triggering itself?
#             return

#         elif message.content.startswith('$hello'):
#             await message.channel.send('Hello! :test_tube:')

#         elif message.content == '99!':
#             b99_quotes = [
#                 "I'm the human form of the :100: emoji.",
#                 'Bingpot!',
#                 (
#                     'Cool. Cool cool cool cool cool cool cool cool, '
#                     'no doubt no doubt no doubt no doubt.'
#                 ),
#             ]
#             await message.channel.send(random.choice(b99_quotes))

#         elif message.content == 'force error!':
#             raise discord.DiscordException

#     async def on_error(self, event, *args, **kwargs):
#         with open('err.log', 'a') as fp:
#             if event == 'on_message':
#                 fp.write(f'Unhandled message: {args[0]}\n')
#             else:
#                 raise

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='99', help='Responds with a random Brooklyn Nine Nine quote')
async def nine_nine(ctx):
    b99_quotes = [
        "I'm the human form of the :100: emoji.",
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(b99_quotes)
    await ctx.send(response)

@bot.command(name='roll', help='Rolls a die a few times and returns the results')
async def roll_dice(ctx, times: int, sides: int): 
    # TODO: makes sides a dice object initializer e.g. Die(d4)
    rolls = [
        str(random.choice(range(1, sides + 1)))
        for _ in range(times)
    ]
    await ctx.send(rolls)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    logging.info('Starting bot...')
    # client = WrattBot()
    # client.run(TOKEN)

    bot.run(TOKEN)
