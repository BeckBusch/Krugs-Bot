import discord
import asyncio

# Initialisation and constant definition
client = discord.Client()
secret = open('client_secret.txt', 'r').read()
settings = {"general_channel_id": 762152576032047156,
            "bot_channel_id": 762224452440031284
            }

# Startup notification
@client.event
async def on_ready():
    print('Logged in as\n' + client.user.name + '\n' + str(client.user.id) + '\n------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("boof"))
    await client.get_channel(settings["bot_channel_id"]).send("Krug Bot online!\n*boof boof boof*")

# Reacting to message being sent anywhere in the server
@client.event
async def on_message(message):
    code = message.content[-6:]
    line = message.content[:-6]
    if line == "Join my coop game on Bloons TD 6! https://join.btd6.com/Coop/":
        await discord.Message.delete(message)
        await client.get_channel(message.channel.id).send(code)


client.run(secret)