import os

import discord
from dotenv import load_dotenv 
from choose_res import choose_res
import re 

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
def main():
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

            print(message.channel.name)
            if message.channel.name == 'bot-testing':
                avt = message.author.avatar_url
                content = message.content.strip()
                msg = "".join(re.split("<@!\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d>", content))
                await message.channel.trigger_typing()
                res = choose_res(msg, avt)
                await message.channel.send(f'{message.author.mention} {res}')

    client.run(TOKEN)
    
if __name__ == '__main__':
    main()