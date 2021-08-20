import discord
import os
import time
from replit import db


client = discord.Client()

if not "players" in db.keys():
  db["players"] = ""
  print('Creating player list')


def do_localtime(epoch_time):
  day = time.localtime(epoch_time)[2]

  months = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December']

  month = months[time.localtime(epoch_time)[1]-1]

  year = time.localtime(epoch_time)[0]
  hour = ('00' + str(time.localtime(epoch_time)[3]))[-2:]
  minute = ('00' + str(time.localtime(epoch_time)[4]))[-2:]

  weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', ]
  weekday = weekdays[time.localtime(epoch_time)[6]-1]

  return f'{weekday}, {day}. of {month} {year}, at {hour}:{minute}'



def do_dong(user_id, user_name, dong_type):
#  print(f'{user_id}, {user_name}, {dong_type}')
  nu = time.time()
  if user_id in db["players"].split(", "):
    user_str = db[user_id]
    user_name, dongs, last_dong, self_dongs, last_self_dong = user_str.split(", ")
    if dong_type == 1:
      last_dong = float(last_dong)
      dongs = int(dongs) + 1
      db_string = f'{user_name}, {dongs}, {nu}, {self_dongs}, {last_self_dong}'
      db[user_id] = db_string
      return dongs, last_dong
    else:
      last_self_dong = float(last_self_dong)
      self_dongs = int(self_dongs) + 1
      db_string = f'{user_name}, {dongs}, {last_dong}, {self_dongs}, {nu}'
      db[user_id] = db_string
      return self_dongs, last_self_dong

  else:
    if dong_type == 1:
      db_string = f'{user_name}, 1, {nu}, 0, 0'
    else:
      db_string = f'{user_name}, 0, 0, 1, {nu}'
    print(f'Creating new player, {user_name}')
    player_str = db["players"]
    if player_str == "":
      player_str = user_id
    else:
      player_str += ", " + user_id

    db["players"] = player_str
    db[user_id] = db_string
    return 1, 0

def do_standings():
  stats = []
  for player in db["players"].split(", "):
    try:
      user_str = db[player]
      user_name, dongs, last_dong, self_dongs, last_self_dong = user_str.split(", ")
      stats.append((user_name, int(dongs), int(self_dongs)))
      dong_top = sorted(stats, key=lambda tup: tup[1], reverse=True)
      self_dong_top = sorted(stats, key=lambda tup: tup[2], reverse=True)
    except:
      print('error doing standings')

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
    dongs, last_dong = do_dong(str(user_id), user_name, 1)
    if last_dong == 0:
      last_dong = "Never!"
    else:
      last_dong = do_localtime(last_dong)

    await message.reply(f'DONG!! {user_name} has scored! {user_name} now has {dongs} dongs! Last dong was: {last_dong}')

  if msg.startswith('!selfdong') or msg.startswith('!SelfDong'):
    dongs, last_dong = do_dong(str(user_id), user_name, 2)
    if last_dong == 0:
      last_dong = "Never!"
    else:
      last_dong = do_localtime(last_dong)

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