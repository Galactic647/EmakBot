from EmakBot.core import decorators, descriptions as desc
from EmakBot.core.logger import logger

from discord.ext import commands
import discord


class Kick(commands.Cog):  # TODO implement kick feature
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief=desc.KICK_BRIEF, description=desc.KICK)
    @decorators.in_channels(has_user=True)
    @decorators.self_check
    async def kick(self, ctx, user: discord.Member, reason: str) -> None:
        pass


def setup(bot):
    bot.add_cog(Kick(bot))
    logger.info(f'Extension {__name__} loaded')


def teardown(bot):
    bot.remove_cog(__name__)
    logger.info(f'Extension {__name__} unloaded')
