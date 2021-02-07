#!/usr/bin/env python3.9
"""An example file for test the discord API."""
# import urllib.request
# import subprocess
# import platform
# import requests
# import asyncio
# import random
# import socket
# import json
# import discord
from discord.ext import commands

# from discord.http import Route

from config.config import my_id
from tools.format import fcite


class Example(commands.Cog):
    """"""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tExample's Cog is ready.")

    # ######### #
    # Commandes #
    # ######### #

    def is_me():
        def predicate(ctx):
            return ctx.message.author.id == my_id

        return commands.check(predicate)

    @commands.command()
    @is_me()
    async def only_me(ctx):
        await ctx.send("Only you!")

    @commands.command(name="test", help="Commande de test/brouillon", hidden=True)
    async def test(self, ctx: commands.Context, *args, **kwargs):
        """Commande de test/brouillon."""
        await ctx.send("Cette commande ne fait rien du tout.")


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Example(bot))
