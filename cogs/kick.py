from globals import ERROR_MESSAGE, DEVELOPMENT
from core import decorators, descriptions as desc, functions as func
from core.logger import logger

from discord.ext import commands
import discord

import asyncio


class Kick(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.KICK_BRIEF, description=desc.KICK)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def kick(self, ctx, user: discord.Member, reason: str) -> None:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        try:
            await ctx.channel.send(f'Apakah anda yakin ingin mengkick user {user}? [Y/N]')
            reply = await self.bot.wait_for('message', check=check, timeout=15)
            if reply.content.lower() == 'y':
                msg_id = func.generate_id()
                embed = func.embedder('Kick', msg_id, ctx.author.mention, user, user.avatar_url, reason, str(), str())

                await ctx.channel.send(embed=embed)
                if not DEVELOPMENT:
                    await self.bot.kick(user, reason=reason)
                    logger.info(f'User {ctx.author} just kick a user\n'
                                f'User: {user}\n'
                                f'Reason: {reason}')
        except asyncio.TimeoutError:
            await ctx.channel.send('Command di cancel')
        except Exception as e:
            await ctx.channel.send(ERROR_MESSAGE.format(e))
            logger.error(e)


def setup(bot):
    bot.add_cog(Kick(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
