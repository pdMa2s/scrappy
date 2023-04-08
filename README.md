# Scrappy Bot

Scrappy Bot is a Discord bot that tracks prices of products and notifies you about price changes.

## Usage

usage: 
```shell
python main.py [-h] [-t --tokken] [-c --channel]
```

optional arguments:

-   -h, --help -> show this help message and exit

-   -t, --token TOKEN -> Discord Bot Token. 
The `TOKEN` argument can be passed as a command line argument, or set as an environment variable `SCRAPPY_TOKEN`.
  
- -c, --channel `CHANNEL` -> The channel to where the bot will show the product prices. 
If not provided it will default to the first guild's channel.

## Commands

- `!add [url]`: Adds a product to be tracked.
- `!remove [url]`: Removes a product from the list of tracked products.
- `!list`: Lists the products that are being tracked.
- `!interval [hours]`: Set a time interval in hours for the bot to retrieve the prices and list them

## Installation
1. [Create a Bot account on Discord](https://discordpy.readthedocs.io/en/stable/discord.html)
2. Copy the bot's token. 
3. Clone the repository: `git clone https://github.com/pdMa2s/Scrappy.git`.
4. Navigate to the cloned directory: `cd scrappy`.
5. .Install the required packages: `pip install -r requirements.txt`.

## Supported websites
This list will increase with time. **If you have a website that you would like to see supported, please feel free to
mention it on an issue.**

- [digitec.ch](https://www.digitec.ch/)
- [amazon.com](https://www.amazon.com/)
- [ottos](https://www.ottos.ch/)