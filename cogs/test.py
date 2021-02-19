#!/usr/bin/env python3.9
"""An example file for test the discord API."""
import discord
from discord.ext import commands
from config.config import my_id
from config import emoji
from tools.format import fcite



class Test(commands.Cog):
    """Classe de test."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Example's Cog is ready.")

    # ######### #
    # Commandes #
    # ######### #

    @commands.command(hidden=True)
    async def test(self, ctx: commands.Context, msg: str = "@everyone"):
        """Commande de test/brouillon."""
        await ctx.send("Cette commande ne fait rien du tout.")
        await ctx.send(msg)



def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Test(bot))