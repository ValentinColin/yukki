#!/usr/bin/env python3.9

"""Fichier principale du bot."""

import os
import socket
import progressbar
import subprocess
import platform
import discord

from discord.ext import commands
from discord.http import Route

from tools.access import access
from tools.format import fcite, fmarkdown


class Main(commands.Cog):
    """Classe principale du bot."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot
        self.load_cogs()

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Main's Cog is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Nouveau membre."""
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Départ d'un membre."""
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Envoie l'erreur aux utilisateurs."""
        message = str(error)
        if message[-1] != ".":
            message += "."
        await ctx.send(message)
        raise error

    # ######### #
    # Functions #
    # ######### #

    def load_cogs(self):
        """Charge toutes les extensions."""
        cogs = [
            file
            for file in os.listdir("./cogs")
            if (file.endswith(".py") and file != "main.py")
        ]
        with progressbar.ProgressBar(max_value=len(cogs) + 1) as bar:
            bar.update(0)
            for i, filename in enumerate(cogs):
                bar.update(i + 1)
                self.bot.load_extension(f"cogs.{filename[:-3]}")
        print("Extension loaded:")  # les méthodes on_ready() dirons s'ils sont prêt

    # ######### #
    # Commandes #
    # ######### #

    @commands.command()
    @access.admin
    async def load(self, ctx: commands.Context, extension):
        """Charge une extension."""
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(fcite(f"L'extension **{extension}** à été chargée."))

    @commands.command()
    @access.admin
    async def load_all(self, ctx: commands.Context):
        """Charge toutes les extensions."""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "main.py":
                self.bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send(fcite("Tous les cogs ont été chargée."))

    @commands.command()
    @access.admin
    async def unload(self, ctx: commands.Context, extension):
        """Décharge une extension."""
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(fcite(f"L'extension **{extension}** à été déchargée."))

    @commands.command()
    @access.admin
    async def unload_all(self, ctx: commands.Context):
        """Décharge toutes les extensions."""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "main.py":
                self.bot.unload_extension(f"cogs.{filename[:-3]}")
        await ctx.send(fcite("Tous les cogs ont été déchargée."))

    @commands.command(name="reload")
    @access.admin
    async def _reload(self, ctx: commands.Context, extension):
        """Recharge une extension."""
        self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(fcite(f"L'extension **{extension}** à été rechargée."))

    @commands.command()
    @access.admin
    async def reload_all(self, ctx: commands.Context):
        """Recharge toutes les extensions."""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "main.py":
                self.bot.reload_extension(f"cogs.{filename[:-3]}")
        await ctx.send(fcite("Tous les cogs ont été rechargée."))

    @commands.group()
    async def cogs(self, ctx: commands.Context):
        """Affiche la liste des extensions."""
        if ctx.invoked_subcommand is None:
            txt = "- cogs.main\n"
            for ext in sorted(self.bot.extensions, reverse=True):
                txt += f"- {ext}\n"
            await ctx.send(fmarkdown(txt))

    @cogs.group()
    async def dev(self, ctx: commands.Context):
        """Affiche la liste des extensions en développement."""
        dev_cogs = [
            file[:-3]
            for file in os.listdir("./cogs/dev")
            if (file.endswith(".py"))
        ]
        txt = ""
        for dev_cog in dev_cogs:
            txt += f"- {dev_cog}\n"
        await ctx.send(fmarkdown(txt))

    @commands.command(aliases=["est_propriétaire", "est_propio"])
    async def is_owner(self, ctx: commands.Context, target: discord.Member = None):
        """Vérifie si cette personne est propriétaire du serveur.
		L'auteur de la commande est désigné comme target par défault.
		"""
        if target is None:
            if ctx.guild.owner_id == ctx.author.id:
                txt = "Vous êtes le propriétaire de ce serveur"
            else:
                txt = "Vous n'êtes pas le propriétaire de ce serveur"
        else:
            if ctx.guild.owner_id == target.id:
                txt = f"{target.name} est le propriétaire de ce serveur"
            else:
                txt = f"{target.name} n'êtes pas le propriétaire de ce serveur"
        await ctx.send(fcite(txt))

    @commands.command(aliases=["name_of_owner", "propriétaire", "propio"])
    async def owner(self, ctx: commands.Context):
        """Affiche le nom du propriétaire du serveur."""
        owner_name = await ctx.guild.fetch_member(ctx.guild.owner_id)
        await ctx.send(fcite(f"Le propriétaire du serveur est {owner_name}"))

    @commands.command()
    async def id(self, ctx: commands.Context, target: discord.Member = None):
        """Affiche l'id du membre."""
        if target is None:
            await ctx.send(fcite(f"Ton id est: {ctx.author.id}"))
        else:
            await ctx.send(fcite(f"L'id de {target.name} est: {target.id}"))

    @commands.command(aliases=["guild", "serveur"])
    async def server(self, ctx: commands.Context):
        """Affiche l'id du server."""
        await ctx.send(fcite(f"L'id du serveur est {ctx.guild.id}"))

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Affiche les informations générales de l'application."""
        text = open("data/md/info.md").read()
        emoji_os = (
            ":AppleOldLogo:" if str(
                platform.system()) == "Darwin" else "LinuxLogo"
        )
        os_info = str(platform.system()) + " / " + str(platform.release())
        em = discord.Embed(
            title="Informations sur Yukki",
            description=text.format(
                discord.__version__,
                Route.BASE,
                socket.gethostname(),
                os_info,
                platform.python_version(),
                emoji_os=emoji_os,
            ),
            colour=0x89C4F9,
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["effacer"])
    async def clear(self, ctx, n: int = 1):
        """Efface les <n> derniers messages."""
        async for message in ctx.message.channel.history(limit=n + 1):
            await message.delete()

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Affiche la latence."""
        ping_res = str(
            subprocess.Popen(
                ["/sbin/ping", "-c1", "discordapp.com"], stdout=subprocess.PIPE
            ).stdout.read()
        )
        formated_res = [item for item in ping_res.split() if "time=" in item]
        result = str(formated_res[0])[5:]
        if float(result) >= 200:
            em = discord.Embed(
                title="Ping : " + str(result) + "ms",
                description="... c'est quoi ce ping !",
                colour=0xFF1111,
            )
            await ctx.send(embed=em)
        elif 100 < float(result) < 200:
            em = discord.Embed(
                title="Ping : " + str(result) + "ms",
                description="Ca va, ça peut aller, mais j'ai "
                "l'impression d'avoir 40 ans !",
                colour=0xFFA500,
            )
            await ctx.send(embed=em)
        else:
            em = discord.Embed(
                title="Ping : " + str(result) + "ms",
                description="Wow c'te vitesse de réaction, je m'épate moi-même !",
                colour=0x11FF11,
            )
            await ctx.send(embed=em)


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Main(bot))
