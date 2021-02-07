#!/usr/bin/env python3.9
"""Fichiers d'affichage de fichiers json."""
import os
import re
import json
import discord
from discord.ext import commands
from config.config import path_todo_json
from tools.format import fcite, fmarkdown, fmdcheck
from tools.multi_index import MultiIndex


class Todo:
    """Classe de gestion des fichiers json sur discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tTodo's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    def read_from_json(path_json: str):
        """Lire un json de todo."""
        with open(path_json) as json_data:
            return json.load(json_data)

    # ######### #
    # Commandes #
    # ######### #

    @commands.group(name="todo", help="Affiche le fichier todo.json")
    async def todo(self, ctx: commands.Context):
        """Affiche le fichier todo.md."""
        if ctx.invoked_subcommand is None:
            with open(path_todo_list, "r") as todo_list:
                await ctx.send(fmarkdown(todo_list.read()))


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Todo(bot))
