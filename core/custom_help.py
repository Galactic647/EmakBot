from core.functions import color_picker
from globals import VISIBLE_COGS
from discord.ext import commands
import discord


class CustomHelp(commands.HelpCommand):
    def __init__(self, parent=None) -> None:
        super(CustomHelp, self).__init__(parent=parent)

    async def send_bot_help(self, mapping) -> None:
        caller = f'{self.clean_prefix}{self.invoked_with}'
        embed = discord.Embed(title='Commands', color=color_picker())
        embed.set_author(name=self.context.author, icon_url=self.context.author.avatar_url)
        embed.description = f'Untuk melihat detail setiap command bisa menggunakan ' \
                            f'`{caller} [group]` atau `{caller} [command]`'

        for cog, cmds in mapping.items():
            if cog is None or cog.qualified_name.lower() not in VISIBLE_COGS:
                continue

            cmds = await self.filter_commands(cmds, sort=True)
            embed.add_field(name=f'{cog.qualified_name} Commands',
                            value=' '.join([f'`{cmd.name}`' for cmd in cmds if not cmd.hidden]),
                            inline=False)

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, cmd) -> None:
        if 'bot owner only' in cmd.brief.lower():
            name = f'{cmd.qualified_name} [Bot Owner Only]'
        else:
            name = cmd.qualified_name
        embed = discord.Embed(title=f'Command info: {name}', color=color_picker())
        embed.set_author(name=self.context.author, icon_url=self.context.author.avatar_url)

        embed.description = f'>>> {cmd.description}'

        embed.add_field(name='Command', value=f'`{cmd.qualified_name}`', inline=True)
        embed.add_field(name='Group', value=f'`{cmd.cog_name}`', inline=True)
        embed.add_field(name='Usage', value=f'`{self.clean_prefix}{cmd.name} {cmd.signature}`', inline=False)

        embed.set_footer(text='[opsional], <wajib diisi>\n'
                              'Gunakan double quotes ("") untuk <reason> dan [duration]')
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog) -> None:
        caller = f'{self.clean_prefix}{self.invoked_with}'
        embed = discord.Embed(title=f'Group info: {cog.qualified_name}', color=color_picker())
        embed.set_author(name=self.context.author, icon_url=self.context.author.avatar_url)
        embed.description = f'Untuk melihat detail setiap command bisa menggunakan ' \
                            f'`{caller} [command]`'

        cmds = await self.filter_commands(cog.get_commands(), sort=True)

        for cmd in cmds:
            if cmd.hidden:
                continue
            embed.add_field(name=cmd.name, value=f'> {cmd.brief}', inline=False)

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error) -> None:
        error = error.split('"')[-2]
        await self.get_destination().send(f':warning: Tidak ada command dengan nama `{error}`')
