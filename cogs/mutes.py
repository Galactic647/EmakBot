from core import functions as func, descriptions as desc, moderation as mod, decorators
from core.logger import logger
import config

from discord.ext import commands
import discord

from typing import Optional, Union
import asyncio


class Mutes(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.MUTE_BRIEF, description=desc.MUTE)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def mute(self, ctx, target: Union[discord.Member, str], reason: str,
                   duration: Optional[str] = None) -> Union[dict, None]:
        mute_role = func.get_role(ctx, role='Mute')
        duration = duration if duration is not None else config.DEFAUT_DURATION.get('mute')

        for msg_id, mute_obj in config.mute_list.items():
            if target == mute_obj.user and 'Server' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url,
                                      reason, duration, 'Server')
                await func.process_message(self, ctx, embed, target,
                                           config.USER_PREFIX['mute'].format('Server', duration, reason))
                asyncio.ensure_future(mute_obj.count_down())
                return mute_obj.info()

        msg_id = func.generate_id()

        config.mute_list[msg_id] = mod.Mute(self.bot, ctx.author, target, duration, reason, msg_id)
        embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url,
                              reason, duration, 'Server')
        await target.add_roles(mute_role)
        await func.process_message(self, ctx, embed, target,
                                   config.USER_PREFIX['mute'].format('Server', duration, reason))

        asyncio.ensure_future(config.mute_list[msg_id].count_down())
        return config.mute_list[msg_id].info()

    @commands.command(brief=desc.UNMUTE_BRIEF, description=desc.UNMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def unmute(self, ctx, target: Union[discord.Member, str], reason: str) -> None:
        mute_obj = config.mute_list.get(target)
        mute_role = func.get_role(ctx, role='Mute')

        msg = config.ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, reason)

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        await func.process_message(self, ctx, msg, mute_obj.user,
                                   config.USER_PREFIX['unmute'].format(mute_obj.type_, reason))

        del config.mute_list[target]
        return mute_obj.info()

    @commands.command(brief=desc.LSMUTE_BRIEF, description=desc.LSMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def lsmute(self, ctx, target: Union[discord.Member, str], reason: str,
                     duration: Optional[str] = None) -> Union[dict, None]:
        lsmute_role = func.get_role(ctx, role='Livestream Mute')
        duration = duration if duration is not None else config.DEFAUT_DURATION.get('mute')
        duration = 'Permanent' if 'permanent' == duration.lower() else duration

        for msg_id, mute_obj in config.mute_list.items():
            if target == mute_obj.user and 'Livestream' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url,
                                      reason, duration, 'Livestream')
                await func.process_message(self, ctx, embed, target,
                                           config.USER_PREFIX['mute'].format('Livestream', duration, reason))
                asyncio.ensure_future(mute_obj.count_down())
                return mute_obj.info()

        msg_id = func.generate_id()

        config.mute_list[msg_id] = mod.LSMute(self.bot, ctx.author, target, duration, reason, msg_id,
                                              True if duration == 'Permanent' else False)
        embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url, reason, duration,
                              'Livestream')

        await target.add_roles(lsmute_role)
        await func.process_message(self, ctx, embed, target,
                                   config.USER_PREFIX['mute'].format('Livestream', duration, reason))

        asyncio.ensure_future(config.mute_list[msg_id].count_down())
        return config.mute_list[msg_id].info()

    @commands.command(brief=desc.UNLSMUTE_BRIEF, description=desc.UNLSMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def unlsmute(self, ctx, target: Union[discord.Member, str], reason: str) -> None:
        mute_obj = config.mute_list.get(target)
        mute_role = func.get_role(ctx, role='Livestream Mute')

        msg = config.ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, reason)

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        await func.process_message(self, ctx, msg, mute_obj.user,
                                   config.USER_PREFIX['unmute'].format(mute_obj.type_, reason))

        del config.mute_list[target]
        return mute_obj.info()

    @commands.command(brief=desc.SILENTMUTE_BRIEF, description=desc.SILENTMUTE, hidden=True)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def silentmute(self, ctx, target: Union[discord.Member, str], reason: str, duration: Optional[str] = None,
                         silent: Optional[bool] = False) -> None:
        mute_role = func.get_role(ctx, role='Mute')
        duration = duration if duration is not None else config.DEFAUT_DURATION.get('mute')

        for msg_id, mute_obj in config.mute_list.items():
            if target == mute_obj.user and 'Server' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                if not silent:
                    embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url,
                                          reason, duration, 'Server')
                    await ctx.channel.send(embed=embed)

                asyncio.ensure_future(mute_obj.count_down())
                return mute_obj.info()

        msg_id = func.generate_id()

        config.mute_list[msg_id] = mod.Mute(self.bot, ctx.author, target, duration, reason, msg_id)
        await target.add_roles(mute_role)

        if not silent:
            embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url, reason, duration,
                                  'Server')
            await ctx.channel.send(embed=embed)

        asyncio.ensure_future(config.mute_list[msg_id].count_down())
        return config.mute_list[msg_id].info()

    @commands.command(brief=desc.SILENTUNMUTE_BRIEF, description=desc.SILENTUNMUTE, hidden=True)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def silentunmute(self, ctx, target: Union[discord.Member, str], silent: Optional[bool] = False) -> None:
        mute_obj = config.mute_list.get(target)
        mute_role = func.get_role(ctx, role='Mute')

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)

        if not silent:
            await ctx.channel.send(config.ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, 'silent'))

        del config.mute_list[target]
        return mute_obj.info()

    @commands.command(brief=desc.SILENTLSMUTE_BRIEF, description=desc.SILENTLSMUTE, hidden=True)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def silentlsmute(self, ctx, target: Union[discord.Member, str], reason: str, duration: Optional[str] = None,
                           silent: Optional[bool] = False) -> None:
        lsmute_role = func.get_role(ctx, role='Livestream Mute')
        duration = duration if duration is not None else config.DEFAUT_DURATION.get('mute')
        duration = 'Permanent' if 'permanent' == duration.lower() else duration

        for msg_id, mute_obj in config.mute_list.items():
            if target == mute_obj.user and 'Livestream' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                if not silent:
                    embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url,
                                          reason, duration, 'Livestream')
                    await ctx.channel.send(embed=embed)
                asyncio.ensure_future(mute_obj.count_down())
                return mute_obj.info()

        msg_id = func.generate_id()

        config.mute_list[msg_id] = mod.LSMute(self.bot, ctx.author, target, duration, reason, msg_id,
                                              True if duration == 'Permanent' else False)
        await target.add_roles(lsmute_role)

        if not silent:
            embed = func.embedder('Mute', msg_id, ctx.author.mention, target, target.avatar_url, reason, duration,
                                  'Livestream')
            await ctx.channel.send(embed=embed)

        asyncio.ensure_future(config.mute_list[msg_id].count_down())
        return config.mute_list[msg_id].info()

    @commands.command(brief=desc.SILENTUNLSMUTE_BRIEF, description=desc.SILENTUNLSMUTE, hidden=True)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def silentunlsmute(self, ctx, target: Union[discord.Member, str], silent: Optional[bool] = False) -> None:
        mute_obj = config.mute_list.get(target)
        mute_role = func.get_role(ctx, role='Livestream Mute')

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)

        if not silent:
            await ctx.channel.send(config.ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, 'silent'))

        del config.mute_list[target]
        return mute_obj.info()

    @commands.command(brief=desc.MUTEINFO_BRIEF, description=desc.MUTEINFO)
    @decorators.in_channels(has_target=False)
    async def muteinfo(self, ctx) -> None:
        embed = discord.Embed(title='Mute List', color=func.color_picker())

        for index, items in enumerate(config.mute_list.items()):
            msg_id, mute_obj = items
            data = f'```User: {mute_obj.user}\n' \
                   f'Type: {mute_obj.type_}\n' \
                   f'Durasi: {func.time_convert(mute_obj.duration)}\n' \
                   f'Reason: {mute_obj.reason}```'
            embed.add_field(name=f'{index + 1}. {msg_id}', value=data, inline=False)
        if not config.mute_list:
            embed.description = 'Kosong bang'

        embed.set_footer(
            text=f'Total mute: {len(config.mute_list)} • Hari ini pada {func.get_time(no_date=True, thformat=True)}'
        )
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Mutes(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
