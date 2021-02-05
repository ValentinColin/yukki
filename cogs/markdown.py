#!/usr/bin/env python3.9
"""Fichiers d'affichage de fichiers markdown."""
import os
import re
import discord
from discord.ext import commands
from tools.format import fmarkdown, fmdcheck


class Markdown(commands.Cog):
	"""Classe de gestion des fichiers markdown sur discord."""

	# ###### #
	# Events #
	# ###### #

	@commands.Cog.listener()
	async def on_ready(self):
		"""Déclare être prêt."""
		print('\tMarkdown\'s Cog is ready.')

	# ######### #
	# Functions #
	# ######### #

	def count_multi_index(self, path_file: str) -> list:
		"""Renvoie une liste de multi_index présent dans le fichier."""
		with open(path_file, 'r') as file:
			list_multi_index = []
			reg = re.compile(r'({...})') # pour trouver: {blablabla}
			for ligne in file:
				list_multi_index += reg.findall(ligne)
		return list_multi_index

	# ######### #
	# Commandes #
	# ######### #

	@commands.group(name='todo', aliases=[], help='Affiche le fichier todo.md')
	async def todo(self, ctx: commands.Context):
		"""Affiche le fichier todo.md."""
		if ctx.invoked_subcommand is None:
			with open('text/TODO.md', 'r') as todo_list:
				await ctx.send(fmarkdown(todo_list.read()))

	@todo.command(name='add', help='Ajouter un élément à la todo_list')
	async def add(self, ctx: commands.Context, *, txt: str):
		"""Ajouter un élément à la todo_list."""
		path_file = 'text/TODO.md'
		multi_index = None
		with open(path_file, 'r') as todo_list:
			await ctx.send('Not fully implemented yet')
			list_multi_index = count_multi_index(path_file)
			multi_index = list_multi_index[-1]
		with open(path_file, 'w') as todo_list:
			multi_index = ...
			todo_list.write(fmdcheck(txt+'\n', level=1))

	@todo.command(name='insert', aliases=[], help='Insère un élément à la todo-list')
	async def insert(self, ctx: commands.Context, multi_index: str, *, txt: str):
		"""Insère un élément à la todo-list."""
		await ctx.send('Not implemented yet')

	@todo.command(name='check', help='Coche une checkbox dans la todo-add', )
	async def check(self, ctx: commands.Context, multi_index: str):
		"""Coche une checkbox dans la todo-list."""
		await ctx.send('Not implemented yet')


def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Markdown(bot))