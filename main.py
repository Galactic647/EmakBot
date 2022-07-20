#!/usr/bin/env python
# coding: utf-8

from core import custom_help as ch
from core.logger import logger
from cogs.utils import Utils
import config

from dotenv import load_dotenv
from discord.ext import commands
import discord

import os

load_dotenv()
client = commands.Bot(command_prefix='?')
client.owner_id = config.OWNER_ID


@client.event
async def on_ready() -> None:
    print(f'Bot ready!, logged as {client.user}')
    game = discord.Game('Gosip dengan tetangga')
    await client.change_presence(status=discord.Status.online, activity=game)

    logger.info(f'Logged as {client.user}')
    backup = Utils(client)
    await backup.regular_backup(config.BACKUP_INTERVAL)


@client.event
async def on_command_error(ctx, error) -> None:
    if isinstance(error, commands.errors.CommandInvokeError):
        if 'valueerror' in str(error).lower():
            await ctx.channel.send(':warning: Argumen yang diberikan invalid')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send(':warning: Argumen yang diberikan kurang')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.channel.send(f':warning: Command `{ctx.invoked_with}` tidak ditemukan')
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.channel.send(f':warning: Command ini hanya untuk owner dari bot ini')
    else:
        logger.error(error)


for ext in os.listdir('cogs'):
    if not ext.startswith('_') and ext.endswith('.py'):
        client.load_extension(f'cogs.{ext[:-3]}')

client.help_command = ch.CustomHelp()
client.run(os.getenv('BOT_TOKEN'))
