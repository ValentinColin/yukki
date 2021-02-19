#!/usr/bin/env python3.9

"""Fichiers de gestion des liens utiles (pense-bête)."""

import os
import yaml
import discord
from discord.ext import commands


class Link(commands.Cog):
    """Classe de gestion des liens utiles."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Link's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #
    
    def get_links_target(self, id_target: int):
        """Renvoie tous les liens de la target."""
        pass

    def add_link(self, target: discord.Member, *urls: str):
        """Ajoute un lien."""
        target_id = str(target.id)
        with open("data/yaml/bot.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for url in urls:
                data["linker"]["links"].append(url)
                data[target_id].append(id(url))

    # ######### #
    # Commandes #
    # ######### #
    
    # liste des commandes
    # - link (affiche MES liens fait sur le serveur ou celui de la target si défini)
    # - link server (affiche TOUS LES liens fait sur le serveur)
    # - link all (affiche TOUS MES liens sans limite de serveur) -> ajouter une métode de confirmation
    # - link target (affiche la liste des link de la cible)
    # - link add (ajoute un lien au répertoire)

    @commands.group()
    async def link(self, ctx: commands.Context):
        """Affiche les liens fait sur le serveur."""
        if ctx.invoked_subcommand is None: # vérifier si invoked_subcommand est à None si j'écris n'importe quoi 
            await ctx.send("link")

    @link.command(aliases=["cible", "of", "de"])
    async def target(self, ctx: commands.Context, target: discord.Member = None):
        """Affiche les liens fait par la cible sur le serveur."""
        if target is None:
            target = ctx.author
        await ctx.send("link target")

    @link.command()
    async def server(self, ctx: commands.Context):
        """Affiche tous les liens fait sur le serveur."""
        await ctx.send("link server")

    @link.command()
    async def all(self, ctx: commands.Context):
        """Affiche la totalité des liens."""
        await ctx.send("link all")

    @link.command()
    async def add(self, ctx: commands.Context, url: str):
        """Ajoute un lien au répertoire."""
        await ctx.send("link add")





def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Link(bot))
