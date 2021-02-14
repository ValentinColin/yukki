#!/usr/bin/env python3.9
"""Fichiers de gestion des sondages."""
import re
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from dateutil import tz
from config import emoji
from tools.format import fcite, fcode



class Sondage(commands.Cog):
    """Classe de Sondage"""

    sep = " | "

    secondes = { # nombre de seconde dans l'unité correspondante
        "min": 60,
        "h": 60*60,
        "d": 60*60*24,
        "m": 60*60*24,
        "y": 60*60*24*12
    }

    default_unit = "min"

    def __init__(self, bot: commands.Bot):
        """"""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Sondage's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    @property
    def max_options(self):
        """Renvoie le nombre d'emoji numéroté."""
        return len(emoji.numbers)

    # ######### #
    # Commandes #
    # ######### #

    @commands.group()
    async def sondage(self, ctx: commands.Context):
        """Gestion des sondages."""
        if ctx.invoked_subcommand is None:
            text = open("data/md/sondage-help.md").read().format(self.default_unit)
            em = discord.Embed(
                title="Aide sur le sondage", description=text, colour=0xEEEEEE
            )
            await ctx.send(embed=em)

    @sondage.command(aliases=["créer", "crée"])
    async def create(self, ctx: commands.Context, *, message: str):
        """Créer un sondage.

        format de la commande:
        <question> ? [time=<Durée> | ]<rep 1> | <rep 2> [| <rep 3> ...]

        Si aucune durée n'est définie, le sondage ne s'arrétera pas.
        """
        await ctx.message.delete()
        options = message.replace("? ", "?" + Sondage.sep).split(Sondage.sep)
        question = options.pop(0)
        time = [x for x in options if x.startswith("time=")]
        if len(time) > 0:
            time = time[0]
            options.remove(time)
            time = time.strip("time=")
            unit = re.compile(r"(min|h|d|m|y)").findall(time) # On trouve l'unité
            if len(unit) > 0:
                unit = unit[0]
            else:
                unit = self.default_unit
            time = int(time.strip(unit)) # on retire l'unité
        else:
            time = None
        if len(options) < 2:  # Si il y a moins de 2 arguments
            raise commands.errors.MissingRequiredArgument
        if len(options) > self.max_options:  # Si il y a trop d'arguments
            return await ctx.send(fcite(
                f"{ctx.message.author.mention} >"
                f"{emoji.no_entry} Vous ne pouvez pas "
                f"mettre plus de {self.max_options} réponses !"
            ))

        to_react = []
        sondage_msg = f"**{question}**:\n\n"
        for index, option in enumerate(options):
            sondage_msg += f"{emoji.numbers[index]} - {option}\n"
            to_react.append(emoji.numbers[index])
        sondage_msg += f"\n*Sondage proposé par* {ctx.message.author.mention}"

        if time is not None:
            FRA = tz.gettz('Europe/Paris')

            now = datetime.now(tz=FRA)
            delta = timedelta(seconds=time * self.secondes[unit])
            date_stop = now + delta

            format_date = "%A %d %B - %H:%M"  # lundi 01 Janvier - 17:13
            str_date_stop = date_stop.strftime(format_date)

            sondage_msg += f"\n\nVous avez {time}{unit} pour voter!"
            sondage_msg += f"\n\nVous avez jusqu'au {str_date_stop} pour voter!"

        # Envoie du sondage et ajout des réactions
        poll_msg = await ctx.send(sondage_msg)
        for emote in to_react:
            await poll_msg.add_reaction(emote)

        # sleep puis résultat
        if time is not None:
            await asyncio.sleep(time * self.secondes[unit])

            # On synchronise l'état du message
            async for message in ctx.message.channel.history(limit=100):
                if message.id == poll_msg.id:
                    poll_msg = message

            results = {}  # dict -> emoji: count
            for reaction in poll_msg.reactions:
                if reaction.emoji in to_react:
                    results[reaction.emoji] = reaction.count - 1
            end_msg = "@everyone\nLe sondage est terminé. Voici les résultats:\n\n"
            for result in results:
                option = options[emoji.numbers.index(result)]
                end_msg += f"{result} {option} -> {results[result]} votes\n"
            best_emoji = max(results, key=lambda key: results[key])
            best_emojis = [x for x in results if results[x] == results[best_emoji]]
            if len(best_emojis) > 1:  # plusieurs gagnant
                top_results = []
                for key, value in results.items():
                    if value == results[best_emoji]:
                        top_results.append(options[emoji.numbers.index(key)])
                end_msg += "\nLes gagnants sont :" + "\n - ".join([""]+top_results)
            else:
                winner = options[emoji.numbers.index(best_emoji)]
                end_msg += f'\n"{winner}" est le gagnant!'
            await ctx.send(fcite(end_msg))
        else:
            await ctx.send(fcite("Pas de limite de temps."))

    @sondage.command(hidden=True)
    async def stop(self, ctx: commands.Context):
        """NotImplementedError !
        Arrête le sondage en cours."""
        raise NotImplementedError

    @sondage.command(aliases=["example"])
    async def exemple(self, ctx: commands.Context):
        """Affiche un exemple de sondage."""
        description = (
            "Voici un petit exemple de la commande à écrire pour pour crée un sondage:\n\n"
            "\t- Premier arguments: la question\n"
            "\t- Deuxième arguments (illimité par défaut): la durer du sondage\n"
            "\t\t └>où les unités possible sont décrites ici (par défault: {}):\n"
            "\t\t\t └> minutes = min\n"
            "\t\t\t └> heures  =   h\n"
            "\t\t\t └> jours   =   d\n"
            "\t\t\t └> mois    =   m\n"
            "\t\t\t └> années  =   y\n"
            "\t- Les autres arguments sont les réponses possibles au sondage\n\n"
        )
        description = description.format(self.default_unit)
        prefix = await self.bot.get_prefix(ctx.message)
        cmd = f"{prefix}sondage créer"
        question = "Quel âge avez-vous ? "
        options = [
            "time=1h",
            "Moins de 18 ans",
            "Plus de 18 ans",
            "Plus de 30 ans",
            "Plus de 50 ans",
        ]
        exemple = cmd + question + Sondage.sep.join(options)
        await ctx.send(fcode(description + exemple))


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Sondage(bot))
