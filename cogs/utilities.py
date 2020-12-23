import json

from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('characters.json') as file:
            self.client.characters = json.load(file)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot logged on as {self.client.user}')

    @commands.command()
    async def name(self, ctx):
        """"Registers a given name, or reports the current name."
        """
        player, name = self.get_player_and_name(ctx)
        if ctx.message.content == '/name':
            await self.report_name(player, name, ctx)
        else:
            await self.add_name(player, name, ctx)

    def get_player_and_name(self, ctx):
        player = str(ctx.message.author)
        name = self.client.characters.get(player, player[:-5])

        return player, name

    def save_characters(self):
        with open('characters.json', 'w') as file:
            json.dump(self.client.characters, file)

    async def add_name(self, player, name, ctx):
        character_name = ' '.join(ctx.message.content.split()[1:])
        self.client.characters[player] = character_name
        self.save_characters()
        await ctx.message.channel.send(f'**{player[:-5]}** registered as **{character_name}**')

    async def report_name(self, player, name, ctx):
        if name == player[:-5]:
            await ctx.message.channel.send(f'**{name}** does not have a character name registered')
        else:
            await ctx.message.channel.send(f'**{player[:-5]}** is registered as **{name}**')

    @commands.command()
    async def noname(self, ctx):
        """"Removes the name associated with the player."
        """
        player, _ = self.get_player_and_name(ctx)
        character = self.client.characters.get(player)
        if character:
            del self.client.characters[player]
            self.save_characters()
            await ctx.message.channel.send(f'**{player}** no longer registered as **{character}**')
        else:
            await ctx.message.channel.send(f'No character registered to **{player}**')


def setup(client):
    client.add_cog(Utilities(client))
