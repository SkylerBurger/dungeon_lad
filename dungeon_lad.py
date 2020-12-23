import os

from discord.ext import commands
import environ

env = environ.Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')

dungeon_lad = commands.Bot(command_prefix='/')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        dungeon_lad.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded cog: {file[:-3]}')

dungeon_lad.run(BOT_TOKEN)
