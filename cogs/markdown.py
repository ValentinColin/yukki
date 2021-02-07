#!/usr/bin/env python3.9
"""Fichiers d'affichage de fichiers markdown."""
import os
import re
import json
import discord
from discord.ext import commands
from config.config import path_todo_list, path_todo_json
from tools.format import fcite, fmarkdown, fmdcheck
from tools.multi_index import MultiIndex


class Markdown(commands.Cog):
    """Classe de gestion des fichiers markdown sur discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tMarkdown's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    def read_todo_from_json(path_json: str):
        """Lire un json de todo."""
        with open(path_json) as json_data:
            return json.load(json_data)

    # ######### #
    # Commandes #
    # ######### #

    @commands.group(name="todo", help="Affiche le fichier todo.md")
    async def todo(self, ctx: commands.Context):
        """Affiche le fichier todo.md."""
        if ctx.invoked_subcommand is None:
            with open(path_todo_list, "r") as todo_list:
                await ctx.send(fmarkdown(todo_list.read()))

    @todo.command(
        name="ajouter", aliases=["add"], help="Ajouter un élément à la todo_list"
    )
    async def add(self, ctx: commands.Context, *, txt: str):
        """Ajouter un élément à la todo_list."""
        with open(path_todo_list, "a") as todo_list:
            list_multi_index = MultiIndex.extract(
                path_file=path_todo_list, regex=r"{[\d\.]*}"
            )
            multi_index = list_multi_index[-1]
            new_multi_index = multi_index + 1
            txt_formatted = f"{{{multi_index}}} " + txt + "\n"
            todo_list.write(fmdcheck(txt_formatted, level=1))
        await ctx.send(fcite("Ajouter à la todo-list !"))

    @todo.command(
        name="retirer",
        aliases=["remove", "supprimer"],
        help="Supprime une ligne de la todo-list",
    )
    async def remove(self, ctx, *, multi_index: str):
        """Supprime une ligne de la todo-list."""
        with open(path_todo_list, "r+") as todo_list:
            lines = todo_list.readlines()
            todo_list.seek(0)
            for line in lines:
                if f"{{{multi_index}}}" not in line:
                    todo_list.write(line)
            todo_list.truncate()
        await ctx.send(fcite("Supprimer de la todo-list !"))

    @todo.command(
        name="insérer",
        aliases=["inserer", "insert"],
        brief="Insère un sous-tâche à la todo-list",
        help="Insère un sous-tâche à la todo-list en donnant la tâche parente en paramètre.",
    )
    async def insert(self, ctx: commands.Context, father_multi_index: str, *, txt: str):
        """Insère une sous-tâche à la todo-list."""
        await ctx.send(fcite("Not worked !"))
        return None
        with open(path_todo_list, "r+") as todo_list:
            father_multi_index = MultiIndex(father_multi_index)
            list_multi_index = father_multi_index.extract(path_todo_list)
            children = father_multi_index.children(list_multi_index)

            if len(children) > 0:
                last_child = children[-1]
            else:
                last_child = None
            lvl = father_multi_index.level + 1

            lines = todo_list.readlines()
            todo_list.seek(0)
            for line in lines:
                todo_list.write(line)
                if last_child is not None:
                    if f"{{{last_child}}}" in line:
                        txt_formatted = f"{{{last_child + 1}}} " + txt + "\n"
                        todo_list.write(fmdcheck(txt_formatted, level=lvl))
                else:
                    if f"{{{father_multi_index}}}" in line:
                        txt_formatted = (
                            f"{{{father_multi_index.make_child(i=1)}}} " + txt + "\n"
                        )
                        todo_list.write(fmdcheck(txt_formatted, level=lvl))

    @todo.command(
        name="valider",
        aliases=["fini", "check"],
        help="Coche une checkbox dans la todo-add",
    )
    async def check(self, ctx: commands.Context, multi_index: MultiIndex):
        """Coche une checkbox dans la todo-list."""
        await ctx.send("Not implemented yet")


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Markdown(bot))
