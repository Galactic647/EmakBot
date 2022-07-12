from EmakBot.globals import DEFAUT_DURATION

# Ban
BAN_BRIEF = 'Command untuk memban user dari server'
BAN = BAN_BRIEF
UNBAN_BRIEF = 'Command untuk mengunban user dari server'
UNBAN = UNBAN_BRIEF

# Kick
KICK_BRIEF = 'Command untuk menkick user dari server'
KICK = KICK_BRIEF

# Mutes
MUTE_BRIEF = 'Command untuk memberikan mute kepada user'
MUTE = '''
Mute ini adalah tipe mute server dimana user yang dimute tidak akan bisa
mengakes seluruh channel di server

Mute ini sendiri memiliki durasi default yaitu: `{DEFAUT_DURATION.get("mute")}`
Jika parameter `[duration]` tidak diberikan maka akan diambil durasi default

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
UNMUTE_BRIEF = 'Command untuk mencabut mute user'
UNMUTE = '''
Mute dari user dapat dicabut menggunakan mute id atau username mereka

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
LSMUTE_BRIEF = 'Command untuk memberikan livestream mute kepada user'
LSMUTE = '''
Mute ini adalah tipe mute livestream dimana user yang dimute tidak akan bisa
mengakses channel livestream

Mute sendiri memiliki durasi default yaitu: `{DEFAUT_DURATION.get("mute")}`
Jika parameter `[duration]` tidak diberikan maka akan diambil durasi default

Untuk tipe mute ini ada pilihan durasi `Permanent` dimana mute ini tidak akan
pernah dicabut kecuali menggunakan `?unlsmute`
Durasi `Permanent` akan diperlihatkan sebagai `-1 Hari` ketika menggunakan
`?mutes`

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
UNLSMUTE_BRIEF = 'Command untuk mencabut livestream mute kepada user'
UNLSMUTE = '''
Mute dari user dapat dicabut menggunakan mute id atau username mereka

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
SILENTMUTE_BRIEF = ''
SILENTMUTE = ''
SILENTUNMUTE_BRIEF = ''
SILENTUNMUTE = ''
SILENTLSMUTE_BRIEF = ''
SILENTLSMUTE = ''
SILENTUNLSMUTE_BRIEF = ''
SILENTUNLSMUTE = ''
MUTEINFO_BRIEF = 'Command untuk menampilkan seluruh mute yang sedang aktif'
MUTEINFO = f'''
{MUTEINFO_BRIEF}
Command ini akan mengirim pesan hanya pada 1 channel:
- Channel command ini dipanggil
'''

# Warnings
WARN_BRIEF = 'Command untuk memberikan warn kepada user'
WARN = f'''
Level maksimal untuk warn adalah level 2

Warn sendiri memiliki durasi default untuk setiap levelnya
Warn 1 : `{DEFAUT_DURATION.get("warn-1")}`
Warn 2 : `{DEFAUT_DURATION.get("warn-2")}`
Jika parameter `[duration]` tidak diberikan maka akan diambil durasi default

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
REMOVEWARN_BRIEF = 'Command untuk mencabut warn dari user'
REMOVEWARN = '''
Warn dari user dapat dicabut menggunakan warn id atau username mereka

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
LOWERWARN_BRIEF = 'Command untuk menurunkan level warn user'
LOWERWARN = '''
Warn dari user dapat diturunkan menggunakan warn id atau username mereka

Command ini akan mengirim pesan pada 3 channel:
- Channel command ini dipanggil
- Channel `#warnings`
- DM User
'''
SILENTWARN_BRIEF = 'Command untuk memberikan warn kepada user **[Not Safe]**'
SILENTWARN = '''
Command ini seharusnya tidak pernah digunakan kecuali ada masalah ketika
bot mencoba untuk menrecovery data moderasi

Command ini akan mengirim pesan hanya pada 1 channel:
- Channel command ini dipanggil
'''
SILENTREMOVEWARN_BRIEF = 'Command untuk mencabut warn dari user **[Not Safe]**'
SILENTREMOVEWARN = '''
Command ini seharusnya tidak pernah digunakan kecuali ada masalah ketika
bot mencoba untuk menrecovery data moderasi

Command ini akan mengirim pesan hanya pada 1 channel:
- Channel command ini dipanggil
'''
WARNINFO_BRIEF = 'Command untuk menampilkan seluruh warning yang sedang aktif'
WARNINFO = f'''
{WARNINFO_BRIEF}
Command ini akan mengirim pesan hanya pada 1 channel:
- Channel command ini dipanggil
'''
ASCENDMUTE_BRIEF = ''
ASCENDMUTE = ''
ASCENDKICK_BRIEF = ''
ASCENDKICK = ''
ASCENDBAN_BRIEF = ''
ASCENDBAN = ''

# Utils
BACKUP_BRIEF = 'Command untuk membackup data moderasi'
BACKUP = '''
Data yang dibackup akan disimpan pada server dan juga dikirim
ke channel command ini dipanggil
        
Data yang dibackup sendiri memiliki limit maksimal yaitu 7 hari,
data yang backup yang sudah melebihi limit ini akan dihapus secara otomatis
'''
LISTBACKUP_BRIEF = 'Command untuk memberikan list folder backup'
LISTBACKUP = 'Folder backup akan diperlihatkan berdasarkan tipe dan tanggalnya'
BACKUPDETAIL_BRIEF = 'Command untuk melihat informasi dari backup'
BACKUPDETAIL = '''
Detail dari backup dapat dilihat berdasarkan tipe, tanggal atau
file backup itu sendiri
'''
RELOAD_BRIEF = 'Command untuk mereload data moderasi'
RELOAD = '''
Data yang direload akan dikembalikan seperti semula
dimana durasi dari setiap item moderasi akan di kurangi
berdasarkan waktu yang telah berlalu hingga command ini
dipanggil
'''
LOADEXT_BRIEF = 'Command untuk mengload extensi bot **[Bot Owner Only]**'
LOADEXT = '''
Command ini digunakan ketika ingin mengload suatu extensi yang
ingin ditambahkan ke botnya
'''
UNLOADEXT_BRIEF = 'Command untuk mengunload extensi bot **[Bot Owner Only]**'
UNLOADEXT = '''
Command ini digunakan ketika ingin mengunload suatu extensi yang
ingin dihapus dari botnya
'''
RELOADEXT_BRIEF = 'Command untuk mereload extensi bot **[Bot Owner Only]**'
RELOADEXT = '''
Command ini digunakan ketika ingin mereload suatu extensi yang
ingin direload dari botnya
'''
RELOADALLEXT_BRIEF = 'Command untuk mereload semua extensi bot **[Bot Owner Only]**'
RELOADALLEXT = '''
Command ini digunakan ketika ingin mereload semua extensi yang
digunakan botnya
'''
PING_BRIEF = 'Command untuk melihat latency bot'
PING = PING_BRIEF
SHUTDOWN_BRIEF = 'Command untuk menghentikan bot **[Bot Owner Only]**'
SHUTDOWN = '''
Command ini digunakan untuk menghentikan bot
Bot sendiri akan membackup data sebelum dihentikan
'''
