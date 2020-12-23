import random

from discord.ext import commands

class CypherSystem(commands.Cog):
    def __init__(self, client):
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

        if bonus > 2 or assets > 2:
            await ctx.message.channel.send('Neither bonuses nor assets can exceed 2')
            return
        raw_roll = self.roll_d20()
        final_roll = raw_roll + bonus
        success_level = self.calculate_success(final_roll, effort, assets, shift)
        succeeds = f'**{name}** succeeds up to difficulty **level {success_level}**\n'
        roll_summary = f'`Roll: {final_roll} (raw {raw_roll} + bonus {bonus})`\n'
        utilized = f'`Success Level: {success_level} (roll {final_roll // 3} + effort {effort} + assets {assets} + shifts {shift})`' 
        await ctx.message.channel.send(succeeds + roll_summary + utilized)

    def roll_d20(self):
        return random.randint(1, 20)

    def calculate_success(self, roll, effort, assets, shift):
        success_level = roll // 3
        success_level += effort
        success_level += assets
        # Double check if you need to confirm that success_level is <= 10 before adding in the shift 
        success_level += shift

        return success_level

    def parse_cypher(self, content):
        effort = 0
        assets = 0
        bonus = 0
        shift = 0
        words = content.split()
        for index, word in enumerate(words):
            word = word.lower()
            if word == 'effort':
                effort = int(words[index + 1])
            if word == 'asset' or word == 'assets':
                assets = int(words[index + 1])
            if word == 'bonus' or word == 'bonuses':
                bonus = int(words[index + 1])
            if word == 'shift' or word == 'shifts':
                shift = int(words[index + 1])

        return effort, assets, bonus, shift


def setup(client):
    client.add_cog(CypherSystem(client))
