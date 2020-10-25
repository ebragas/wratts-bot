"""A bot for fun and profit."""

import logging
import os
import random

from discord.ext import commands
from dotenv import load_dotenv # NOTE: not sure I want to keep this
import discord


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """Logs bot ready state"""
    logging.info(f'{bot.user.name} has connected to Discord!')


@bot.command(name='99', help='Responds with a random Brooklyn Nine Nine quote')
async def nine_nine(ctx):
    """Responds with a random Brooklyn Nine Nine quote"""
    b99_quotes = [
        "I'm the human form of the :100: emoji.",
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool cool, '
            + 'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(b99_quotes)
    await ctx.send(response)


@bot.command(name='roll', help='Rolls a die a few times and returns the results')
async def roll_dice(ctx, times: int, sides: int):
    """Rolls virtual dice"""
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

    bot.run(TOKEN)
