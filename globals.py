from dotenv import load_dotenv

from collections import namedtuple
import re
import os

load_dotenv()

USER_PREFIX = {
    'warn': '**Sebud Gang:** Anda telah di :warning: warn\n'
            '**Level:** {0}\n'
            '**Durasi:** {1}\n'
            '**Reason:** {2}',
    'lower_warn': '**Sebud Gang:** :warning: Warn anda telah diturunkan ke level {0}\n'
                  '**Durasi:** {1}\n'
                  '**Reason:** {2}',
    'remove_warn': '**Sebud Gang:** :warning: Warn anda telah dicabut\n'
                   '**Reason:** {0}',
    'mute': '**Sebud Gang:** Anda telah di :mute: mute\n'
            '**Type:** {0}\n'
            '**Durasi:** {1}\n'
            '**Reason:** {2}',
    'unmute': '**Sebud Gang:** Anda telah di :speaker: unmute\n'
              '**Type:** {0}\n'
              '**Reason:** {1}',
    'kick': '**Sebud Gang:** Anda telah di :warning: kick\n'
            '**Reason** {0}'
}
ADMIN_PREFIX = {
    'lower_warn': '**Info:** :warning: Warn user `{0}` telah diturunkan\n'
                  '**Level:** {1}'
                  '\n**Durasi:** {2}\n**Reason:** {3}',
    'remove_warn': '**Info:** :warning: Warn user `{0}` telah dicabut\n'
                   '**Reason:** {1}',
    'unmute': '**Info:** :mute: User `{0}` telah diunmute\n'
              '**Type:** {1}\n'
              '**Reason:** {2}',
    'kick': '**Info:** :warning: User {0} telah di kick\n'
            '**Reason:** {1}'
}
ERROR_MESSAGE = ':warning: Ada sesuatu yang salah!\nError Log\n```{0}```'

DEFAUT_DURATION = {
    'warn-1': '10 hari',
    'warn-2': '25 hari',
    'mute': '7 hari'
}
VISIBLE_COGS = ('warnings', 'mutes', 'kick', 'ban', 'utils')

PATTERN = re.compile(r'''
    ((?P<hari>-?\d+)\shari)?\s?
    ((?P<jam>-?\d+)\sjam)?\s?
    ((?P<menit>-?\d+)\smenit)?\s?
    ((?P<detik>-?\d+)\sdetik)?
    ''', re.VERBOSE | re.IGNORECASE)

CHANNELS = namedtuple('CHANNEL_IDS', 'bot_development, warnings, moderation')
CHANNEL_IDS = CHANNELS(int(os.getenv('BOT_DEV_CH_ID')), int(os.getenv('WARN_CH_ID')), int(os.getenv('MOD_CH_ID')))
GUILD_ID = int(os.getenv('GUILD_ID'))
OWNER_ID = int(os.getenv('AUTHOR_ID'))

RESTRICT = True  # Only send to #warnings if False
ALLOW_DM = True  # Only send dm if true
DEVELOPMENT = True  # True if still in development

BACKUP_INTERVAL = 3600  # 1 Hour
MAX_BACKUP_FOLDERS = 7  # A week

warn_list = {}
mute_list = {}
