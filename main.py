#!/usr/bin/env python3
import discord
from discord_slash import SlashCommand
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
import yeelight
import re

# Initialisation and constant definition
client = commands.Bot(command_prefix='/')
slash = SlashCommand(client, sync_commands=True)

secret = open('client_secret.txt', 'r').read()
settings = {"general_channel_id": 762152576032047156,
            "bot_channel_id": 762224452440031284,
            "server_id": [762152575381536798],
            "bulb_ip": "192.168.1.65",
            "light_control": False,
            "developer_id": 319603023137472512
            }

bulb = yeelight.Bulb(settings["bulb_ip"])


@client.event
async def on_ready():
    print('Logged in as\n' + client.user.name + '\n' + str(client.user.id) + '\n------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("boof"))
    # await client.get_channel(settings["bot_channel_id"]).send("Krug Bot online!\n*boof boof boof*")


@slash.slash(name="light",  # Create a slash command object
             guild_ids=settings["server_id"],
             description="Change Light",
             options=[
                 create_option(
                     name="brightness",
                     description="Change brightness of light",
                     option_type=4,
                     required=False
                 ),
                 create_option(
                     name="power",
                     description="Turn the light on or off",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="On",
                             value="True"
                         ),
                         create_choice(
                             name="Off",
                             value=""
                         )
                     ]
                 ),
                 create_option(
                     name="rgb",
                     description="RGB value for light. \"Format 255 255 255\"",
                     option_type=3,
                     required=False
                 ),
                 create_option(
                     name="control",
                     description="Enable or Disable lighting control",
                     option_type=5,
                     required=False
                 )
             ]
             )
async def light_brightness(ctx, brightness=None, power=None, rgb=None, control=None):  # Command function
    option = list(ctx.kwargs.keys())[0]
    if (option == "brightness") and (settings["light_control"]):
        if (brightness < 0) | (brightness > 100):
            await ctx.send("Brightness value must be from 0 to 100 inclusive")
        else:
            bulb.set_brightness(brightness)
            await ctx.send(f"Brightness set to {brightness}")

    elif option == "power" and settings["light_control"]:
        if bool(power):
            bulb.turn_on()
            await ctx.send("Light turned on")
        else:
            bulb.turn_off()
            await ctx.send("Light turned off")

    elif option == "rgb" and settings["light_control"]:
        regex_match = re.search(r"^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\s){2}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", rgb)

        if regex_match is not None:
            rgb_values = rgb.split(" ")
            bulb.set_rgb(int(rgb_values[0]), int(rgb_values[1]), int(rgb_values[2]))
            await ctx.send(f"Light color set to Red:{rgb_values[0]} Green:{rgb_values[1]} Blue:{rgb_values[2]}")
        else:
            await ctx.send("Invalid response. Input format is three numbers from 0 - 255 inclusive, separated by a "
                           "space")

    elif option == "control":
        if ctx.author_id == settings["developer_id"]:
            if control:
                settings["light_control"] = True
                await ctx.send("Lighting control enabled")
            else:
                settings["light_control"] = False
                await ctx.send("Lighting control disabled")
        else:
            await ctx.send("You do not have permission to change this")

    else:
        await ctx.send("Light control is disabled")


@client.event  # Reacting to message being sent anywhere in the server
async def on_message(message):
    code = message.content[-6:]
    line = message.content[:-6]
    if line == "Join my coop game on Bloons TD 6! https://join.btd6.com/Coop/":
        await discord.Message.delete(message)
        await client.get_channel(message.channel.id).send(code)


client.run(secret)
