from globals import DEFAUT_DURATION, USER_PREFIX, ADMIN_PREFIX, mute_list
from core import functions as func, descriptions as desc, moderation as mod, decorators
from core.logger import logger

from discord.ext import commands
import discord

from typing import Optional, Union
import json


class Mutes(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.MUTE_BRIEF, description=desc.MUTE)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def mute(self, ctx, user: discord.Member, reason: str, duration: Optional[str] = None) -> None:
        mute_role = func.get_role(ctx, role='Mute')
        duration = duration if duration is not None else DEFAUT_DURATION.get('mute')

        for msg_id, mute_obj in mute_list.items():
            if user == mute_obj.user and 'Server' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url,
                                      reason, duration, 'Server')
                await func.process_message(self, ctx, embed, user,
                                           USER_PREFIX['mute'].format('Server', duration, reason))
                await mute_obj.count_down()
                return

        msg_id = func.generate_id()

        mute_list[msg_id] = mod.Mute(self.bot, ctx.author, user, duration, reason, msg_id)
        embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url, reason, duration, 'Server')
        await user.add_roles(mute_role)
        await func.process_message(self, ctx, embed, user, USER_PREFIX['mute'].format('Server', duration, reason))

        logger.info(f'User {ctx.author} mute a user, info\n{json.dumps(mute_list[msg_id].info(), indent=4)}')
        await mute_list[msg_id].count_down()

    @commands.command(brief=desc.UNMUTE_BRIEF, description=desc.UNMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def unmute(self, ctx, target: Union[discord.Member, str], reason: str) -> None:
        mute_obj = mute_list.get(target)
        mute_role = func.get_role(ctx, role='Mute')

        msg = ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, reason)

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        await func.process_message(self, ctx, msg, mute_obj.user, USER_PREFIX['unmute'].format(mute_obj.type_, reason))

        logger.info(f'User {ctx.author} unmute a user, info\nuser: {mute_obj.user}\nreason: {reason}')
        del mute_list[target]

    @commands.command(brief=desc.LSMUTE_BRIEF, description=desc.LSMUTE)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def lsmute(self, ctx, user: discord.Member, reason: str, duration: Optional[str] = None) -> None:
        lsmute_role = func.get_role(ctx, role='Livestream Mute')
        duration = duration if duration is not None else DEFAUT_DURATION.get('mute')
        duration = 'Permanent' if 'permanent' == duration.lower() else duration

        for msg_id, mute_obj in mute_list.items():
            if user == mute_obj.user and 'Livestream' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url,
                                      reason, duration, 'Livestream')
                await func.process_message(self, ctx, embed, user,
                                           USER_PREFIX['mute'].format('Livestream', duration, reason))
                await mute_obj.count_down()
                return

        msg_id = func.generate_id()

        mute_list[msg_id] = mod.LSMute(self.bot, ctx.author, user, duration, reason, msg_id,
                                       True if duration == 'Permanent' else False)
        embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url, reason, duration,
                              'Livestream')

        await user.add_roles(lsmute_role)
        await func.process_message(self, ctx, embed, user, USER_PREFIX['mute'].format('Livestream', duration, reason))

        logger.info(f'User {ctx.author} mute a user, info\n{json.dumps(mute_list[msg_id].info(), indent=4)}')
        await mute_list[msg_id].count_down()

    @commands.command(brief=desc.UNLSMUTE_BRIEF, description=desc.UNLSMUTE)
    @decorators.in_channels(has_target=True)
    @decorators.target_check(type_='mute')
    async def unlsmute(self, ctx, target: Union[discord.Member, str], reason: str) -> None:
        mute_obj = mute_list.get(target)
        mute_role = func.get_role(ctx, role='Livestream Mute')

        msg = ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, reason)

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        await func.process_message(self, ctx, msg, mute_obj.user, USER_PREFIX['unmute'].format(mute_obj.type_, reason))

        logger.info(f'User {ctx.author} unmute a user, info\nuser: {mute_obj.user}\nreason: {reason}')
        del mute_list[target]

    @commands.command(brief=desc.SILENTMUTE_BRIEF, description=desc.SILENTMUTE, hidden=True)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def silentmute(self, ctx, user: discord.Member, reason: str, duration: Optional[str] = None,
                         silent: Optional[bool] = False) -> None:
        mute_role = func.get_role(ctx, role='Mute')
        duration = duration if duration is not None else DEFAUT_DURATION.get('mute')

        for msg_id, mute_obj in mute_list.items():
            if user == mute_obj.user and 'Server' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                if not silent:
                    embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url,
                                          reason, duration, 'Server')
                    await ctx.channel.send(embed=embed)

                await mute_obj.count_down()
                return

        msg_id = func.generate_id()

        mute_list[msg_id] = mod.Mute(self.bot, ctx.author, user, duration, reason, msg_id)
        await user.add_roles(mute_role)

        if not silent:
            embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url, reason, duration,
                                  'Server')
            await ctx.channel.send(embed=embed)

        logger.info(f'User {ctx.author} mute a user, info\n{json.dumps(mute_list[msg_id].info(), indent=4)}')
        await mute_list[msg_id].count_down()

    @commands.command(brief=desc.SILENTUNMUTE_BRIEF, description=desc.SILENTUNMUTE, hidden=True)
    @decorators.in_channels(has_user=True)
    @decorators.target_check(type_='mute')
    async def silentunmute(self, ctx, target: Union[discord.Member, str], silent: Optional[bool] = False) -> None:
        mute_obj = mute_list.get(target)
        mute_role = func.get_role(ctx, role='Mute')

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        
        if not silent:
            await ctx.channel.send(ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, 'silent'))
        
        logger.info(f'User {ctx.author} unmute a user, info\nuser: {mute_obj.user}\nreason: silent')
        del mute_list[target]

    @commands.command(brief=desc.SILENTLSMUTE_BRIEF, description=desc.SILENTLSMUTE, hidden=True)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def silentlsmute(self, ctx, user: discord.Member, reason: str, duration: Optional[str] = None,
                           silent: Optional[bool] = False) -> None:
        lsmute_role = func.get_role(ctx, role='Livestream Mute')
        duration = duration if duration is not None else DEFAUT_DURATION.get('mute')
        duration = 'Permanent' if 'permanent' == duration.lower() else duration

        for msg_id, mute_obj in mute_list.items():
            if user == mute_obj.user and 'Livestream' == mute_obj.type_:
                await mute_obj.interrupt()

                mute_obj.reason = reason
                mute_obj.duration = func.time_process(duration)

                if not silent:
                    embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url,
                                          reason, duration, 'Livestream')
                    await ctx.channel.send(embed=embed)
                await mute_obj.count_down()
                return

        msg_id = func.generate_id()

        mute_list[msg_id] = mod.LSMute(self.bot, ctx.author, user, duration, reason, msg_id,
                                       True if duration == 'Permanent' else False)
        await user.add_roles(lsmute_role)

        if not silent:
            embed = func.embedder('Mute', msg_id, f'<@{ctx.author.id}>', user, user.avatar_url, reason, duration,
                                  'Livestream')
            await ctx.channel.send(embed=embed)

        logger.info(f'User {ctx.author} mute a user, info\n{json.dumps(mute_list[msg_id].info(), indent=4)}')
        await mute_list[msg_id].count_down()

    @commands.command(brief=desc.SILENTUNLSMUTE_BRIEF, description=desc.SILENTUNLSMUTE, hidden=True)
    @decorators.in_channels(has_user=True)
    @decorators.target_check(type_='mute')
    async def silentunlsmute(self, ctx, target: Union[discord.Member, str], silent: Optional[bool] = False) -> None:
        mute_obj = mute_list.get(target)
        mute_role = func.get_role(ctx, role='Livestream Mute')

        await mute_obj.interrupt()
        await mute_obj.user.remove_roles(mute_role)
        
        if not silent:
            await ctx.channel.send(ADMIN_PREFIX['unmute'].format(mute_obj.user, mute_obj.type_, 'silent'))

        logger.info(f'User {ctx.author} unlsmute a user, info\nuser: {mute_obj.user}\nreason: silent')
        del mute_list[target]

    @commands.command(brief=desc.MUTEINFO_BRIEF, description=desc.MUTEINFO)
    @decorators.in_channels(has_user=False, has_target=False)
    async def muteinfo(self, ctx) -> None:
        embed = discord.Embed(title='Mute List', color=func.color_picker())

        for index, items in enumerate(mute_list.items()):
            msg_id, mute_obj = items
            data = f'```User: {mute_obj.user}\n' \
                   f'Type: {mute_obj.type_}\n' \
                   f'Durasi: {func.time_convert(mute_obj.duration)}\n' \
                   f'Reason: {mute_obj.reason}```'
            embed.add_field(name=f'{index + 1}. {msg_id}', value=data, inline=False)
        if not mute_list:
            embed.description = 'Kosong bang'

        embed.set_footer(
            text=f'Total mute: {len(mute_list)} • Hari ini pada {func.get_time(no_date=True, thformat=True)}'
        )
        logger.info(f'User {ctx.author} use {ctx.invoked_with}')
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Mutes(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
