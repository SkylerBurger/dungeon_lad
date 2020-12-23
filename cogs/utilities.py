import json

from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, client):
        """Instantiates a Utilities object.

        Args:
            client (discord.ext.commands.Bot): The bot the Class/Cog is being added to.
        """
        self.client = client
        with open('characters.json') as file:
            self.client.characters = json.load(file)

    @commands.Cog.listener()
    async def on_ready(self):
        """Logs that the bot is logged in and ready.
        """
        print(f'Bot logged on as {self.client.user}')

    @commands.command()
    async def name(self, ctx):
        """Manages character names for players.

        Uses:
            /name - Will report back your character name, if one is registered.
            /name <character_name> - Will assign <character_name> to your account.

        Examples:
            /name Rune Amon - Will set my name to 'Rune Amon'
            /name - Will report back that my current character name is 'Rune Amon'

        Notes:
            See /noname if you wish to remove your character name without setting a new one.
        """
        player, name = self.get_player_and_name(ctx)
        if ctx.message.content == '/name':
            await self.report_name(player, name, ctx)
        else:
            await self.add_name(player, ctx)

    def get_player_and_name(self, ctx):
        """Extracts the player's username and character name.

        Args:
            ctx (discord.Context): An object containing information regarding the context in which the command was issued.

        Returns:
            tuple(player, name):
                player (str): Represents the username of the player that issued the command.
                name (str): Represents the character name of the player that issued the command.
        """
        player = str(ctx.message.author)
        name = self.client.characters.get(player, player[:-5])

        return player, name

    def save_characters(self):
        """Saves the current state of the characters dict into the 'characters.json' file.
        """
        with open('characters.json', 'w') as file:
            json.dump(self.client.characters, file)

    async def add_name(self, player, ctx):
        """Registers a given character name to a player in the characters dict.

        Args:
            player (str): The username of the player issuing the command.
            ctx (discord.Context): An object containing information regarding the context in which the command was issued. 
        """
        character_name = ' '.join(ctx.message.content.split()[1:])
        self.client.characters[player] = character_name
        self.save_characters()
        await ctx.message.channel.send(f'**{player[:-5]}** registered as **{character_name}**')

    async def report_name(self, player, name, ctx):
        """Reports the current character name registered to the player issuing the command.

        Args:
            player (str): The username of the player issuing the command.
            name (str): The character name associated with the player issuing the command.
            ctx (discord.Context): An object containing information regarding the context in which the command was issued.
        """
        if name == player[:-5]:
            await ctx.message.channel.send(f'**{name}** does not have a character name registered')
        else:
            await ctx.message.channel.send(f'**{player[:-5]}** is registered as **{name}**')

    @commands.command()
    async def noname(self, ctx):
        """Removes associated character name for player issuing the command.

        Example:
            /noname - That's it! Any associated character name will be removed.
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
    """Allows a Bot from discord.ext.commands to add Utilities as a cog.

    Args:
        client (discord.ext.commands.Bot): The bot to add the Cog to.
    """
    client.add_cog(Utilities(client))
