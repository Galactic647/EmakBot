from core.logger import logger
import config

import discord

from typing import Optional, Union
import inspect
import json


def in_channels(has_target: Optional[bool] = False):
    def wrapper(func):
        if has_target:
            async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
                async with ctx.typing():
                    try:
                        if ctx.channel.id not in config.CHANNEL_IDS:
                            return
                        detail = await func(self, ctx, target, *args, **kwargs)
                    except Exception as e:
                        await ctx.channel.send(config.ERROR_MESSAGE.format(e))
                        logger.error(f'{"-" * 80}\n{e}\n{"-" * 80}')
                    else:
                        if not detail or detail is None:
                            logger.info(f'User {ctx.author} use {func.__name__}')
                        else:
                            logger.info(f'User {ctx.author} use {func.__name__}, details:\n'
                                        f'{"-" * 80}\n'
                                        f'{json.dumps(detail, indent=4)}\n'
                                        f'{"-" * 80}')

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
        else:
            async def predicate(self, ctx, *args, **kwargs):
                async with ctx.typing():
                    try:
                        if ctx.channel.id not in config.CHANNEL_IDS:
                            return
                        detail = await func(self, ctx, *args, **kwargs)
                    except Exception as e:
                        await ctx.channel.send(config.ERROR_MESSAGE.format(e))
                        logger.error(f'{"-" * 80}\n{e}\n{"-" * 80}')
                    else:
                        if not detail or detail is None:
                            logger.info(f'User {ctx.author} use {func.__name__}')
                        else:
                            logger.info(f'User {ctx.author} use {func.__name__}, details:\n'
                                        f'{"-" * 80}\n'
                                        f'{json.dumps(detail, indent=4)}\n'
                                        f'{"-" * 80}')

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
    return wrapper


def self_check(func):
    async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
        if isinstance(target, str):
            guild = await self.bot.fetch_guild(config.GUILD_ID)
            try:
                target = await guild.fetch_member(target)
            except discord.HTTPException:
                await ctx.channel.send(f'Tidak ada user dengan id {target} di server ini')
                return
        if (target == self.bot.user) or (ctx.author.id == target.id):
            await ctx.channel.send('Mabok ya bang?')
            return
        return await func(self, ctx, target, *args, **kwargs)

    predicate.__name__ = func.__name__
    predicate.__signature__ = inspect.signature(func)
    return predicate


def target_check(type_: str):
    def wrapper(func):
        mod_obj = None
        if type_.lower() == 'warn':
            mod_obj = config.warn_list
        elif type_.lower() == 'mute':
            mod_obj = config.mute_list
        else:
            raise ValueError(f'Unknown type {type_}')

        async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
            msg_id = None
            if isinstance(target, discord.Member):
                if target not in [value.user for _, value in mod_obj.items()]:
                    await ctx.channel.send(f'Tidak ada :warning: {type_.lower()} dengan user {target}')
                    return
                msg_id = [value for _, value in mod_obj.items() if value.user == target][0].id_
            elif isinstance(target, str):
                if target in mod_obj:
                    msg_id = target
                else:
                    guild = await self.bot.fetch_guild(config.GUILD_ID)
                    try:
                        target = await guild.fetch_member(target)
                        msg_id = target.id
                    except discord.HTTPException:
                        await ctx.channel.send(f'Tidak ada user ataupun {type_} dengan id {target} di server ini')
                        return
            await func(self, ctx, msg_id, *args, **kwargs)

        predicate.__name__ = func.__name__
        predicate.__signature__ = inspect.signature(func)
        return predicate
    return wrapper
