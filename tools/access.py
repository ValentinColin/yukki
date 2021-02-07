#!/usr/bin/env python3.9
"""Gestion des droits d'exécution des commandes du bot discord."""
import inspect
import discord
from discord.ext import commands
from config import emoji
from config.config import masters_id


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

    def admin(self, func):
        """Impose la condition d'être admin pour exécuter une commande."""

        async def decorated(obj, ctx: commands.Context, *args, **kwargs):
            if ctx.author.id in masters_id:
                return await func(obj, ctx, *args, **kwargs)
            else:
                await ctx.send(
                    "> " + self.rejection + " Il s'agit d'une commande administrateur."
                )

        decorated.__doc__ = self.admin_emoji + func.__doc__
        decorated.__name__ = func.__name__
        decorated.__signature__ = inspect.signature(func)
        return decorated

    def has_role(self, role):
        commands.has_role(role).__doc__
        return commands.has_role(role)

    def has_min_role(self, roles_authorized, nb_min: int = 1):
        """Renvoie un décorateur vérifiant que la personne possède au moins nb_min rôles."""

        def deco(func):
            """Limite l'accès à la fonction."""

            async def decorated(obj, ctx: commands.Context, *args, **kwargs):
                print("ctx.author.roles: ", ctx.author.roles)
                print("roles_authorized: ", roles_authorized)
                if (
                    len(
                        self.intersection(
                            [r.name for r in ctx.author.roles], roles_authorized
                        )
                    )
                    >= nb_min
                ):
                    return await func(obj, ctx, *args, **kwargs)
                else:
                    rejection = (
                        "```md\n"
                        + self.rejection
                        + f" Il s'agit d'une commande réservée aux personnes \
						possédant au moins {nb_min} de ces rôles: \n"
                    )
                    # for r in roles_authorized:
                    # 	rejection += '\n- ' + str(r)
                    rejection += "\n- ".join([""] + [str(r) for r in roles_authorized])
                    await ctx.send(rejection + "\n```")

            decorated.__doc__ = func.__doc__
            decorated.__name__ = func.__name__
            decorated.__signature__ = inspect.signature(func)
            return decorated

        return deco


access = Access(masters_id)
