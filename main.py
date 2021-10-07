import os
my_secret = os.environ['TOKEN']
import discord
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "depressing", "angry", "miserable", "depressing"]

words_of_encouragement = ["Plis don't die",
 "I am here for you, virtually",
 "Sadness is Temporary, monke is eternal. Return to monke"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"]+ "\n" + "                                     -" + json_data[0]["a"]
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  

@client.event
async def on_ready():
  print("we have logged on as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$hello"):
    await message.channel.send("Hello_OwO")
  
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  options = words_of_encouragement
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(words_of_encouragement))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    


client.run(my_secret)