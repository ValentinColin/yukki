#!/usr/bin/env python3.9
""""""
import urllib.request 	# bitcoin price
import requests			# cat
import asyncio			# ethylotest
import random 			# joke, ethylotest
import json 			# joke
import discord
from discord.ext import commands
from tools.format import fcite


class Fun(commands.Cog):
	"""Classe """

	# ###### #
	# Events #
	# ###### #

	@commands.Cog.listener()
	async def on_ready(self):
		"""Déclare être prêt."""
		print('\tFun\'s Cog is ready.')

	# ######### #
	# Commandes #
	# ######### #

	@commands.command(aliases=['dire'], help='Faire dire quelque chose au bot')
	async def say(self, ctx: commands.Context, *, txt: str = 'Donne moi un texte à dire.'):
		"""Fais dire un txt au bot."""
		await ctx.send(fcite(txt))

	@commands.command()
	async def btcprice(self, ctx: commands.Context):
		"""Le prix du BTC"""
		loading = await ctx.send("_réfléchis..._")
		try:
			url = urllib.request.urlopen("https://blockchain.info/fr/ticker")
			btc = json.loads(url.read().decode())
		except KeyError:
			btc = 1

		if btc == 1:
			await loading.edit(content="Impossible d'accèder à l'API"
									" blockchain.info, veuillez réessayer"
									" ultérieurment ! :c")
		else:
			frbtc = str(btc["EUR"]["last"]).replace(".", ",")
			usbtc = str(btc["USD"]["last"]).replace(".", ",")
			await loading.edit(content=f"Un bitcoin est égal à :"
									f" {usbtc}$US soit {frbtc}€.")

	@commands.command()
	async def joke(self, ctx: commands.Context, number: str = 0):
		"""Print a random joke in a json file"""
		with open('data/json/jokes.json') as data_json:
			joke_dict = json.load(data_json)

		try:
			if 0 < int(number) <= 9:
				clef = str(number)
			else:
				clef = str(random.randint(1, 15))
		except Exception:
			lef = str(random.randint(1, 15))

		joke = joke_dict[f'{clef}']

		embed = discord.Embed(title=f'Blague _{clef}_ : ',
							description=joke['content'], colour=0x03C9A9)
		embed.set_footer(text='Par ' + joke['author'])
		embed.set_thumbnail(url='https://outout.tech/tuxbot/blobjoy.png')
		await ctx.send(embed=embed)

	@commands.command()
	async def ethylotest(self, ctx: commands.Context):
		"""Ethylotest simulator 2018"""
		results_poulet = ["Désolé mais mon ethylotest est sous Windows Vista, "
						"merci de patienter...",
						"_(ethylotest)_ : Une erreur est survenue. Windows "
						"cherche une solution à se problème.",
						"Mais j'l'ai foutu où ce p\\*\\*\\* d'ethylotest de m\\*\\*\\* "
						"bordel fait ch\\*\\*\\*",
						"C'est pas possible z'avez cassé l'ethylotest !"]
		results_client = ["D'accord, il n'y a pas de problème à cela je suis "
						"complètement clean",
						"Bien sur si c'est votre devoir !", "Suce bi\\*e !",
						"J'ai l'air d'être bourré ?",
						"_laissez moi prendre un bonbon à la menthe..._"]
 
		result_p = random.choice(results_poulet)
		result_c = random.choice(results_client)

		await ctx.send(fcite(":oncoming_police_car: Bonjour bonjour,"
		    			" contrôle d'alcoolémie !"))
		await asyncio.sleep(0.5)
		await ctx.send(fcite(':man: ' + result_c))
		await asyncio.sleep(1)
		await ctx.send(fcite(':police_car: ' + result_p))

	@commands.command(name='cat', aliases=['randomcat'])
	async def randomcat(self, ctx):
		"""Display a random cat"""
		r = requests.get('http://aws.random.cat/meow')
		cat_url = str(r.json()['file'])
		embed = discord.Embed(title='Meow',
							description=f'[Voir le chat plus grand]({cat_url})',
							colour=0x03C9A9)
		embed.set_thumbnail(url=cat_url)
		embed.set_author(name='Random.cat', url='https://random.cat/')
		await ctx.send(embed=embed)
		await ctx.send(f'{cat_url}')


def setup(bot: commands.Bot):
	"""Setup the bot for the main cog."""
	bot.add_cog(Fun(bot))