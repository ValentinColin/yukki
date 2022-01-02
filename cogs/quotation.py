#!/usr/bin/env python3.9

"""Fichier de gestion des citations."""

import yaml
import datetime
import random
import discord
from discord.ext import commands
from config import emoji

from tools.format import fcite, fmarkdown


class Quotation(commands.Cog):
    """Classe principale de gestion des citations."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Quotation's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    @staticmethod
    def get_categories() -> list:
        """Récupérer la liste des catégories."""
        with open("data/yaml/quote.yml") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data["famous"].keys()

    @staticmethod
    def get_famous_quotes(category: str) -> list:
        """Récupérer les citations connu d'une catégorie."""
        with open("data/yaml/quote.yml") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data["famous"][category]

    @staticmethod
    def get_user_quotes(target: discord.Member) -> list:
        """Récupérer les citations connu d'une catégorie."""
        with open("data/yaml/quote.yml") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data["users"][target.name]

    @staticmethod
    def add_user_quote(target: discord.Member, quotation: str) -> None:
        """Ajoute une citation."""
        with open("data/yaml/quote.yml") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        if str(target.id) not in data["users"]:
            data["users"][str(target.id)] = []
        quotation_dict = {
            "quotation": quotation,
            "date": datetime.date.today()
        }
        data["users"][str(target.id)].append(quotation_dict)
        with open("data/yaml/quote.yml", "w") as f:
            yaml.dump(data, f)

    # ######### #
    # Commandes #
    # ######### #

    @commands.command(aliases=["cite", "citation", "quotation"])
    async def quotes(self, ctx: commands.Context, *, category: str = None):
        """Renvoie une citation appartenant à une catégorie.
        Si aucune catégorie n'est donnée renvoie la liste des catégories.
        """
        if category is None:
            categories = list(self.get_categories())
            txt = "Catégories disponible:"
            txt += "\n -".join([""] + categories)
            await ctx.send(fmarkdown(txt))
        else:
            quotes = self.get_famous_quotes(category)
            rand_quote = random.choice(quotes)
            txt = rand_quote["quotation"] + "\n" + f"*{rand_quote['author']}*"
            await ctx.send(fcite(txt))

    '''
    @commands.command()#aliases=["cite", "citation", "quotation"])
    async def quotess(self, ctx: commands.Context, *, category: str):
        """Renvoie une citation appartenant à une catégorie."""
        data = self.get_famous_quotes(category)
        txt = data["quotation"] + "\n"+ f"*{data['author']}*"
        await ctx.send(fcite(txt))
    '''

    @commands.command(aliases=["mirai", "nikki", "yuno"])
    async def yukki(self, ctx: commands.Context):
        """Renvoie une citation aléatoire de l'anime Mirai Nikki."""
        quotes = self.get_famous_quotes("Mirai Nikki")
        rand_quote = random.choice(quotes)
        txt = rand_quote["quotation"] + "\n" + f"*{rand_quote['author']}*"
        await ctx.send(fcite(txt))

    

def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Quotation(bot))
