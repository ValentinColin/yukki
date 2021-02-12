#!/usr/bin/env python3.9
"""Fichier de gestion du bot/robot."""
import yaml
import config.config as cfg
import discord
from discord.ext import commands
from config import emoji

from tools.access import access
from tools.format import fmarkdown, fcite


class Robot(commands.Cog):
    """Classe principale de gestion du bot."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt. Et écrit le statut d'activité."""
        # with open("data/yaml/bot.yml") as f:
        #     data = yaml.load(f, Loader=yaml.FullLoader)
        # prefix = data["servers"]["default"]["prefix"]
        # name = data["bot"]["status"]["listening"].format(prefix=prefix)
        # await self.bot.change_presence(
        #     activity=discord.Activity(type=discord.ActivityType.listening, name=name)
        # )
        self._activity = self.get_status(activity_name="listening")
        await self.bot.change_presence(activity=self._activity)
        print("    Robot's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    def get_prefix(self, id_server: int) -> str:
        """Renvoie le prefix du serveur."""
        with open("data/yaml/bot.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if str(id_server) in data["servers"]:
                return data["servers"][str(id_server)]["prefix"]
            else:
                return cfg.PREFIX

    def set_prefix(self, id_server: int, prefix: str):
        """Modifie le prefix du serveur."""
        id_server = str(id_server)
        with open("data/yaml/bot.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if id_server not in data["servers"]:
            data["servers"][id_server] = data["servers"]["default"]
        data["servers"][id_server]["prefix"] = prefix
        with open("data/yaml/bot.yml", "w") as f:
            yaml.dump(data, f)

    def get_status(self, activity_name: str) -> discord.Activity:
        """Renvoie l'objet d'activité correspondante avec les infos dans la bdd.
        Attention: ce n'est pas le statut en cours du bot.
        Activités possible:
            - game
            - listening
            - watching
        """
        with open("data/yaml/bot.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        name = data["bot"]["status"][activity_name]
        if "{{prefix}}" in name:
            prefix = data["servers"]["default"]["prefix"]
            name = name.format(prefix=prefix)
        if activity_name == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
        elif activity_name == "game":
            activity = discord.Activity(type=discord.ActivityType.game, name=name)
        elif activity_name == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        else:
            raise ValueError(
                f"{activity_name} not accepted. Only listening, game, watching."
            )
        return activity

    # ######### #
    # Commandes #
    # ######### #

    @commands.command()
    async def prefix(self, ctx: commands.Context, *, prefix: str = None):
        """Changer le prefix des commandes du bot."""
        if prefix is None:
            prefix = self.get_prefix(ctx.guild.id)
            await ctx.send(f"Le prefix actuelle est: `{ctx.prefix}`")
        else:
            ctx.bot.command_prefix = self.set_prefix(ctx.guild.id, prefix)
            await self.bot.change_presence()
            await ctx.send(f"Le prefix à été changer en: `{prefix}`")

    @commands.command(aliases=["jeu"])
    @access.admin
    async def game(self, ctx: commands.Context, *, jeu: str):
        """Initialise le jeu du bot."""
        if jeu is None:
            game = self.get_status(
                activity_name="game"
            )  # Renvoie une activité de type game, est-ce pareil que discord.Game?
        else:
            game = discord.Game(jeu)
        await self.bot.change_presence(activity=game)

    @commands.command(aliases=["activité"])
    @access.admin
    async def activity(self, ctx: commands.Context, activity_name: str = None):
        """Définie une activité.
        Nom d'activité autorisé:
            - listening
            - game
            - watching"""
        if activity_name is not None:
            activity = self.get_status(activity_name)
            await self.bot.change_presence(activity=activity)
        else:
            await ctx.send(
                f"L'activité `{activity_name}`n'est pas accepter, "
                f"voir l'aide pour plus d'informations."
            )


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Robot(bot))
