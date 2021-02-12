#!/usr/bin/env python

"""Les commandes de Marc sont partout."""

import os
import time
import shlex
import subprocess
import functools
import discord
import requests
import progressbar
import yaml

from discord.ext import commands


class Marc(commands.Cog):
    """Les commandes de Marc sont vraiment partout."""

    marc = "Marc"
    marc_id = 478552571510915072
    api_url = "https://api.github.com/repos/marcpartensky/discord-bot/git/trees/master?recursive=1"
    raw_url = "https://raw.githubusercontent.com/MarcPartensky/discord-bot/master"
    store = "marc_store.yml"

    def __init__(self, bot: commands.Bot):
        """Best commands are here."""
        self.bot = bot

    # c'est pour me chauffer
    @commands.command()
    async def who_is_marc(self, ctx: commands.Context):
        """Répond Marc est Marc."""
        await ctx.send(f"> **{Marc.marc}** est **Marc**.")

    @commands.command()
    async def is_marc_the_owner(self, ctx: commands.Context):
        """Évidemment on le sait tous!"""
        await ctx.send(__doc__)

    @commands.command()
    async def load_marc_cogs(self, ctx: commands.Context):
        """Charge les cogs de Marc."""

        cogs_path = os.path.join(os.getcwd(), "cogs")
        if not os.path.exists(cogs_path):
            os.makedirs(os.path.join(cogs_path))

        d = requests.get(Marc.api_url).json

        cogs = []
        for file_info in d["tree"]:
            if file_info["path"].startswith("cogs"):
                cogs.append(file_info["path"].replace("cogs"))
                text = requests.get(os.path.join(Marc.raw_url, file_info["path"])).text

                with open(cogs_path, "w") as f:
                    f.write(text)

        with progressbar.ProgressBar(max_value=len(cogs) + 1) as bar:
            bar.update(0)
            for i, filename in enumerate(cogs):
                bar.update(i + 1)
                self.bot.load_extension(f"cogs.{filename[:-3]}")

        await ctx.send("> **Done!**")

    @commands.group()
    async def marc(self, ctx: commands.Context):
        """Groupe de commandes de marc."""
        if not ctx.invoked_subcommand:
            raise Exception("Toutes les commandes de Marc sont permises!")

    @marc.command()
    async def run(self, ctx: commands.Context, *, command):
        """Run code."""
        await ctx.send(f"> Running: *{command}*")
        if ctx.author.id == Marc.marc_id:
            print(shlex.split(command))
            process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            # await ctx.send(f"> {process.stdout.read()}")
            await ctx.send(f"{stdout.decode('utf-8')}")
        else:
            time.sleep(1)
            await ctx.send("wait", delete_after=9)
            time.sleep(2)
            await ctx.send("humm", delete_after=7)
            time.sleep(2)
            await ctx.send("let me see", delete_after=5)
            time.sleep(2)
            await ctx.send("humm hummm", delete_after=3)
            time.sleep(3)
            await ctx.send("**NOPE**")

    @marc.command()
    async def website(self, ctx: commands.Context):
        """"Renvoie l'url du site de Marc."""
        await ctx.send("> https://marcpartensky.com")

    @marc.command()
    async def fourier(self, ctx: commands.Context):
        """Vive fourier."""
        await ctx.send(
            "https://camo.githubusercontent.com/49845b8edeb"
            "73d1e59403369c9a40e6d404eaa171dc27183fcfdd0537"
            "3c6ffbb/68747470733a2f2f63646e2e646973636f7264"
            "6170702e636f6d2f6174746163686d656e74732f353037"
            "3531393135373338373133323934302f38303830333930"
            "32343032323235373639342f666f75726965722e676966"
        )

    @marc.command()
    async def store(self, ctx: commands.Context, key: str, value: str):
        """Store something."""
        with open(Marc.marc_store, "r") as stream:
            d = yaml.safe_load(stream) 
        
        functools.reduce(dict.__getitem__, key.split('/'))
        # di = d.copy()
        # for ki in key.split('/'):
        #     if ki not in di:
        #         di = {}
        #     di = di[key]

        di[key] = value

        with 
        await ctx.send(f"> Stored in {key} : {value}")


def setup(bot: commands.Bot):
    """Setup le marc cog."""
    bot.add_cog(Marc(bot))
