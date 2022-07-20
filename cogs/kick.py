from core import decorators, descriptions as desc, functions as func
from core.logger import logger
import config

from discord.ext import commands
import discord

from typing import Union
import asyncio


class Kick(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.KICK_BRIEF, description=desc.KICK)
    @decorators.in_channels(has_target=True)
    @decorators.self_check
    async def kick(self, ctx, target: Union[discord.Member, str], reason: str) -> dict:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        try:
            await ctx.channel.send(f'Apakah anda yakin ingin mengkick user {target}? [Y/N]')
            reply = await self.bot.wait_for('message', check=check, timeout=15)
            if reply.content.lower() == 'y':
                msg_id = func.generate_id()
                embed = func.embedder('Kick', msg_id, ctx.author.mention, target, target.avatar_url,
                                      reason, str(), str())

                await ctx.channel.send(embed=embed)
                if not config.DEVELOPMENT:
                    await self.bot.kick(target, reason=reason)
                    return {
                        'user': target,
                        'reason': reason
                    }
        except asyncio.TimeoutError:
            await ctx.channel.send('Command di cancel')


def setup(bot):
    bot.add_cog(Kick(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
