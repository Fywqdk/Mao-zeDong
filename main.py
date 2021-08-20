import discord
import os
import time
from replit import db


client = discord.Client()


players = {}


class Player(object):
  def __init__(self, user_name, user_id):
    self.user_name = user_name
    self.user_id = user_id
    self.dongs = 0
    self.last_dong = 'Never'
    self.self_dongs = 0
    self.last_self_dong = 'Never'

  def dong(self):
    self.dongs += 1
    last_dong = self.last_dong
    now = time.time()
    self.last_dong = time.ctime(now)
    return self.dongs, last_dong

  def self_dong(self):
    self.self_dongs += 1
    last_self_dong = self.last_self_dong
    now = time.time()
    self.last_self_dong = time.ctime(now)
    return self.self_dongs, last_self_dong


def do_dong(user_id, user_name):
#  players = db["data_dict"]
  if user_id in players.keys():
    player = players[user_id]
    dongs, last_dong = player.dong()
    players[user_id] = player
  else:
    try:
      player = Player(user_name, user_id)
      dongs, last_dong = player.dong()
      players[user_id] = player
    except:
      print("could not add player")
      dongs = 0
      last_dong = "error"

#  db["data_dict"] = players
  return dongs, last_dong


def do_self_dong(user_id, user_name):
#  players = db["data_dict"]
  if user_id in players.keys():
    player = players[user_id]
    dongs, last_dong = player.self_dong()
    players[user_id] = player
  else:
    try:
      player = Player(user_name, user_id)
      dongs, last_dong = player.self_dong()
      players[user_id] = player
    except:
      print("could not add player")
      dongs = 0
      last_dong = "error"

#  db["data_dict"] = players
  return dongs, last_dong


def do_standings():
#  players = db["data_dict"]
  stats = []
  for key in players:
    player = players[key]
    stats.append((player.user_name, player.dongs, player.self_dongs))
  dong_top = sorted(stats, key=lambda tup: tup[1], reverse=True)
  self_dong_top = sorted(stats, key=lambda tup: tup[2], reverse=True)
  return dong_top, self_dong_top


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

  if msg.startswith('!dong') or msg.startswith('!Dong'):
    dongs, last_dong = do_dong(user_id, user_name)
    await message.reply(f'DONG!! {user_name} has scored! {user_name} now has {dongs} dongs! Last dong was: {last_dong}')

  if msg.startswith('!selfdong') or msg.startswith('!SelfDong'):
    dongs, last_dong = do_self_dong(user_id, user_name)
    await message.reply(f'SELFDONG!! {user_name} has been good to themself! {user_name} now has {dongs} selfdongs! Last selfdong was: {last_dong}')

  if msg.startswith('!standings'):
    dong_top, self_dong_top = do_standings()

    await message.reply('__*DONG STANDINGS*__')
    dong_str = ""
    for i, player in enumerate(dong_top):
      if i < 3:
        dongs = player[1]
        user_name = player[0]
        dong_str += f'{i+1}. {dongs} dongs - {user_name}\n'
    await message.channel.send(dong_str)

    await message.channel.send('__*SELFDONG STANDINGS*__')
    self_dong_str = ""
    for i, player in enumerate(self_dong_top):
      if i < 3:
        self_dongs = player[2]
        user_name = player[0]
        self_dong_str += f'{i+1}. {self_dongs} selfdongs - {user_name}\n'
    await message.channel.send(self_dong_str)


client.run(os.environ['TOKEN_PASS'])