#!/usr/bin/env python3.9
# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members ({len(guild.members)} members):\n - {members}')

@bot.command(name='make-chan', help='Create a channel')
@commands.has_any_role('admin')
async def create_channel(ctx: commands.Context, *, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await ctx.send(f'The channel {channel_name} is ready !')
    else:
        print(f'The channel {channel_name} already exist')
        await ctx.send(f'The channel {channel_name} already exist')

@bot.command(name='rm-chan', help='remove a channel')
@commands.has_any_role('admin')
async def remove_channel(ctx: commands.Context, *, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel is not None:
        print(f'The channel {channel_name} has been removed !')
        await existing_channel.delete()
        try:
            await ctx.send(f'The channel {channel_name} has been removed !')
        except:
            pass
    else:
        print(f'The channel {channel_name} doesn\'t exist')
        await ctx.send(f'The channel {channel_name} doesn\'t exist')

@bot.event
async def on_command_error(ctx: commands.Context, error):
    """Envoie l'erreur aux utilisateurs."""
        message = str(error)
        if message[-1]!=".": message+="."
        await ctx.send(message)
        raise error


if __name__ == '__main__':
	bot.run(TOKEN)


	