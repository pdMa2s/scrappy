
# Scrappy Bot

Scrappy Bot is a Discord bot that tracks prices of products and notifies you about price changes.

## Usage

usage: scrappy [-h] [-t TOKEN]

Scrappy Bot

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Discord Bot Token

The `TOKEN` argument can be passed as a command line argument, or set as an environment variable `SCRAPPY_TOKEN`.

## Commands

- `!add [url]`: Adds a product to be tracked.
- `!remove [url]`: Removes a product from the list of tracked products.
- `!list`: Lists the products that are being tracked.
- `!schedule [hour]`: Schedule a time for the bot to retrieve the prices and list them.
- `!remove_schedule [job_id]`: Removes one of the scheduled prices retrievals and listing.
- `!list_schedules`: Lists all the schedules for the price retrievals.

## Installation

1. Clone the repository: `git clone https://github.com/your_username/scrappy-bot.git`.
2. Navigate to the cloned directory: `cd scrappy-bot`.
3. Install the required packages: `pip install -r requirements.txt`.
4. Create the database: `python create_db.py`.
5. Run the bot: `python bot.py`.
