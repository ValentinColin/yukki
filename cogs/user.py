#!/usr/bin/env python3.9
"""Fichier de gestion des intéraction avec les utilisateurs sur discord."""
import discord
from discord.ext import commands


class User(commands.Cog):
    """Classe de gestion des intéraction avec les utilisateurs sur discord."""

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("\tUser's Cog is ready.")

    # ######### #
    # Commandes #
    # ######### #

    @commands.command(help="Affiche l'avatar d'un membre")
    async def avatar(self, ctx: commands.Context, target: discord.Member = None):
        """Récuperer l'avatar de ..."""
        if target is None:
            target = ctx.message.author
        url_avatar = target.avatar_url_as()
        embed = discord.Embed(
            title="Avatar de : " + target.name,
            description=f"[Voir en plus grand]({url_avatar})",
        )
        embed.set_thumbnail(url=url_avatar)
        await ctx.send(embed=embed)

    @commands.command(
        brief="Poke quelqu'un",
        help="Poke quelqu'un. Anonymement ou non"
        " écrivans n'importe toi derrière le tag de la personne.",
    )
    async def poke(self, ctx: commands.Context, target: discord.Member, anonymous=None):
        """Poke quelqu'un. Anonymement ou non."""
        await ctx.message.delete()
        if anonymous:
            await ctx.send(f":clap: Hey {target.mention} tu t'es fait poker !")
        else:
            await ctx.send(
                f":clap: Hey {target.mention} tu t'es fait poker par "
                f"{ctx.message.author} !"
            )


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(User(bot))
