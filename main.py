import discord
import os
import time
import sqlite3

con = sqlite3.connect('work_out.db')

cur = con.cursor()

print("Opened database successfully")


client = discord.Client()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    user_name = message.author.display_name
    user_id = message.author.id

    if msg.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)

    if msg.startswith('!done') or msg.startswith('!Done'):
        await message.reply(
            f'Well done, {message.author.display_name}'
        )

client.run(os.environ['TOKEN_PASS'])
