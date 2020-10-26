"""A bot for fun and profit."""

import logging
import os
import random
from collections import defaultdict
from itertools import cycle

from discord.ext import commands
from dotenv import load_dotenv  # NOTE: not sure I want to keep this
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


@bot.command(
    name='roll', help='Rolls a die a few times and returns the results')
async def roll_dice(ctx, times: int, sides: int):
    """Rolls virtual dice"""
    rolls = [
        str(random.choice(range(1, sides + 1)))
        for _ in range(times)
    ]
    await ctx.send(rolls)


class Greetings(commands.Cog):
    """Basic greetings cog"""

    ingredients = ['oh hai', 'Hey', 'Hey hey', ':wave:']

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Greet new members"""
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
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
    """Roll call manager for taco salad ingredient assignment"""

    ingredients = [
        'lettuce',
        'tomato',
        'cilantro',
        'cheese',
        'sour cream',
        'chips', 'salsa',
        'seasoning',
        'beans',
        'avocados'
    ]

    def __init__(self, bot):
        self.bot = bot
        self._poll_msg = None

    @commands.command(name='rollcall')
    async def start_roll(self, ctx):
        """Starts a reaction poll"""
        self._poll_msg = await ctx.send(
            'Game night has begun! You coming?'
        )

        for emoji in ('👍', '👎'):
            await self._poll_msg.add_reaction(emoji)

        await self._poll_msg.pin()

    @commands.command(name='closeroll')
    async def close_roll(self, ctx):
        """Closes the roll and randomly assigns ingredients to users who
        responded affirmative
        """
        try:
            if not self._poll_msg:
                await ctx.send("Roll hasn't been called yet. Start with `!rollcall`")
                return

            self._poll_msg = await ctx.channel.fetch_message(
                self._poll_msg.id
            )

            # get affirmative responders
            logging.info(self._poll_msg.reactions)

            attendees = []
            async for user in self._poll_msg.reactions[0].users():
                if user.name != bot.user.name:
                    attendees.append(user)

            if not attendees:
                await ctx.send('No on likes my cooking? :cry:')

            # assign ingredients
            assignments = self._random_assignment(attendees)

            for member, items in assignments.items():
                assignment = f'{member.mention}: {", ".join(items)}'
                await ctx.send(assignment)

        finally:
            # cleanup
            await self._poll_msg.unpin()
            self._poll_msg = None

    def _random_assignment(self, members):
        """Randomly assign users a set of ingredients"""
        random.shuffle(members)
        ingredients = self.ingredients.copy()
        random.shuffle(ingredients)

        assignments = defaultdict(list)
        for member, ingredient in zip(cycle(members), ingredients):
            assignments[member].append(ingredient)

        return assignments


bot.add_cog(Greetings(bot))
bot.add_cog(RollCall(bot))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # GUILD = os.getenv('DISCORD_GUILD')

    logging.info('Starting bot...')

    bot.run(TOKEN)
