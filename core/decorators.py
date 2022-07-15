from globals import CHANNEL_IDS, ERROR_MESSAGE, GUILD_ID, warn_list, mute_list
from core.logger import logger

import discord

from typing import Optional, Union
import inspect


def in_channels(has_target: Optional[bool] = False):
    def wrapper(func):
        if has_target:
            async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
                async with ctx.typing():
                    try:
                        if ctx.channel.id not in CHANNEL_IDS:
                            return
                        await func(self, ctx, target, *args, **kwargs)
                    except Exception as e:
                        await ctx.channel.send(ERROR_MESSAGE.format(e))
                        logger.error(e)
                    else:
                        logger.info(f'User {ctx.author} use {func.__name__} at target {target}')

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
        else:
            async def predicate(self, ctx, *args, **kwargs):
                async with ctx.typing():
                    try:
                        if ctx.channel.id not in CHANNEL_IDS:
                            return
                        await func(self, ctx, *args, **kwargs)
                    except Exception as e:
                        await ctx.channel.send(ERROR_MESSAGE.format(e))
                        logger.error(e)
                    else:
                        logger.info(f'User {ctx.author} use {func.__name__}')

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
    return wrapper


def self_check(func):
    async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
        if isinstance(target, str):
            guild = await self.bot.fetch_guild(GUILD_ID)
            try:
                target = await guild.fetch_member(target)
            except discord.HTTPException:
                await ctx.channel.send(f'Tidak ada user dengan id {target} di server ini')
                return
        if (target == self.bot.user) or (ctx.author.id == target.id):
            await ctx.channel.send('Mabok ya bang?')
            return
        await func(self, ctx, target, *args, **kwargs)

    predicate.__name__ = func.__name__
    predicate.__signature__ = inspect.signature(func)
    return predicate


def target_check(type_: str):
    def wrapper(func):
        mod_obj = None
        if type_.lower() == 'warn':
            mod_obj = warn_list
        elif type_.lower() == 'mute':
            mod_obj = mute_list
        else:
            raise ValueError(f'Unknown type {type_}')

        async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
            mod_id = None
            if isinstance(target, discord.Member):
                if target not in [value.user for _, value in mod_obj.items()]:
                    await ctx.channel.send(f'Tidak ada :warning: {type_.lower()} dengan user {target}')
                    return
                mod_id = [value for _, value in mod_obj.items()][0].id_
            elif isinstance(target, str):
                if target not in mod_obj:
                    await ctx.channel.send(f'Tidak ada :warning: {type_.lower()} dengan id {target}')
                    return
                mod_id = target
            await func(self, ctx, mod_id, *args, **kwargs)

        predicate.__name__ = func.__name__
        predicate.__signature__ = inspect.signature(func)
        return predicate
    return wrapper
