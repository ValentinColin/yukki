#!/usr/bin/env python3.9
"""Gestion de la prison sur discord."""
import discord
from discord.ext import commands
from config import emoji
from tools.access import access


class Jail(commands.Cog):
	"""Classe de gestion de la prison sur discord."""

	role_name = 'Jail'
	channel_name = 'jail'

	prisoners = [] # l.append('a') l.removed('a')

	# ###### #
	# Events #
	# ###### #

	@commands.Cog.listener()
	async def on_ready(self):
		"""Déclare être prêt."""
		print('\tJail\'s Cog is ready.')

	# ######### #
	# Commandes #
	# ######### #

	def get_role(self, ctx: commands.Context):
		"""Renvoie le rôle prisonnier."""
		return discord.utils.get(ctx.guild.roles, name=Jail.role_name)

	def get_voice_channel(self, ctx: commands.Context):
		"""Renvoie le channel vocal de la prison."""
		return discord.utils.get(ctx.guild.voice_channels, name=Jail.channel_name)

	@commands.command(name='jail', 
					aliases=['emprisonner', 'emprisonnement'], 
					help='Envoie une personne en prison')
	# @commands.has_role('Policeman')
	@commands.has_role('Policeman')
	async def jail(self, ctx: commands.Context, new_prisoner: discord.Member):
		"""Mettre une personne en prison."""
		jail_role = self.get_role(ctx)
		jail_voice_channel = self.get_voice_channel(ctx)
		try:
			await new_prisoner.edit(mute=True, 
							deafen=False, 
							roles=[jail_role], 
							voice_channel=jail_voice_channel, 
							reason="Tu es à présent en prison !")
		except:
			# await new_prisoner.add_roles(jail_role)
			# await new_prisoner.move_to(jail_voice_channel)
			await new_prisoner.edit(mute=True, 
							deafen=False, 
							roles=[jail_role])
		Jail.prisoners.append(new_prisoner)
		await ctx.send(f'> {emoji.lock} {new_prisoner.mention}, vous avez été placé en prison ! {emoji.lock}')

	@commands.command(name='unjail', 
					aliases=['liberer', 'liberation'], 
					help='Envoie une personne en prison')
	@commands.has_role('Policeman')
	async def unjail(self, ctx: commands.Context, new_free_user: discord.Member):
		"""Libérer une personne de prison."""
		jail_role = self.get_role(ctx)
		try:
			await new_free_user.edit(mute=False, 
							deafen=False, 
							roles=[], 
							#voice_channel=None, 
							reason="Tu n'as plus besoins d'être dans le channel de la prison")
		except:
			await new_free_user.remove_roles(jail_role)
			# await new_free_user.move_to(channel=None)
		Jail.prisoners.remove(new_free_user)
		await ctx.send(f'> {emoji.unlock} {new_free_user.mention}, vous avez été libéré de prison ! {emoji.unlock}')

	@commands.command(name='jail_visitor', aliases=['voir_prisonnier'], help='Voir la liste des prisonniers')
	async def jail_visitor(self, ctx: commands.Context):
		"""Voir la liste des prisonniers."""
		list_prisoners = '\n- '.join([''] + [prisoner.name for prisoner in Jail.prisoners])
		list_emoji = 10 * (emoji.jail + ' ')
		await ctx.send(f'```md\nListe des prisonniers: {list_emoji} {list_prisoners}```')

def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Jail(bot))