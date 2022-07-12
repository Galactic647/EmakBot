from EmakBot.globals import PATTERN, CHANNEL_IDS, ALLOW_DM, RESTRICT

import discord

from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import random
import string


def generate_id() -> str:
    return ''.join(random.choices(string.digits, k=18))


def color_picker() -> int:
    return int(''.join(random.choices(string.hexdigits, k=6)), 16)


def time_process(time_: str) -> Union[None, int]:
    total_time = 0.5  # Only accept int, 0.x is just for checking
    groups = {'hari': 86400, 'jam': 3600, 'menit': 60, 'detik': 1}
    match = PATTERN.match(time_.lower())

    if time_.lower() == 'permanent':
        return -1

    for k, v in groups.items():
        try:
            total_time += int(match.group(k)) * v
        except TypeError:
            pass
        except AttributeError:
            pass

    if total_time == 0.5:
        raise ValueError('Invalid duration')
    return int(total_time)


def get_time(no_date: Optional[bool] = False, date_only: Optional[bool] = False,
             thformat: Optional[bool] = False, as_dict: Optional[bool] = False) -> Union[dict, str]:
    now = datetime.now()
    wib = timezone(timedelta(hours=7))
    wib = now.astimezone(wib)

    formatted = {
        'years': 0,
        'months': 0,
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0
    }

    if as_dict:
        for time_, scale in zip(wib.timetuple()[:6], formatted):
            formatted[scale] += time_
        return formatted

    if date_only:
        return wib.strftime('%d/%m/%Y')
    if no_date:
        if thformat:
            return wib.strftime('%I.%M.%S %p WIB')
        return wib.strftime('%H.%M.%S WIB')
    if thformat:
        return wib.strftime('%d/%m/%Y - %I.%M.%S %p WIB')
    return wib.strftime('%d/%m/%Y %H.%M.%S WIB')


def elapsed_time(start: dict, end: dict) -> str:
    # TODO implement a more accurate calculation for longer time range
    time_scale = {
        '0': 'tahun',
        '1': 'bulan',
        '2': 'hari',
        '3': 'jam',
        '4': 'menit',
        '5': 'detik'
    }
    elapsed = dict()

    for index, value in enumerate(zip(start.values(), end.values())):
        s, e = value
        scale = time_scale.get(str(index))

        if scale == 'tahun':
            elapsed['hari'] = (e - s) * 365
        elif scale == 'bulan':
            elapsed['hari'] += (e - s) * 30
        elif diff := (e - s) < 0:
            elapsed[time_scale.get(str(index - 1))] -= 1
            elapsed[scale] = 60 + diff
        else:
            elapsed[scale] = e - s

    return ' '.join([f'{v} {k}' for k, v in elapsed.items()])


def convert_size(size, size_type, place=2):
    size_types = {'0': '',
                  '1': 'K',
                  '2': 'M',
                  '3': 'G',
                  '4': 'T'}
    while size >= 1024:
        if size_type >= 4:
            break
        size_type += 1
        size /= 1024
    return f'{round(size, place)}{size_types[str(size_type)]}B'


def time_convert(duration: int) -> str:
    formatted = []
    scale = {
        '0': 'detik',
        '1': 'menit',
        '2': 'jam',
        '3': 'hari'
    }
    magnitude = {
        '0': 60,
        '1': 60,
        '2': 24,
        '3': duration  # So that it stay in remainder
    }

    if duration == -1:
        return '-1 hari'

    for index in range(4):
        duration, remainder = divmod(duration, magnitude[str(index)])
        formatted.append(f'{remainder} {scale[str(index)]}')
    return ' '.join(formatted[::-1])


def embedder(type_: str, msg_id: str, moderator, user, avatar, reason: str, duration: str, level: Union[str, int]):
    embed = discord.Embed(title=type_, color=color_picker())
    embed.set_author(name=user, icon_url=avatar)
    embed.add_field(name='Moderator', value=moderator, inline=True)

    if type_.lower() == 'warning':
        embed.add_field(name='Warning Level', value=str(level), inline=True)
    elif type_.lower() == 'mute':
        embed.add_field(name='Mute Type', value=str(level).capitalize(), inline=True)
    elif type_.lower() == 'kick':
        embed.add_field(name='', value='')
    elif type_.lower() == 'ban':
        embed.add_field(name='', value='')
    elif type_.lower() == 'unban':
        embed.add_field(name='', value='')

    embed.add_field(name='Reason', value=reason, inline=True)
    if type_.lower() not in ('kick', 'ban'):
        embed.add_field(name='Duration', value=duration, inline=False)

    embed.set_footer(text=f'{msg_id} • {get_time(date_only=True)}')
    return embed


async def process_message(self, ctx, msg, user, user_msg) -> None:
    warn_channel = await self.bot.fetch_channel(CHANNEL_IDS[1])

    if isinstance(msg, discord.Embed):
        await ctx.channel.send(embed=msg)
        if not RESTRICT:
            await warn_channel.send(embed=msg)
    else:
        if not RESTRICT:
            await warn_channel.send(msg)
        await ctx.channel.send(msg)

    if ALLOW_DM:
        await user.send(user_msg)


def get_role(ctx, role: str) -> discord.Role:
    return discord.utils.get(ctx.author.guild.roles, name=role)
