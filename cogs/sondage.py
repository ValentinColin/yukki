#!/usr/bin/env python3.9
"""Fichiers de gestion des sondages."""
import asyncio
import discord
from discord.ext import commands
from config import emoji
from tools.format import fcite, fcode


sep = " | "


class Sondage(commands.Cog):
    """Classe de Sondage"""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tSondage's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    @property
    def max_options(self):
        return len(emoji.numbers)

    # @property
    # def sep(self):
    # 	return cls._sep

    # @sep.setter
    # def sep(self, value):
    # 	cls._sep = value

    # ######### #
    # Commandes #
    # ######### #

    @commands.command(
        name="sondage",
        aliases=["stawpoll"],
        brief="Créer un sondage.",
        help=(
            "Crée un sondage de la forme:\n"
            f"\t.sondage <ma question> ? time=<Durée (min)> {sep} "
            f"<choix 1> {sep} <choix 2> [{sep} <choix 3> ...]"
        ),
    )
    async def sondage(self, ctx: commands.Context, *, msg="help"):
        """Créer un sondage."""
        if msg != "help":
            await ctx.message.delete()
            options = msg.replace("? ", "?" + sep).split(sep)
            question = options.pop(0)
            time = [x for x in options if x.startswith("time=")]
            if len(time) > 0:
                time = time[0]
                options.remove(time)
                time = int(time.strip("time="))
            else:
                time = None
            if len(options) < 2:  # Si il y a moins de 2 arguments
                raise commands.errors.MissingRequiredArgument
            if len(options) > self.max_options:  # Si il y a trop d'arguments
                return await ctx.send(
                    f"> {ctx.message.author.mention} >"
                    f"{emoji.no_entry} Vous ne pouvez pas "
                    f"mettre plus de {self.max_options} réponses !"
                )

            to_react = []
            sondage_msg = f"**{question}**:\n\n"
            for index, option in enumerate(options):
                sondage_msg += f"{emoji.numbers[index]} - {option}\n"
                to_react.append(emoji.numbers[index])
            sondage_msg += f"\n*Sondage proposé par* {ctx.message.author.mention}"

            if time is not None:
                sondage_msg += f"\n\nVous avez {time} minutes pour voter!"

            # Envoie du sondage et ajout des réactions
            poll_msg = await ctx.send(sondage_msg)
            for emote in to_react:
                await poll_msg.add_reaction(emote)

            # sleep + résultat
            print("ligne: ", 87, ", options: ", options)
            print("ligne: ", 88, ", time: ", time)
            if time is not None:
                await asyncio.sleep(time * 60)
                # On vas rechercher le message du sondage pour récupérer son nouvel état -> réctions ?
                async for message in ctx.message.channel.history(limit=100):
                    if message.id == poll_msg.id:
                        poll_msg = message
                results = {}  # dict -> emoji: count
                for reaction in poll_msg.reactions:
                    if reaction.emoji in to_react:
                        results[reaction.emoji] = reaction.count - 1
                end_msg = "Le sondage est terminé. Voici les résultats sont:\n\n"
                for result in results:
                    option = options[emoji.numbers.index(result) + 1]
                    end_msg += f"{result} {option} -> {results[result]} votes\n"
                best_emoji = max(results, key=lambda key: results[key])
                best_emojis = [x for x in results if results[x] == results[best_emoji]]
                if len(best_emojis) > 1:  # plusieurs gagnant
                    top_results = []
                    for key, value in results.items():
                        if value == results[best_emoji]:
                            top_results.append(options[emoji.numbers.index(key) + 1])
                    end_msg += "\nLes gagnants sont : " + "\n- ".join(top_results)
                else:
                    best_emoji = options[emoji.numbers.index(best_emoji) + 1]
                    end_msg += f'\n"{best_emoji}" est le gagnant!'
                await ctx.send(fcite(end_msg))
        else:
            await ctx.message.delete()

            text = open("texts/rpoll.md").read()
            em = discord.Embed(
                title="Aide sur le sondage", description=text, colour=0xEEEEEE
            )
            await ctx.send(embed=em)

    @commands.command(name="exemple", aliases=["example"], help="Exemple de sondage")
    async def exemple(self, ctx: commands.Context):
        """Affiche un exemple de sondage."""
        description = (
            "Voici un petit exemple de la commande à écrire pour pour crée un sondage:\n"
            "\t- Premier arguments: la question\n"
            "\t- Deuxième arguments: le temps (optionnel)\n"
            "\t- Les autres arguments sont les réponses possible au sondage\n\n"
        )
        cmd = ".sondage"
        question = "Quel âge avez-vous ?"
        options = [
            "time=1",
            "Moins de 18 ans",
            "Plus de 18 ans",
            "Plus de 30 ans",
            "Plus de 50 ans",
        ]
        txt = description + cmd + " " + question + " " + sep.join(options)
        await ctx.send(fcode(txt))


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Sondage(bot))
