import os
from requests import get
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from json import dumps, loads
import openai
from choose_res import choose_res
from proc_res import org_res

openai.api_key = os.getenv('OPEN_AI_TOKEN')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
print(client)
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        print(message)
        msg = message.content.split("> ")[1].strip()
        await message.channel.send(f'{message.author.mention} {choose_res(msg)}')

client.run(TOKEN)
