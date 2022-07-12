from EmakBot.globals import CHANNEL_IDS, warn_list, mute_list

import discord

from typing import Optional, Union
import inspect


def in_channels(has_user: Optional[bool] = False, has_target: Optional[bool] = False):
    def wrapper(func):
        if has_user and has_target:
            raise ValueError("A fuction can't have both user and target")
        elif has_user and not has_target:
            async def predicate(self, ctx, user: discord.Member, *args, **kwargs):
                if ctx.channel.id not in CHANNEL_IDS:
                    return
                await func(self, ctx, user, *args, **kwargs)

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
        elif not has_user and has_target:
            async def predicate(self, ctx, target: Union[discord.Member, str], *args, **kwargs):
                if ctx.channel.id not in CHANNEL_IDS:
                    return
                await func(self, ctx, target, *args, **kwargs)

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
        else:
            async def predicate(self, ctx, *args, **kwargs):
                if ctx.channel.id not in CHANNEL_IDS:
                    return
                await func(self, ctx, *args, **kwargs)

            predicate.__name__ = func.__name__
            predicate.__signature__ = inspect.signature(func)
            return predicate
    return wrapper


def self_check(func):
    async def predicate(self, ctx, user: discord.Member, *args, **kwargs):
        if (user == self.bot.user) or (ctx.author.id == user.id):
            await ctx.channel.send('Mabok ya bang?')
            return
        await func(self, ctx, user, *args, **kwargs)

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
