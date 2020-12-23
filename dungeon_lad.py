import json
import random

import discord


class DungeonLad(discord.Client):
    def __init__(self):
        super().__init__()
        with open('characters.json') as file:
            self.characters = json.load(file)

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

    def save_characters(self):
        with open('characters.json', 'w') as file:
            json.dump(self.characters, file)

    async def cypher_system(self, name, message):
        effort, assets, bonus, shift = self.parse_cypher(message.content)

        if bonus > 2 or assets > 2:
            await message.channel.send('Neither bonuses nor assets can exceed 2')
            return
        raw_roll = self.roll_d20()
        final_roll = raw_roll + bonus
        success_level = self.calculate_success(final_roll, effort, assets, shift)
        succeeds = f'**{name}** succeeds up to difficulty **level {success_level}**\n'
        roll_summary = f'`Roll: {final_roll} (raw {raw_roll} + bonus {bonus})`\n'
        utilized = f'`Success Level: {success_level} (roll {final_roll // 3} + effort {effort} + assets {assets} + shifts {shift})`' 
        await message.channel.send(succeeds + roll_summary + utilized)

    async def add_name(self, player, name, message):
        character_name = ' '.join(message.content.split()[1:])
        self.characters[player] = character_name
        self.save_characters()
        await message.channel.send(f'**{name}** registered as **{character_name}**')

    async def report_name(self, player, name, message):
        if name == player[:-5]:
            await message.channel.send(f'**{name}** does not have a character name registered')
        else:
            await message.channel.send(f'**{player[:-5]}** is registered as **{name}**')

    async def remove_name(self, player, message):
        character = self.characters.get(player)
        if character:
            del self.characters[player]
            self.save_characters()
            await message.channel.send(f'**{player}** no longer registered as **{character}**')
        else:
            await message.channel.send(f'No character registered to **{player}**')

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        player = str(message.author)
        name = self.characters.get(player, player[:-5]);
        
        command = lambda *x: any([message.content.startswith(y) for y in x])

        if command('/cypher', '/cy'):
            await self.cypher_system(name, message)

        if command('/name'):
            if message.content == '/name':
                await self.report_name(player, name, message)
            else:
                await self.add_name(player, name, message)

        if command('/no-name'):
            await self.remove_name(player, message)

        if command('/pm'):
            await message.author.send('heyo')


if __name__ == "__main__":
    import environ
    env = environ.Env()
    env.read_env()
    BOT_TOKEN = env('BOT_TOKEN')

    client = DungeonLad()
    client.run(BOT_TOKEN)