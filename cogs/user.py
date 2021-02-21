#!/usr/bin/env python3.9

"""Fichier de gestion des intéraction avec les utilisateurs sur discord."""

import discord
from discord.ext import commands
from tools.access import access
from tools.format import fcite


class User(commands.Cog):
    """Classe de gestion des intéraction avec les utilisateurs sur discord."""

    def __init__(self, bot: commands.Bot):
        """Create the main cog using the bot as argument."""
        self.bot = bot

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    User's Cog is ready.")

    # ######### #
    # Commandes #
    # ######### #

    @commands.command()
    async def avatar(self, ctx: commands.Context, target: discord.Member = None):
        """Affiche l'avatar d'un membre."""
        if target is None:
            target = ctx.message.author
        url_avatar = target.avatar_url_as()
        embed = discord.Embed(
            title="Avatar de : " + target.name,
            description=f"[Voir en plus grand]({url_avatar})",
        )
        embed.set_thumbnail(url=url_avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def user_info(self, ctx: commands.Context, target: discord.Member = None):
        """Affiche l'avatar d'un membre."""
        if target is None:
            target = ctx.message.author
        url_avatar = target.avatar_url_as()
        info = {
            "Id": target.id,
            "Nom": target.name,
            "Surnom": target.nick,
            "Avatar": f"[Voir en plus grand]({url_avatar})",
            "À créé son compte à": target.created_at,
            "À rejoint le serveur à": target.joined_at,
        }
        if info["Surnom"] is None:
            info["Surnom"] = "~~Pas de surnom~~"

        txt = "\n - ".join([""] + [f"{key} : {val}" for key, val in info.items()])
        embed = discord.Embed(
            title=f"Informations sur {target.name}",
            description=txt,
            colour=target.top_role.color,
        )
        embed.set_thumbnail(url=url_avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def poke(self, ctx: commands.Context, target: discord.Member, anonymous=None):
        """Poke quelqu'un. Anonymement ou non.
        Écrire n'importe toi derrière le tag de la personne pour être anonyme.
        """
        await ctx.message.delete()
        if anonymous:
            await ctx.send(f":clap: Hey {target.mention} tu t'es fait poker !")
        else:
            await ctx.send(
                f":clap: Hey {target.mention} tu t'es fait poker par "
                f"{ctx.message.author} !"
            )

    @commands.command(hidden=True)
    @access.admin
    async def move(
        self, ctx: commands.Context, channel: discord.VoiceChannel, *users: discord.Member
    ):
        """Déplace le membre vers un salon vocal."""
        await ctx.message.delete()
        for user in users:
            await user.move_to(channel)

    @commands.command()
    @access.admin
    async def disconnect(self, ctx: commands.Context, *users: discord.Member):
        """Déplace le membre vers un salon vocal."""
        await ctx.message.delete()
        for user in users:
            await user.move_to(None)

    @commands.command()
    @access.admin
    async def mute(self, ctx: commands.Context, *users: discord.Member):
        """Déplace le membre vers un salon vocal."""
        await ctx.message.delete()
        for user in users:
            await user.edit(mute=True)

    @commands.command()
    @access.admin
    async def unmute(self, ctx: commands.Context, *users: discord.Member):
        """Déplace le membre vers un salon vocal."""
        await ctx.message.delete()
        for user in users:
            await user.edit(mute=False)

    @commands.command()
    @access.admin
    async def rename(self, ctx: commands.Context, user: discord.Member, *, nickname: str = None):
        """Rename un membre.
        Ne pas donner d'arguments permet de retirer le surnom.
        """
        await user.edit(nick=nickname)

    @commands.command(aliases=["envoie", "mp", "dm"])
    async def send(self, ctx: commands.Context, member: discord.Member, *, msg: str):
        """Envoie un messages privée à un membre."""
        txt = f"Message **{msg}** envoyé."
        print(ctx.message.channel)
        print(type(ctx.message.channel))
        channel_type = type(ctx.message.channel)
        if channel_type is discord.TextChannel:  # channel textuel de server
            await member.send(msg)
        elif channel_type is discord.DMChannel:  # message privée avec une seul personne
            await ctx.channel.send(msg)
        elif channel_type is discord.GroupChannel:  # message privée avec une seul personne
            await ctx.channel.send(msg)
        else:
            txt = "J'ai pas réussi à envoyer le message."
        await ctx.send(fcite(txt))



def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(User(bot))
