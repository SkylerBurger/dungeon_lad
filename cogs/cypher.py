import random

from discord.ext import commands


class CypherSystem(commands.Cog):
    def __init__(self, client):
        """Instantiates a CypherSystem object.

        Args:
            client (discord.ext.commands.Bot): The bot the Class/Cog is being added to.
        """
        self.client = client
    
    @commands.command()
    async def cy(self, ctx):
        """Calculates the success level of a cypher system task.

        Format:
          /cy effort <int> asset(s) <int> bonus(es) <int> shift(s) <int>
          The argument pairs are all optional and can be entered in any order.

        Examples:
          /cy
          /cy effort 2 bonus 1
          /cy shift 1 assets 2
          /cy bonuses 1 asset 1 effort 2 shifts 1
        """
        player = str(ctx.message.author)
        name = player[:-5]
        name = self.client.characters.get(player, player[:-5]);

        effort, assets, bonus, shift = self.parse_cypher(ctx.message.content)

        if bonus > 2:
            await ctx.message.channel.send('Applied bonuses cannot exceed 2')
            return
        elif assets > 2:
            await ctx.message.channel.send('Applied assets cannot exceed 2')
            return
        elif effort > 6:
            await ctx.message.channel.send('Applied effort cannot exceed 6')
            return

        raw_roll = self.roll_d20()
        final_roll = raw_roll + bonus
        success_level = self.calculate_success(final_roll, effort, assets, shift)
        succeeds = f'**{name}** succeeds up to difficulty **level {success_level}**\n'
        roll_summary = f'`Roll: {final_roll} (raw {raw_roll} + bonus {bonus})`\n'
        utilized = f'`Success Level: {success_level} (roll {final_roll // 3} + effort {effort} + assets {assets} + shifts {shift})`' 
        await ctx.message.channel.send(succeeds + roll_summary + utilized)

    def roll_d20(self):
        """Simulates rolling a d20 die.

        Returns:
            (int): An integer between 1-20 (inclusive) representing the roll of the die.
        """
        return random.randint(1, 20)

    def calculate_success(self, roll, effort, assets, shift):
        """Calculates the success level of a task based on the Cypher Systems engine.

        Args:
            roll (int): Represents the roll total, raw roll + any bonuses.
            effort (int): Represents the level(s) of effort used on the task.
            assets (int): Represents the number of assets available for the task.
            shift (int): Represents the number of shifts available for the task.

        Returns:
            success_level (int): Represents the success level achieved for a task.
        """
        success_level = roll // 3
        success_level += effort
        success_level += assets
        # Double check if you need to confirm that success_level is <= 10 before adding in the shift 
        success_level += shift

        return success_level

    def parse_cypher(self, content):
        """Parses a Cypher System command received by the bot.

        Args:
            content (str): The text content of the message the bot received with the command.

        Returns:
            tuple(effort, assets, bonus, shift):
                effort (int): Represents the intended level(s) of effort to apply to the task.
                assets (int): Represents the number of assets available for the task.
                bonus  (int): Represents the number of bonuses to apply to the roll.
                shift (int): Represents the number of shifts to apply to the task.
        """
        effort = 0
        assets = 0
        bonus = 0
        shift = 0
        words = content.split()
        for index, word in enumerate(words):
            word = word.lower()
            if word == 'effort' or word == 'e':
                effort = int(words[index + 1])
            if word == 'asset' or word == 'assets' or word == 'a':
                assets = int(words[index + 1])
            if word == 'bonus' or word == 'bonuses' or word == 'b':
                bonus = int(words[index + 1])
            if word == 'shift' or word == 'shifts' or word == 's':
                shift = int(words[index + 1])

        return effort, assets, bonus, shift


def setup(client):
    """Allows a Bot from discord.ext.commands to add CypherSystem as a cog.

    Args:
        client (discord.ext.commands.Bot): The bot to add the Cog to.
    """
    client.add_cog(CypherSystem(client))
