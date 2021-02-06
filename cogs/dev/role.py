#!/usr/bin/env python3.9
"""Fichiers de gestion des rôles sur discord."""
import discord
from discord.ext import commands
from tools.format import fcite


class Role:
	"""Classe de gestion des rôles sur discord."""

	# ###### #
	# Events #
	# ###### #

	@commands.Cog.listener()
	async def on_ready(self):
		"""Déclare être prêt."""
		print('\tRole\'s Cog is ready.')

	# ######### #
	# Functions #
	# ######### #



	# ######### #
	# Commandes #
	# ######### #




def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Role(bot))