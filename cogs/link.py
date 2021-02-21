#!/usr/bin/env python3.9

"""Fichiers de gestion des liens utiles (pense-bête)."""

import datetime
import yaml
import discord
from discord.ext import commands

# from typing import Union, Optional
from tools.format import fcite, fmarkdown, flisting


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

    @staticmethod
    def get_links_server(guild_id: int) -> None:
        """Renvoie tous les liens de la target."""
        with open("data/yaml/linker.yml") as f:
            data_links = yaml.load(f, Loader=yaml.FullLoader)
        links_target = []
        for data_link in data_links:
            if str(guild_id) == data_link["server"]:
                links_target.append(data_link)
        return links_target

    @staticmethod
    def get_links_user(user_id: int, guild_id: int = None) -> None:
        """Renvoie tous les liens de la target."""
        with open("data/yaml/linker.yml") as f:
            data_links = yaml.load(f, Loader=yaml.FullLoader)
        links_target = []
        if guild_id is not None:
            for data_link in data_links:
                if (
                    user_id == int(data_link["author"])
                    and guild_id == int(data_link["server"])
                ):
                    links_target.append(data_link)
        else:
            for data_link in data_links:
                if str(user_id) == data_link["author"]:
                    links_target.append(data_link)
        return links_target

    @staticmethod
    def add_link(guild: discord.Guild, member: discord.Member, urls: str) -> None:
        """Ajoute un lien."""
        with open("data/yaml/linker.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for url in urls:
            linker = {
                "author": str(member.id),
                "date": datetime.date.today(),
                "server": str(guild.id),
                "url": url,
            }
            data.append(linker)
        with open("data/yaml/linker.yml", "w") as f:
            yaml.dump(data, f)

    # ######### #
    # Commandes #
    # ######### #

    # liste des commandes
    # - link (affiche MES liens fait sur le serveur)
    # - link server (affiche TOUS LES liens fait sur le serveur)
    # - link all (affiche TOUS MES liens peu importe le serveur) -> ajouter une confirmation
    # - link target (affiche la liste des link de la cible)
    # - link add (ajoute un lien au répertoire)

    @commands.group()
    async def link(self, ctx: commands.Context):
        """Affiche les liens fait sur le serveur."""
        if ctx.invoked_subcommand is None:
            await ctx.send(fcite("Use link with a subcommand please."))

    @link.command()
    async def server(self, ctx: commands.Context):
        """Affiche tous les liens fait sur le serveur."""
        data_links = self.get_links_server(ctx.guild.id)
        links = []
        for _, link in enumerate(data_links):
            links.append(link["url"])
        txt = "Liens ajouter sur le serveur:\n" + flisting(links)
        await ctx.send(fmarkdown(txt))

    @link.command(aliases=["member", "membre", "cible", "of", "de", "me", "moi"])
    async def target(self, ctx: commands.Context, target: discord.Member = None):
        """Affiche les liens fait par la cible sur le serveur."""
        if target is None:
            target = ctx.author
        data_links = self.get_links_user(target.id, ctx.guild.id)
        links = []
        for _, link in enumerate(data_links):
            links.append(link["url"])
        txt = f"Liens ajouter par {target.display_name}:\n" + flisting(links)
        await ctx.send(fmarkdown(txt))

    @link.command()
    async def all(self, ctx: commands.Context):
        """Affiche la totalité des liens."""
        data_links = self.get_links_user(ctx.author.id)
        links = []
        for _, link in enumerate(data_links):
            links.append(link["url"])
        txt = f"Liens ajouter par {ctx.author.display_name}:\n"
        txt += flisting(links)
        await ctx.send(fmarkdown(txt))

    @link.command()
    async def add(self, ctx: commands.Context, *urls: str):
        """Ajoute un lien au répertoire."""
        self.add_link(ctx.guild, ctx.author, urls)
        await ctx.send(fcite("added"), delete_after=5)


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Link(bot))
