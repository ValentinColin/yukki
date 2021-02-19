#!/usr/bin/env python3.9

"""The launch file of the bot."""

import cogs.main as main
from discord.ext import commands
from config.config import get_prefix, DISCORD_TOKEN


client = commands.Bot(command_prefix=get_prefix)

main.setup(client)
client.run(DISCORD_TOKEN)