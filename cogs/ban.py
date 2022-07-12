from core import decorators, descriptions as desc
from core.logger import logger

from discord.ext import commands
import discord


class Ban(commands.Cog):  # TODO implement ban feature
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.BAN_BRIEF, description=desc.BAN)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def ban(self, ctx, user: discord.Member, reason: str) -> None:
        pass

    @commands.command(brief=desc.UNBAN_BRIEF, description=desc.UNBAN)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def unban(self, ctx, user: discord.Member, reason: str) -> None:
        pass


def setup(bot):
    bot.add_cog(Ban(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
