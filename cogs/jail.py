#!/usr/bin/env python3.9

"""Gestion de la prison sur discord."""

import yaml
import discord
from discord.ext import commands
from config import emoji
from tools.access import access
from tools.format import fcite, fmarkdown, fcode


class Jail(commands.Cog):
    """Classe de gestion de la prison sur discord."""

    role_name = "Jail"
    channel_name = "jail"

    # ###### #
    # Events #
    # ###### #

    @commands.Cog.listener()
    async def on_ready(self):
        """Déclare être prêt."""
        print("    Jail's Cog is ready.")

    # ######### #
    # Functions #
    # ######### #

    @classmethod
    def get_jail_role(cls, ctx: commands.Context):
        """Renvoie le rôle prisonnier."""
        return discord.utils.get(ctx.guild.roles, name=cls.role_name)

    @classmethod
    def get_jail_voice_channel(cls, ctx: commands.Context):
        """Renvoie le channel vocal de la prison."""
        return discord.utils.get(ctx.guild.voice_channels, name=cls.channel_name)

    @staticmethod
    def save_roles(ctx: commands.Context, prisoner: discord.Member):
        """Sauvegarde les roles du prisonnier."""
        id_server = str(ctx.guild.id)
        prisoner_roles_id = [role.id for role in prisoner.roles]
        with open("data/yaml/bot.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if id_server not in data["servers"]:
            data["servers"][id_server] = data["servers"]["default"]

        # Ajout du prisonnier et ses rôles à la liste des prisonniers,
        # si il n'y es pas déjà.
        data["servers"][id_server]["prisoners"][str(prisoner.id)] = prisoner_roles_id

        with open("data/yaml/bot.yml", "w") as f:
            yaml.dump(data, f)

    @staticmethod
    def get_roles(ctx: commands.Context, user: discord.Member):
        """Récupère les anciens rôles du prisonnier.
        Et supprime le prisonnier de la liste des prisonnier."""
        id_server = str(ctx.guild.id)
        with open("data/yaml/bot.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        # Stock les rôles à renvoyer
        user_roles_id = data["servers"][id_server]["prisoners"][str(user.id)]
        # Supprime le prisonnier de la bdd
        del data["servers"][id_server]["prisoners"][str(user.id)]
        with open("data/yaml/bot.yml", "w") as f:
            yaml.dump(data, f)
        return user_roles_id

    def get_prisoners(self, id_server: int):
        """Renvoie la liste des personnes en prison."""
        with open("data/yaml/bot.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return [prisoner for prisoner in data["servers"][str(id_server)]["prisoners"]]

    # ######### #
    # Commandes #
    # ######### #

    @commands.command(aliases=["emprisonner", "emprisonnement"])
    @access.has_role("Policeman")
    async def jail(self, ctx: commands.Context, new_prisoner: discord.Member):
        """Envoie une personne en prison."""
        self.save_roles(ctx, new_prisoner)
        minus_roles = new_prisoner.roles[1:]
        plus_roles = [self.get_jail_role(ctx)]
        dashboard_roles = "\n - ".join([""] + [role.name for role in minus_roles])
        dashboard_roles += "\n + ".join([""] + [role.name for role in plus_roles])
        await new_prisoner.edit(
            mute=True,
            deafen=False,
            roles=[self.get_jail_role(ctx)],
            voice_channel=self.get_jail_voice_channel(ctx),
            reason="Tu es à présent en prison !",
        )
        await new_prisoner.move_to(self.get_jail_voice_channel(ctx))
        txt = (
            f"{emoji.lock} {new_prisoner.mention}, "
            f"vous avez été placé en prison ! {emoji.lock}\n"
            f"> Tes rôles ne t'appartiennent plus !"
        )
        await ctx.send(fcite(txt))
        await ctx.send(fcode(dashboard_roles, "md"))

    @commands.command(aliases=["liberer", "liberation"])
    @access.has_role("Policeman")
    async def unjail(self, ctx: commands.Context, new_free_user: discord.Member):
        """Libérer une personne de prison."""
        user_roles_id = self.get_roles(ctx, new_free_user)
        user_roles = []
        for role in ctx.guild.roles:
            if role.id in user_roles_id:
                user_roles.append(role)

        minus_roles = [self.get_jail_role(ctx)]
        plus_roles = [role for role in user_roles]
        dashboard_roles = "\n - ".join([""] + [role.name for role in minus_roles])
        dashboard_roles += "\n + ".join([""] + [role.name for role in plus_roles])

        await new_free_user.edit(
            mute=False,
            deafen=False,
            roles=user_roles,
            reason="Tu es libéré de prison !",
        )
        txt = (
            f"{emoji.unlock} {new_free_user.mention}, "
            f"vous avez été libéré de prison ! {emoji.unlock}\n"
            f"> Tu peux récupérer ce qui t'appartient."
        )
        await ctx.send(fcite(txt))
        await ctx.send(fcode(dashboard_roles, "md"))

    @commands.command(aliases=["voir_prisonnier"])
    async def jail_visitor(self, ctx: commands.Context):
        """Voir la liste des prisonniers."""
        list_prisoners = "\n- ".join(
            [""] + [prisoner.name for prisoner in self.get_prisoners(ctx.guild.id)]
        )
        list_emoji = 10 * (emoji.jail + " ")
        txt = f"Liste des prisonniers: {list_emoji} {list_prisoners}"
        await ctx.send(fmarkdown(txt))


def setup(bot: commands.Bot):
    """Setup the bot for the main cog."""
    bot.add_cog(Jail(bot))
