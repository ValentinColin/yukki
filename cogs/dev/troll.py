#!/usr/bin/env python3.9
"""Fichiers de Troll pour discord."""
import discord
from discord.ext import commands
from tools.format import fcite


class Troll:
    """Classe de Troll pour discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tTroll's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    # ######### #
    # Commandes #
    # ######### #


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Troll(bot))
