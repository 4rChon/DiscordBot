import asyncio
import discord

from bot.core import Core

# import nltk

def main():
    core = Core(discord.Client())
    core.runClient()
    

if __name__ == '__main__':
    main()
