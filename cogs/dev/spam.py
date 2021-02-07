#!/usr/bin/env python3.9
"""Fichiers de Spam pour discord."""
import discord
from discord.ext import commands
from tools.format import fcite


class Spam:
    """Classe de Spam pour discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tSpam's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    # ######### #
    # Commandes #
    # ######### #


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Spam(bot))
