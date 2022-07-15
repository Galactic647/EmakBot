from globals import GUILD_ID, MAX_BACKUP_FOLDERS, mute_list, warn_list
from core import functions as func, moderation as mod, descriptions as desc, decorators
from core.logger import logger
import globals

from discord.ext import commands
import discord

from datetime import datetime, timedelta, timezone
from typing import Optional
import asyncio
import shutil
import json
import os


class Utils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def regular_backup(self, interval: int):
        try:
            while True:
                if self._backup(type_='auto'):
                    logger.info('Data backed up! [auto]')
                await asyncio.sleep(interval)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def _backup(type_: Optional[str] = 'auto') -> str:
        data = dict()
        if not mute_list and not warn_list:
            return str()

        for folder in ('backup', 'backup/auto', 'backup/manual'):
            if not os.path.exists(folder):
                os.mkdir(folder)
        for backups in ('backup/auto', 'backup/manual'):
            folders = os.listdir(backups)
            if len(folders) > MAX_BACKUP_FOLDERS:
                for folder in folders[:-1 * MAX_BACKUP_FOLDERS]:
                    shutil.rmtree(folder)

        now = datetime.now()
        wib = now.astimezone(timezone(timedelta(hours=7)))
        folder = f'backup/{type_}/{wib.strftime("%Y-%m-%d")}'

        if not os.path.exists(folder):
            os.mkdir(folder)

        backup_file = f'{folder}/backup@{wib.strftime("%H-%M-%S")}.bak'

        for n, l in zip(('warn_list', 'mute_list'), (warn_list, mute_list)):
            data[n] = dict((k, v.info()) for k, v in l.items())
        with open(backup_file, 'w') as file:
            json.dump(data, file, indent=4)
            file.close()
        return backup_file

    async def _get_member(self, member_id: int) -> discord.Member:
        guild = await self.bot.fetch_guild(GUILD_ID)
        return await guild.fetch_member(member_id)

    @commands.command(brief=desc.BACKUP_BRIEF, description=desc.BACKUP)
    @decorators.in_channels(has_target=False)
    async def backup(self, ctx) -> None:
        file = self._backup('manual')
        attachment = discord.File(file)
        await ctx.channel.send(file=attachment, content=':ok_hand: Backed up!, filenya bisa dicek dibawah')

    @commands.command(brief=desc.LISTBACKUP_BRIEF, description=desc.LISTBACKUP)
    @decorators.in_channels(has_target=False)
    async def listbackup(self, ctx) -> None:
        total_backup = 0
        embed = discord.Embed(title='Backups', color=func.color_picker())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        for backups in os.listdir('backup'):
            value = []
            for backup in os.listdir(f'backup/{backups}'):
                n_backup = len(os.listdir(f'backup/{backups}/{backup}'))
                total_backup += n_backup
                value.append(f'{backup} : {n_backup}\n')
            embed.add_field(name=backups.capitalize(), value=f'```{"".join(value)}```', inline=False)
        embed.set_footer(text=f'Total backup: {total_backup}')

        await ctx.channel.send(embed=embed)

    @commands.command(brief=desc.BACKUPDETAIL_BRIEF, description=desc.BACKUPDETAIL)
    @decorators.in_channels(has_target=False)
    async def backupdetail(self, ctx, type_: str, date: Optional[str] = None, file: Optional[str] = None) -> None:
        attachment = None
        embed = discord.Embed(title='Backups', color=func.color_picker())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        if type_.lower() not in ('auto', 'manual'):
            await ctx.channel.send(f'Tipe {type_} tidak ditemukan')
            return
        elif date is None and file:
            await ctx.channel.send('Tanggal tidak diketahui')
            return
        elif date and not os.path.exists(f'backup/{type_}/{date}'):
            await ctx.channel.send(f'Tipe {type_} tidak memliki folder {date}')
            return
        elif date and file and not os.path.exists(f'backup/{type_.lower()}/{date}/{file}'):
            await ctx.channel.send(f'File backup {file} tidak ditemukan')
            return

        if date is None and file is None:
            for folder in os.listdir(f'backup/{type_.lower()}'):
                value = []
                for file in os.listdir(f'backup/{type_.lower()}/{folder}'):
                    file_size = func.convert_size(os.path.getsize(f'backup/{type_.lower()}/{folder}/{file}'), 0)
                    value.append(f'{file} : {file_size}\n')
                embed.add_field(name=folder, value=f'```{"".join(value)}```', inline=False)
        elif date and file is None:
            value = []
            for file in os.listdir(f'backup/{type_.lower()}/{date}'):
                file_size = func.convert_size(os.path.getsize(f'backup/{type_.lower()}/{date}/{file}'), 0)
                value.append(f'{file} : {file_size}\n')
            embed.description = f'```{"".join(value)}```'
        else:
            embed.description = ':ok_hand: Fetched!'
            attachment = discord.File(f'backup/{type_.lower()}/{date}/{file}')

        embed.set_footer(text=f'Hari ini pada {func.get_time(no_date=True, thformat=True)}')
        if attachment is None:
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed, file=attachment)

    @commands.command(brief=desc.RELOAD_BRIEF, description=desc.RELOAD)
    @decorators.in_channels(has_target=False)
    async def reload(self, ctx, type_: str, date: str, file: str) -> None:
        mute_role = discord.utils.get(ctx.author.guild.roles, name='mod.Mute')
        lsmute_role = discord.utils.get(ctx.author.guild.roles, name='Livestream mod.Mute')

        if not os.path.exists(f'backup/{type_.lower()}/{date}/{file}'):
            await ctx.channel.send('File backup tidak ditemukan')
            return

        with open(f'backup/{type_.lower()}/{date}/{file}', 'r') as bak_file:
            data = json.load(bak_file)
            bak_file.close()

        for type_, items in data.items():
            for id_, value in items.items():
                time_start = None
                edit = value
                edit['moderator'] = await self._get_member(edit.get('moderator_id'))
                edit['user'] = await self._get_member(edit.get('user_id'))

                if edit.get('duration_str').lower() != 'permanent':
                    time_start = edit.get('duration_str')
                    elapsed = func.elapsed_time(edit.get('created_at_as_dict'), func.get_time(as_dict=True))
                    elapsed = func.time_convert(func.time_process(time_start) - func.time_process(elapsed))

                    if func.time_process(elapsed) < 0:
                        elapsed = '1 detik'
                else:
                    elapsed = 'Permanent'

                if type_.lower() == 'warn_list':
                    warn_obj = mod.Warn(
                        self.bot,
                        edit.get('moderator'),
                        edit.get('user'),
                        elapsed,
                        edit.get('reason'),
                        id_,
                        edit.get('level')
                    )
                    warn_obj.duration_str = time_start
                    warn_obj.created_at = edit.get('created_at')
                    warn_obj.created_at_as_dict = edit.get('created_as_dict')

                    warn_list[id_] = warn_obj
                    asyncio.ensure_future(warn_list[id_].count_down())

                elif type_.lower() == 'mute_list':
                    mute_obj = None
                    user = edit.get('user')
                    if edit.get('type_').lower() == 'server':
                        mute_obj = mod.Mute(
                            self.bot,
                            edit.get('moderator'),
                            user,
                            elapsed,
                            edit.get('reason'),
                            id_
                        )
                        await user.add_roles(mute_role)

                    elif edit.get('type_').lower() == 'livestream':
                        mute_obj = mod.LSMute(
                            self.bot,
                            edit.get('moderator'),
                            user,
                            elapsed,
                            edit.get('reason'),
                            id_,
                            edit.get('permanent')
                        )
                        await user.add_roles(lsmute_role)

                    mute_obj.duration_str = time_start
                    mute_obj.created_at = edit.get('created_at')
                    mute_obj.created_at_as_dict = edit.get('created_as_dict')

                    mute_list[id_] = mute_obj
                    asyncio.ensure_future(mute_list[id_].count_down())
        await ctx.channel.send(':ok_hand: Reloaded!')

    @commands.command(brief=desc.LOADEXT_BRIEF, description=desc.LOADEXT)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def loadext(self, ctx, extension: str) -> None:
        if not os.path.exists(f'cogs/{extension.lower()}.py'):
            await ctx.channel.send(f':warning: Tidak ada extensi dengan nama {extension.lower()}')
            return
        self.bot.load_extension(f'cogs.{extension.lower()}')
        await ctx.channel.send(f':ok_hand: Extension `{extension.lower()}` loaded!')

    @commands.command(brief=desc.UNLOADEXT_BRIEF, description=desc.UNLOADEXT)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def unloadext(self, ctx, extension: str) -> None:
        if not os.path.exists(f'cogs/{extension.lower()}.py'):
            await ctx.channel.send(f':warning: Tidak ada extensi dengan nama {extension.lower()}')
            return
        self.bot.unload_extension(f'cogs.{extension.lower()}')
        await ctx.channel.send(f':ok_hand: Extension `{extension.lower()}` unloaded!')

    @commands.command(brief=desc.RELOADEXT_BRIEF, description=desc.RELOADEXT)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def reloadext(self, ctx, extension: str) -> None:
        if not os.path.exists(f'cogs/{extension.lower()}.py'):
            await ctx.channel.send(f':warning: Tidak ada extensi dengan nama {extension.lower()}')
            return
        self.bot.reload_extension(f'cogs.{extension.lower()}')
        await ctx.channel.send(f':ok_hand: Extension `{extension.lower()}` reloaded!')

    @commands.command(brief=desc.RELOADALLEXT_BRIEF, description=desc.RELOADALLEXT)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def reloadallext(self, ctx) -> None:
        for extension in os.listdir('cogs'):
            if not extension.startswith('_') and extension.endswith('.py'):
                self.bot.reload_extension(f'cogs.{extension.lower()[:-3]}')
        await ctx.channel.send(f':ok_hand: All extension reloaded!')

    @commands.command(brief=desc.CHANGEFLAG_BRIEF, description=desc.CHANGEFLAG)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def changeflag(self, ctx, flag: str, value: bool) -> None:
        if flag.upper() not in ('RESTRICT', 'ALLOW_DM', 'DEVELOPMENT'):
            await ctx.channel.send(f'Flag {flag.upper()} tidak ditemukan')
            return
        elif not isinstance(value, bool):
            await ctx.channel.send(f':warning: Illegal value')
            return

        if flag.upper() == 'RESTRICT':
            globals.RESTRICT = value
        elif flag.upper() == 'ALLOW_DM':
            globals.ALLOW_DM = value
        elif flag.upper() == 'DEVELOPMENT':
            globals.DEVELOPMENT = value
        await ctx.channel.send(f'Flag `{flag.upper()}` diubah ke `{value}`')

    @commands.command(brief=desc.CHECKFLAG_BRIEF, description=desc.CHECKFLAG)
    @decorators.in_channels(has_target=False)
    async def checkflag(self, ctx, flag: str) -> None:
        if flag.upper() not in ('RESTRICT', 'ALLOW_DM', 'DEVELOPMENT'):
            await ctx.channel.send(f'Flag {flag.upper()} tidak ditemukan')
            return
        await ctx.channel.send(f'Flag `{flag.upper()} = {getattr(globals, flag.upper())}`')

    @commands.command(brief=desc.PING_BRIEF, description=desc.PING)
    @decorators.in_channels(has_target=False)
    async def ping(self, ctx):
        await ctx.channel.send(f'Ping : {round(self.bot.latency * 1000, 2)}ms')

    @commands.command(brief=desc.SHUTDOWN_BRIEF, description=desc.SHUTDOWN)
    @commands.is_owner()
    @decorators.in_channels(has_target=False)
    async def shutdown(self, ctx) -> None:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        try:
            await ctx.channel.send('Apakah anda yakin ingin menghentikan bot? [Y/N]')
            reply = await self.bot.wait_for('message', check=check, timeout=15)
            if reply.content.lower() == 'y':
                self._backup(type_='auto')
                await ctx.channel.send('See you later!')
                await self.bot.logout()
        except asyncio.TimeoutError:
            await ctx.channel.send('Command di cancel')


def setup(bot):
    bot.add_cog(Utils(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
