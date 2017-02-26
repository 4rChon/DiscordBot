import discord

from bot.core import Core

def main():
    core = Core(discord.Client())
    core.run_client()

if __name__ == '__main__':
    main()
