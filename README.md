Discord personal bot, written in python. Using [`discord.py`](https://github.com/Rapttz/discord.py).

# Setup and running 
Clone this repo. Then, run:
```sh
pip install -r requirements.txt
python3 db-setup.py
```
To run the bot:
```sh
python3 bot.py # or dummy.py
```

# Dummy bot
In commit [8c820df](https://github.com/E9Cipher/tiogilito/commit/8c820dfd01eb261abbeee2ba7f87c604e6e0fd12) a second bot based
on the original file was added. It was created in order for the original bot to interact with it (something like a test user).
Please note that a bot is not the same as a human user, so expect some things not to be avaliable. This bot must be run separately
and has a different discord key than the original.

## `.env` discord key format
```text
DISCORD_TOKEN=<YOUR_TOKEN_HERE>
DISCORD_DUMMY_TOKEN=<OTHER_TOKEN_HERE>
```