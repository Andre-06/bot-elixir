import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents, help_command=None)
