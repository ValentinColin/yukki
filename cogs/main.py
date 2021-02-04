#!/usr/bin/env python3.9
"""Fichier principale du bot."""
import os
import discord
import progressbar
from discord.ext import commands
from tools.access import access


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
		print('\tMain\'s Cog is ready.')

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
		if message[-1] != '.': message += '.'
		await ctx.send(message)
		raise error

	# ######### #
	# Functions #
	# ######### #

	def load_cogs(self):
		"""Charge toutes les extensions."""
		cogs = os.listdir('./cogs')
		with progressbar.ProgressBar(max_value=len(cogs)-1) as bar:
			for i,filename in enumerate(cogs):
				bar.update(i)
				if filename.endswith('.py') and filename != 'main.py':
					self.bot.load_extension(f"cogs.{filename[:-3]}")
		print('Extension loaded:')

	# ######### #
	# Commandes #
	# ######### #
	
	@commands.command(help='Charge une extension')
	@commands.has_role('MASTER')
	async def load(self, ctx: commands.Context, extension):
		"""Charge une extension."""
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f'> L\'extension **{extension}** à été chargée.')

	@commands.command(help='Charge toutes les extensions')
	@commands.has_role('MASTER')
	async def load_all(self, ctx: commands.Context):
		"""Charge toutes les extensions."""
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.bot.load_extension(f'cogs.{filename[:-3]}')
		await ctx.send('> Tous les cogs ont été chargée.')

	@commands.command(help='Décharge une extension')
	@commands.has_role('MASTER')
	async def unload(self, ctx: commands.Context, extension):
		"""Décharge une extension."""
		self.bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f'> L\'extension **{extension}** à été déchargée.')

	@commands.command(help='Décharge toutes les extensions')
	@commands.has_role('MASTER')
	async def unload_all(self, ctx: commands.Context):
		"""Décharge toutes les extensions."""
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.bot.unload_extension(f'cogs.{filename[:-3]}')
		await ctx.send('> Tous les cogs ont été déchargée.')

	@commands.command(help='Recharge toutes les extensions')
	@commands.has_role('MASTER')
	async def reload(self, ctx: commands.Context, extension):
		"""Recharge une extension."""
		self.bot.reload_extension(f'cogs.{extension}')
		await ctx.send(f'> L\'extension **{extension}** à été rechargée.')

	@commands.command(help='Recharge toutes les extensions')
	@commands.has_role('MASTER')
	async def reload_all(self, ctx: commands.Context):
		"""Recharge toutes les extensions."""
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.bot.reload_extension(f'cogs.{filename[:-3]}')
		await ctx.send('> Tous les cogs ont été rechargée.')

	@commands.command(name='id', help="Renvoie l'id de la personne qui exécute la commande")
	async def id(self, ctx: commands.Context, target: discord.Member = None):
		"""Documentation of the function."""
		if target is None:
			await ctx.send(f'> Ton id est: {ctx.author.id}')
		else:
			await ctx.send(f'> L\'id de {target.name} est: {target.id}')

	@commands.command(name='is_owner', 
					aliases=['est_propriétaire', 'est_propio'],
					brief='Vérifie s\'il s\'agit du propriétaire',
					help='Vérifie si la target est le propriétaire du serveur. \
						L\'auteur de la commande est désigné comme target par défault.')
	async def is_owner(self, ctx: commands.Context, target: discord.Member = None):
		"""Documentation of the function."""
		if target is None:
			if ctx.guild.owner_id == ctx.author.id:
				txt = "Vous êtes le propriétaire de ce serveur"
			else:
				txt = "Vous n'êtes pas le propriétaire de ce serveur"
		else:
			if ctx.guild.owner_id == target.id:
				txt = f'{target.name} est le propriétaire de ce serveur'
			else:
				txt = f'{target.name} n\'êtes pas le propriétaire de ce serveur'
		await ctx.send(txt)

	@commands.command(name='owner', 
					aliases=['propriétaire', 'propio'],
					help='Affiche le nom du propriétaire de ce serveur')
	async def name_of_owner(self, ctx: commands.Context):
		"""Affiche dans le channel le nom du propriétaire du serveur."""
		owner_name = await ctx.guild.fetch_member(ctx.guild.owner_id)
		await ctx.send(f'Le propriétaire du serveur est {owner_name}')

def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Main(bot))