#!/usr/bin/env python3.9

"""A funny cogs."""

import urllib.request  #
import discord
from discord.ext import commands
from tools.format import fcite
from tools.couleurs import convert_to_hex


class Git(commands.Cog):
    """Classe concernant git sur discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Git's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #


    # ######### #
    # Commandes #
    # ######### #

    @commands.command()
    async def badge(self, ctx: commands.Context, left_txt: str, right_txt: str, *, color: str):
        """Envoie un lien d'image de badge github généré par https://github.com/badges/shields"""
        color_hex = convert_to_hex(color)
        url = f"https://img.shields.io/badge/{left_txt}-{right_txt}-{color_hex}"
        await ctx.send(url)


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Git(bot))
