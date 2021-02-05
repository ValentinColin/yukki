#!/usr/bin/env python3.9
"""An example file for test the discord API."""
import discord
from discord.ext import commands
from tools.format import fcite


class Example(commands.Cog):
	""""""

	# ###### #
	# Events #
	# ###### #

	@commands.Cog.listener()
	async def on_ready(self):
		"""Déclare être prêt."""
		print('\tExample\'s Cog is ready.')

	# ######### #
	# Commandes #
	# ######### #

	@commands.command(help='ping pong!')
	async def ping(self, ctx: commands.Context):
		"""Ping pong."""
		await ctx.send(fcite('Pong!'))

	@commands.command(aliases=['dire'], help='Faire dire quelque chose au bot')
	async def say(self, ctx: commands.Context, *, txt: str = 'Donne moi un texte à dire.'):
		"""Fais dire un txt au bot."""
		await ctx.send(fcite(txt))

	@commands.command(name='test', help='Commande de test/brouillon', hidden=True)
	async def test(self, ctx, *args, **kwargs):
		"""Commande de test/brouillon."""
		await ctx.send('Cette commande ne fait rien du tout.')
		

def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Example(bot))