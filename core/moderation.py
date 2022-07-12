from EmakBot.globals import ADMIN_PREFIX, USER_PREFIX, CHANNEL_IDS, RESTRICT, warn_list, mute_list
from EmakBot.core import functions as func

import discord

from typing import Optional
import asyncio


class Moderation(object):
    __slots__ = (
        'bot',
        'moderator',
        'moderator_id',
        'user',
        'user_id',
        'duration',
        'duration_str',
        'reason',
        'id_',
        'stop',
        'created_at',
        'created_at_as_dict'
    )

    def __init__(self, bot, moderator: discord.Member, user: discord.Member,
                 duration: str, reason: str, id_: str) -> None:
        self.bot = bot
        self.moderator = moderator
        self.moderator_id = moderator.id
        self.user = user
        self.user_id = user.id
        self.duration = func.time_process(duration)
        self.duration_str = duration
        self.reason = reason
        self.id_ = id_
        self.stop = False
        self.created_at = func.get_time()
        self.created_at_as_dict = func.get_time(as_dict=True)

    async def interrupt(self) -> None:
        self.stop = True

    def info(self) -> dict:
        data = []
        for var in dir(self):
            if not var.startswith('__') and isinstance(x := getattr(self, var), (int, str, dict, discord.Member)):
                if isinstance(x, discord.Member):
                    x = str(x)
                data.append((var, x))
        return dict(data)


class Warn(Moderation):
    __slots__ = 'level'

    def __init__(self, bot, moderator: discord.Member, user: discord.Member,
                 duration: str, reason: str, id_: str, level: int) -> None:
        super(Warn, self).__init__(bot, moderator, user, duration, reason, id_)
        self.level = level

    async def count_down(self) -> None:
        while self.duration and not self.stop:
            self.duration -= 1
            await asyncio.sleep(1)

        if not self.stop:
            dm = await self.user.create_dm()
            channel = self.bot.get_channel(id=CHANNEL_IDS[0])

            msg = ADMIN_PREFIX['remove_warn'].format(self.user, 'Durasi habis')
            await channel.send(msg)
            await dm.send(USER_PREFIX['remove_warn'].format('Durasi habis'))

            if not RESTRICT:
                warn_channel = self.bot.get_channel(id=CHANNEL_IDS[1])
                await warn_channel.send(msg)
            del warn_list[self.id_]
        else:
            self.stop = False


class Mute(Moderation):
    __slots__ = 'type_'

    def __init__(self, bot, moderator: discord.Member, user: discord.Member,
                 duration: str, reason: str, id_: str) -> None:
        super(Mute, self).__init__(bot, moderator, user, duration, reason, id_)
        self.type_ = 'Server'

    async def count_down(self) -> None:
        while self.duration and not self.stop:
            self.duration -= 1
            await asyncio.sleep(1)

        if not self.stop:
            dm = await self.user.create_dm()
            channel = self.bot.get_channel(id=CHANNEL_IDS[0])
            mute_role = discord.utils.get(self.user.guild.roles, name='Mute')

            msg = ADMIN_PREFIX['unmute'].format(self.user, self.type_, 'Durasi habis')
            await channel.send(msg)
            await dm.send(USER_PREFIX['unmute'].format(self.type_, 'Durasi habis'))

            if not RESTRICT:
                mute_channel = self.bot.get_channel(id=CHANNEL_IDS[1])
                await mute_channel.send(msg)
            await self.user.remove_roles(mute_role)
            del mute_list[self.id_]
        else:
            self.stop = False


class LSMute(Moderation):
    __slots__ = (
        'type_',
        'permanent'
    )

    def __init__(self, bot, moderator, user, duration: str, reason: str,
                 id_: str, permanent: Optional[bool] = False) -> None:
        super(LSMute, self).__init__(bot, moderator, user, duration, reason, id_)
        self.type_ = 'Livestream'
        self.permanent = permanent

    async def count_down(self) -> None:
        while (self.duration > 0) and not self.stop and not self.permanent:
            self.duration -= 1
            await asyncio.sleep(1)

        if not self.duration and not self.stop and not self.permanent:
            dm = await self.user.create_dm()
            channel = self.bot.get_channel(id=CHANNEL_IDS[0])
            mute_role = discord.utils.get(self.user.guild.roles, name='Livestream Mute')

            msg = ADMIN_PREFIX['unmute'].format(self.user, self.type_, 'Durasi habis')
            await channel.send(msg)
            await dm.send(USER_PREFIX['unmute'].format(self.type_, 'Durasi habis'))

            if not RESTRICT:
                mute_channel = self.bot.get_channel(id=CHANNEL_IDS[1])
                await mute_channel.send(msg)
            await self.user.remove_roles(mute_role)
            del mute_list[self.id_]
        else:
            self.stop = False
