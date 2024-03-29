#!/usr/bin/env python3.9

"""A usefull cogs for League of legends."""

import discord
from discord.ext import commands


class Lol(commands.Cog):
    """Classe d'outils pour League of legends."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Lol's Cog is ready.")

    @commands.Cog.listener(name="game launched")
    async def game_launched(self, ctx: commands.Context):
        """Notifie dés qu'une personne lance un jeu"""
        async for m in ctx.guild.members:
            if m.activity == discord.ActivityType.playing:
                print(f"{m.display_name} joue à {m.activity.game}")

    # ######### #
    # Functions #
    # ######### #


    # ######### #
    # Commandes #
    # ######### #

    @commands.command(aliases=["alias_de_une_commande"])
    @access.me # droit d'utilisation aux commandes
    async def une_commande(self, ctx: commands.Context, *, txt: str):
        """Une commande dont je ne connais pas l'utilité."""
        await ctx.send(fcite(txt))


    @commands.command()
    @access.me
    async def lol_test(self, ctx: commands.Context, *, txt: str):
        """Commande de test"""
        await ctx.send(ctx.author.activities[0].name)


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Lol(bot))