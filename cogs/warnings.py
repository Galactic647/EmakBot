from core import functions as func, descriptions as desc, decorators
from core.moderation import Warn
from core.logger import logger
import config

from discord.ext import commands
import discord

from typing import Optional, Union
import asyncio


class Warnings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.WARN_BRIEF, description=desc.WARN)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def warn(self, ctx, target: Union[discord.Member, str], reason: str,
                   level: Optional[int] = 1, duration: Optional[str] = None) -> Union[dict, None]:
        level = max(1, min(2, level))

        for msg_id, warn_obj in config.warn_list.items():
            if target == warn_obj.user:
                if warn_obj.level + 1 > 2:
                    await ctx.channel.send(f'User `{target}` sudah berada pada :warning: warn level tertinggi')
                    return

                duration = duration if duration is not None else config.DEFAUT_DURATION.get('warn-2')
                embed = func.embedder('Warning', msg_id, ctx.author.mention, target, target.avatar_url, reason,
                                      duration, level=2)

                warn_obj.duration = func.time_process(duration)
                warn_obj.reason = reason
                warn_obj.level = 2

                await func.process_message(self, ctx, embed, target,
                                           config.USER_PREFIX['warn'].format(2, duration, reason))
                asyncio.ensure_future(warn_obj.count_down())
                return config.warn_list[msg_id].info()

        msg_id = func.generate_id()
        if duration is None:
            duration = config.DEFAUT_DURATION.get('warn-1') if level == 1 else config.DEFAUT_DURATION.get('warn-2')

        config.warn_list[msg_id] = Warn(self.bot, ctx.author, target, duration, reason, msg_id, level)
        embed = func.embedder('Warning', msg_id, ctx.author.mention, target, target.avatar_url, reason,
                              duration, level)
        await func.process_message(self, ctx, embed, target, config.USER_PREFIX['warn'].format(level, duration, reason))

        asyncio.ensure_future(config.warn_list[msg_id].count_down())
        return config.warn_list[msg_id].info()

    @commands.command(brief=desc.REMOVEWARN_BRIEF, description=desc.REMOVEWARN)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def removewarn(self, ctx, target: Union[discord.Member, str], reason: str) -> dict:
        warn_obj = config.warn_list.get(target)

        await warn_obj.interrupt()
        msg = config.ADMIN_PREFIX['remove_warn'].format(warn_obj.user, reason)
        await func.process_message(self, ctx, msg, warn_obj.user, config.USER_PREFIX['remove_warn'].format(reason))

        del config.warn_list[target]
        return warn_obj.info()

    @commands.command(brief=desc.LOWERWARN_BRIEF, description=desc.LOWERWARN)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def lowerwarn(self, ctx, target: Union[discord.Member, str],
                        reason: str, duration: Optional[str] = None) -> Union[dict, None]:
        warn_obj = config.warn_list.get(target)

        if warn_obj.level - 1 < 1:
            await ctx.channel.send(f'User `{warn_obj.user}` sudah berada pada :warning: level terendah')
            return

        await warn_obj.interrupt()
        if duration is None:
            duration = config.DEFAUT_DURATION.get('warn-1')

        warn_obj.level -= 1
        warn_obj.duration = func.time_process(duration)
        msg = config.ADMIN_PREFIX['lower_warn'].format(warn_obj.user, warn_obj.level, duration, reason)
        await func.process_message(self, ctx, msg, warn_obj.user,
                                   config.USER_PREFIX['lower_warn'].format(warn_obj.level, duration, reason))

        asyncio.ensure_future(warn_obj.count_down())
        return warn_obj.info()

    @commands.command(brief=desc.SILENTWARN_BRIEF, description=desc.SILENTWARN)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def silentwarn(self, ctx, target: Union[discord.Member, str], reason: str, level: Optional[int] = 1,
                         duration: Optional[str] = None, silent: Optional[bool] = False) -> Union[dict, None]:
        level = max(1, min(2, level))

        for msg_id, warn_obj in config.warn_list.items():
            if target == warn_obj.user:
                if warn_obj.level + 1 > 2:
                    await ctx.channel.send(f'User `{target}` sudah berada pada :warning: warn level tertinggi')
                    return

                duration = duration if duration is not None else config.DEFAUT_DURATION.get('warn-2')

                warn_obj.duration = func.time_process(duration)
                warn_obj.reason = reason
                warn_obj.level = 2

                if not silent:
                    embed = func.embedder('Warning', msg_id, ctx.author.mention, target, target.avatar_url, reason,
                                          duration, level=2)
                    await ctx.channel.send(embed=embed)
                asyncio.ensure_future(warn_obj.count_down())
                return warn_obj.info()

        msg_id = func.generate_id()
        if duration is None:
            duration = config.DEFAUT_DURATION.get('warn-1') if level == 1 else config.DEFAUT_DURATION.get('warn-2')

        config.warn_list[msg_id] = Warn(self.bot, ctx.author, target, duration, reason, msg_id, level)
        if not silent:
            embed = func.embedder('Warning', msg_id, ctx.author.mention, target, target.avatar_url, reason,
                                  duration, level)
            await ctx.channel.send(embed=embed)

        asyncio.ensure_future(config.warn_list[msg_id].count_down())
        return config.warn_list[msg_id].info()

    @commands.command(brief=desc.SILENTREMOVEWARN_BRIEF, description=desc.SILENTREMOVEWARN)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def silentremovewarn(self, ctx, target: Union[discord.Member, str], silent: Optional[bool] = False) -> dict:
        warn_obj = config.warn_list.get(target)

        await warn_obj.interrupt()
        if not silent:
            await ctx.channel.send(config.ADMIN_PREFIX['remove_warn'].format(warn_obj.user, 'silent'))
        
        del config.warn_list[target]
        return warn_obj.info()

    @commands.command(brief=desc.WARNINFO_BRIEF, description=desc.WARNINFO)
    @decorators.in_channels(has_target=False)
    async def warninfo(self, ctx) -> None:
        
        embed = discord.Embed(title='Warning List', color=func.color_picker())

        for index, items in enumerate(config.warn_list.items()):
            msg_id, warn_obj = items

            data = f'```User: {warn_obj.user}\n' \
                   f'Level: {warn_obj.level}\n' \
                   f'Durasi: {func.time_convert(warn_obj.duration)}\n' \
                   f'Reason: {warn_obj.reason}```'
            embed.add_field(name=f'{index + 1}. {msg_id}', value=data, inline=False)
        if not config.warn_list:
            embed.description = 'Kosong bang'

        embed.set_footer(
            text=f'Total warning: {len(config.warn_list)} • Hari ini pada {func.get_time(no_date=True, thformat=True)}'
        )
        await ctx.channel.send(embed=embed)

    @commands.command(brief=desc.ASCENDMUTE_BRIEF, description=desc.ASCENDMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def ascendmute(self, ctx, target: Union[discord.Member, str],
                         reason: str, duration: Optional[str] = None) -> None:
        warn_obj = config.warn_list.get(target)

        if warn_obj.level < 2:
            await ctx.channel.send(f':warning: Level warn user {warn_obj.user} tidak cukup')
            return

        await ctx.channel.send(f'Warn user {warn_obj.user} telah di ascend ke mute')
        del config.warn_list[target]
        await ctx.invoke(self.bot.get_command('mute'), user=warn_obj.user, reason=reason, duration=duration)

    @commands.command(brief=desc.ASCENDKICK_BRIEF, description=desc.ASCENDKICK)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def ascendkick(self, ctx, target: Union[discord.Member, str], reason: str) -> None:
        warn_obj = config.warn_list.get(target)

        if warn_obj.level < 2:
            await ctx.channel.send(f':warning: Level warn user {warn_obj.user} tidak cukup')
            return

        del config.warn_list[target]
        await ctx.invoke(self.bot.get_command('kick'), user=warn_obj.user, reason=reason)

    @commands.command(brief=desc.ASCENDBAN_BRIEF, description=desc.ASCENDBAN)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='warn')
    async def ascendban(self, ctx, target: Union[discord.Member, str], reason: str,
                        duration: Optional[str] = 'Permanent') -> None:
        warn_obj = config.warn_list.get(target)

        if warn_obj.level < 2:
            await ctx.channel.send(f':warning: Level warn user {warn_obj.user} tidak cukup')
            return

        del config.warn_list[target]
        await ctx.invoke(self.bot.get_command('ban'), user=warn_obj.user, reason=reason, duration=duration)


def setup(bot):
    bot.add_cog(Warnings(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
