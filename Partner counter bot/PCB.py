from typing import Optional

import dotenv
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

load_dotenv()
token = os.getenv("token")

# config
prefix = "<"
print("Loading...")
counter_channel_id = int(os.getenv('channel_id'))
env_file_path = '.env'
default_count = 1


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    os.system('cls')
    print(f"bot ready for action. {bot.user.name}#{bot.user.discriminator}, {bot.user.id}")
    print(f"the bot is in {len(bot.guilds)} guilds")

# commands and on_message stuff
@bot.event
async def on_message(message: discord.Message):
    global counter_channel_id
    if message.content.startswith("<"):
        if message.author.id != discord.Guild.owner_id:
            await message.reply("Only guild owner or Director Noot can access these commands.")
            return
        elif message.author.id != 1081507207180460032:
            await message.reply("Only guild owner or Director Noot can access these commands.")
            return

        if message.content.lower() == "<test":
            await message.reply("Message Received Master")

        elif message.content.lower() == "<help":
            await message.reply(
                "Test: test bot activity (you already did).\nHelp: send this message.\nset_channel: sets channel to count the number of messages sent by users "
                "(specifically partner messages).")

        elif message.content.lower() == "<set_channel":
            counter_channel_id = message.channel.id
            dotenv.set_key(dotenv_path=env_file_path, key_to_set="channel_id", value_to_set=str(message.channel.id))
            await message.reply("counter channel set")

    if message.channel.id == counter_channel_id:
        if 'https://discord.gg' not in message.content:
            return
        author_id = str(message.author.id)
        author = message.author.mention
        dotenv.load_dotenv()
        if os.getenv(author_id) is None:
            await message.channel.send("users first partner. filing.")
            dotenv.set_key(env_file_path, author_id, str(default_count))
            await message.channel.send(f"{author} has {dotenv.get_key(env_file_path, author_id)} partners")
            return
        else:
            dotenv.load_dotenv()
            count = dotenv.get_key(env_file_path, author_id)
            new_C = int(count) + 1
            dotenv.set_key(dotenv_path=env_file_path, key_to_set=author_id, value_to_set=str(new_C))
            await message.channel.send(f"{author} has {dotenv.get_key(env_file_path, author_id)} partners")
            return

    else:
        pass


try:
    bot.run(token)
except discord.LoginFailure:
    print('Invalid Token Passed')
