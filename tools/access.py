#!/usr/bin/env python3.9
"""Gestion des droits d'exécution des commandes du bot discord."""
import functools  # @functools.wraps(func) est un décorateurs à mettre sur new_func() dans un décorateur
import inspect
import discord
from discord.ext import commands
from config import emoji
from config.config import my_id, masters_id
from tools.format import fcite, fmarkdown


class Access:
    """Classe de décorateur d'accès aux fonction."""

    def __init__(self, masters_id, rejection="Vous n'avez pas les droits."):
        self.masters = masters_id
        self.rejection = rejection
        self.admin_emoji = emoji.admin

    # ######### #
    # Functions #
    # ######### #

    def get_role(self, ctx: commands.Context, role_name):
        """Renvoie le rôle prisonnier."""
        return discord.utils.get(ctx.guild.roles, name=role_name)

    def get_roles(self, ctx: commands.Context, roles: list):
        """Renvoie la liste des rôles."""
        return [self.get_role(ctx, role) for role in roles]

    def intersection(self, list1, list2):
        """Renvoie l'intersection de 2 listes."""
        return list(set(list1) & set(list2))

    # ########### #
    # Decorateurs #
    # ########### #

    def me(self, func):
        """Impose la condition d'être admin pour exécuter une commande."""

        @functools.wraps(func)
        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id == my_id:
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(
                    fcite(self.rejection +
                          " Il s'agit d'une commande administrateur.")
                )

        decorated.__doc__ = "[Créateur] " + func.__doc__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def admin(self, func):
        """Impose la condition d'être admin pour exécuter une commande."""

        @functools.wraps(func)
        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id in masters_id:
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(
                    fcite(self.rejection + " Il s'agit d'une commande administrateur.")
                )

        decorated.__doc__ = self.admin_emoji + " " + func.__doc__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def has_role(self, role):
        commands.has_role(role).__doc__
        return commands.has_role(role)

    def has_roles(self, roles_authorized: list, nb_min: int = 1):
        """Renvoie un décorateur vérifiant que la personne possède au moins nb_min rôles."""

        def deco(func):
            """Limite l'accès à la fonction."""

            @functools.wraps(func)
            async def decorated(obj, ctx: commands.Context, *args, **kwargs):
                print("ctx.author.roles: ", ctx.author.roles)
                print("roles_authorized: ", roles_authorized)
                author_roles = [r.name for r in ctx.author.roles]
                if len(self.intersection(author_roles, roles_authorized)) >= nb_min:
                    return await func(obj, ctx, *args, **kwargs)
                else:
                    txt = (
                        self.rejection
                        + f" Il s'agit d'une commande réservée aux personnes \
						possédant au moins {nb_min} de ces rôles: \n"
                    )
                    txt += "\n- ".join([""] + [str(r) for r in roles_authorized])
                    await ctx.send(fmarkdown(txt))

            decorated.__signature__ = inspect.signature(func)
            return decorated

        return deco

access = Access(masters_id)
