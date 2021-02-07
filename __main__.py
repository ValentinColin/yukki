#!/usr/bin/env python3.9
"""The lunch file of the bot."""
import cogs.main as main
from discord.ext import commands
from config.config import DISCORD_TOKEN, PREFIX


client = commands.Bot(command_prefix=PREFIX)

main.setup(client)
client.run(DISCORD_TOKEN)
