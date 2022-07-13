# EmakBot
A moderation bot originally made for [Sebug Gang](https://discord.gg/3UAYsR7wZ3).
A discord server from a youtuber [Sebud Channel](https://www.youtube.com/c/SebudChannel).

The idea for this bot is to add a `warning` with some time period and with its own levels.
Other than that everything is the same as any other moderation bots.

## Usage
```
?warn <user (mention)/user id> <reason> [level=1] [duration='1 hari']
```
The default max `level` is level 2 and for `duration` you can specify it from seconds to days
since it's an Indonesian server some text was still in indonesian,
this includes the regex pattern for the duration</br>
hari = days</br>
jam = hours</br>
menit = minutes</br>
detik = seconds</br>

All the moderation commands will be sent to 3 channels which is
the channel the command was triggered, `#warnings` channel and user's dm

You can specify these channel IDs in the `.env` file
```
WARN_CH_ID=<warning channel id>
MOD_CH_ID=<moderation channel id>
```

## Development
If you want to try some things to the bot you can put a `Bot Development` Channel id in the `.env
file
```
BOT_DEV_CH_ID=<bot development channel id>
```

## Run
To run the bot you need to put these in the `.env` file
```
BOT_TOKEN=<yout bot token>
AUTHOR_ID=<bot owner id>
GUILD_ID=<server id>
```
and so you can run with
```
python main.py
```
