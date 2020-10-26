"""A bot for fun and profit."""

import logging
import os
import random
from collections import defaultdict
from itertools import cycle

from discord.ext import commands
from dotenv import load_dotenv # NOTE: not sure I want to keep this
import discord


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    """Logs bot ready state"""
    logging.info(f'{bot.user.name} has connected to Discord!')
    # TODO: unpin any pinned messages


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


class RollCall(commands.Cog):

    INGREDIENTS = [
        'lettuce, tomato & cilantro',
        'cheese & sour cream',
        'chips & salsa',
        'seasoning & beans',
        'avocados'
    ]

    def __init__(self, bot):
        self.bot = bot
        self._roll_call_msg = None

    @commands.command(name='rollcall')
    async def start_roll(self, ctx):
        self._roll_call_msg = await ctx.send('Game night has begun! You coming?')
        
        for emoji in ('👍', '👎'):
            await self._roll_call_msg.add_reaction(emoji)

        await self._roll_call_msg.pin()

    @commands.command(name='closeroll')
    async def close_roll(self, ctx):

        if not self._roll_call_msg:
            await ctx.send("Roll hasn't been called yet. Start with `!rollcall`")
            return

        self._roll_call_msg = await ctx.channel.fetch_message(self._roll_call_msg.id)

        # get affirmative responders
        reactions = self._roll_call_msg.reactions
        logging.info(reactions)

        attendees = []
        async for user in reactions[0].users():
            attendees.append(user)
 
        # assign ingredients
        # TODO: pull this out
        random.shuffle(attendees)
        ingredients = self.INGREDIENTS.copy()
        random.shuffle(ingredients)

        assignments = defaultdict(list)
        for assignee, ingredient in zip(cycle(attendees), ingredients):
            assignments[assignee].append(ingredient)

        for member, items in assignments.items():
            assignment = f'{member.mention}: {", ".join(items)}'
            await ctx.send(assignment)

        # cleanup



bot.add_cog(Greetings(bot))
bot.add_cog(RollCall(bot))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # GUILD = os.getenv('DISCORD_GUILD')

    logging.info('Starting bot...')

    bot.run(TOKEN)
