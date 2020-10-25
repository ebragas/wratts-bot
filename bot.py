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


class Greetings(commands.Cog):
    
    GREETINGS = ['oh hai', 'Hey', 'Hey hey', ':wave:']
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member=None):
        """Says hello"""
        member = member or ctx.author
        greeting = random.choice(self.GREETINGS)
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'{greeting} {member.mention}!')
        else:
            await ctx.send(
                f'{greeting} {member.mention}...'
                + ' This feels familiar :face_with_monocle:'
                )
        self._last_member = member


bot.add_cog(Greetings(bot))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # GUILD = os.getenv('DISCORD_GUILD')

    logging.info('Starting bot...')

    bot.run(TOKEN)
