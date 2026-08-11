Discord personal bot, written in python. Using [`discord.py`](https://github.com/Rapttz/discord.py).

# Setup and running 
Clone this repo. Then, run:
```bash
pip install -r requirements.txt
python3 db-setup.py
```
Then to run the bot:
```bash
python3 bot.py
```

# Contributing
Follow setup instructions above. Fork the repo. Then, make sure to install the dev dependencies using:
```bash
pip install -r requirements-dev.txt
```

Before pushing changes, please ensure to run
```bash
ruff check .
ruff format .
```
The first command runs a linter. You must fix all the problems the linter reports before pushing changes. The second command just formats the code.