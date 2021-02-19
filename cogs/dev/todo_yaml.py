#!/usr/bin/env python3.9

"""Fichiers d'affichage des fichiers Todo."""

import yaml
import discord
from discord.ext import commands
from tools.access import access



class Todo(commands.Cog):
    """Classe de gestion des fichiers Todo sur discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Todo's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    def get_todo_from_yaml(self):
        """Renvoie le dictionnaire générer le fichier Yaml."""
        with open("data/yaml/todo.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def generate_md(self, id_user, data):
        """Génère le markdown à partir du Yaml."""
        todo_list = data[str(id_user)] # todo["1"]["2"]["3"]["description"] -> "blabla"
        return todo_list

    # ######### #
    # Commandes #
    # ######### #

    @commands.group()
    async def todo(self, ctx: commands.Context):
        """Affiche le fichier todo.md."""
        if ctx.invoked_subcommand is None:
            pass

    @todo.command(aliases=["ajouter"])
    @access.me
    async def add(self, ctx: commands.Context, *, txt: str):
        """Ajouter un élément à la todo_list."""
        pass

    @todo.command(aliases=["retirer", "supprimer"])
    @access.me
    async def remove(self, ctx, *, multi_index: str):
        """Supprime une ligne de la todo-list."""
        pass

    @todo.command(aliases=["inserer", "insérer"])
    @access.me
    async def insert(self, ctx: commands.Context, father_multi_index: str, *, txt: str):
        """Insère un sous-tâche à la todo-list.

        exemple:
            .todo insert 1.2.3 Je ne doit pas oublié de mettre le lait avant les céréales
        """
        pass

    @todo.command(aliases=["valider"])
    @access.me
    async def check(self, ctx: commands.Context, multi_index):
        """Coche une checkbox dans la todo-list."""
        await ctx.send("Not implemented yet")


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Todo(bot))
