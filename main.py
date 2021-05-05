import discord
import asyncio
# Create the client object
client = discord.Client()

# Startup notification
@client.event
async def on_ready():
    print('Logged in as\n' + client.user.name + '\n' + str(client.user.id) + '\n------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("boof"))
    await client.get_channel(762152576032047156).send("Krug Bot online!\n*boof boof boof*")

# Reacting to message being sent anywhere in the server
@client.event
async def on_message(message):
    code = message.content[-6:]
    line = message.content[:-6]
    if line == "Join my coop game on Bloons TD 6! https://join.btd6.com/Coop/":
        await client.get_channel(762152576032047156).send(code)
        await discord.Message.delete(message)


client.run()