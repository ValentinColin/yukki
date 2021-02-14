#!/usr/bin/env python3.9

"""Gestion des droits d'exécution des commandes du bot discord."""

import functools  # @functools.wraps(func) est un décorateurs à mettre sur new_func() dans un décorateur
import yaml
import inspect
import discord
from discord.ext import commands
from config import emoji
from config.config import my_id
from tools.format import fcite, fmarkdown


class Access:
    """Classe de décorateur d'accès aux fonction."""

    def __init__(self):
        self.masters = Access.get_masters_id()
        self.rejection = "Vous n'avez pas les droits. "
        self.admin_emoji = emoji.admin

    # ######### #
    # Functions #
    # ######### #

    @staticmethod
    def get_my_id() -> int:
        """Renvoie mon id."""
        with open("data/yaml/bot.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["bot"]["my_id"]

    @staticmethod
    def get_masters_id() -> list:
        """Renvoie la liste des admins au sens du bot."""
        with open("data/yaml/bot.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["bot"]["masters_id"]

    @staticmethod
    def get_role(ctx: commands.Context, role_name):
        """Renvoie le rôle prisonnier."""
        return discord.utils.get(ctx.guild.roles, name=role_name)

    @classmethod
    def get_roles(cls, ctx: commands.Context, roles: list):
        """Renvoie la liste des rôles."""
        return [cls.get_role(ctx, role) for role in roles]

    @staticmethod
    def intersection(list1, list2):
        """Renvoie l'intersection de 2 listes."""
        return list(set(list1) & set(list2))

    # ########### #
    # Decorateurs #
    # ########### #

    def me(self, func):
        """Impose la condition d'être le créateur du bot pour exécuter une commande."""

        @functools.wraps(func)
        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id == self.get_my_id():
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(fcite("Va te faire foutre ! Tu n'es pas mon maître !"))
                await ctx.message.add_reaction(emoji.poop)

        decorated.__doc__ = "[Créateur] " + func.__doc__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def admin(self, func):
        """Impose la condition d'être admin pour exécuter une commande."""

        @functools.wraps(func)
        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id in self.get_masters_id():
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(
                    fcite(self.rejection + "Il s'agit d'une commande administrateur.")
                )

        decorated.__doc__ = self.admin_emoji + " " + func.__doc__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def server_owner(self, func):
        """Restreint l'exécution de la commande aux propriétaire du serveur."""

        @functools.wraps(func)
        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id == ctx.guild.owner.id:
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(fcite(
                    self.rejection
                    + "Il s'agit d'une commande pour le propriétaire du serveur."
                ))

        decorated.__doc__ = self.admin_emoji + " " + func.__doc__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def has_role(self, role):
        """Alias du décorateur de discord"""
        return commands.has_role(role)

    def has_roles(self, roles_authorized: list, nb_min: int = 1):
        """Renvoie un décorateur vérifiant que la personne possède au moins nb_min rôles."""

        def deco(func):
            """Limite l'accès à la fonction."""

            @functools.wraps(func)
            async def decorated(obj, ctx: commands.Context, *args, **kwargs):
                author_roles = [r.name for r in ctx.author.roles]
                if len(self.intersection(author_roles, roles_authorized)) >= nb_min:
                    return await func(obj, ctx, *args, **kwargs)
                else:
                    txt = (
                        self.rejection
                        + f"Il s'agit d'une commande réservée aux personnes"
                        + f"possédant au moins {nb_min} de ces rôles: \n"
                    )
                    txt += "\n- ".join([""] + [str(r) for r in roles_authorized])
                    await ctx.send(fmarkdown(txt))

            decorated.__signature__ = inspect.signature(func)
            return decorated

        return deco


access = Access()
