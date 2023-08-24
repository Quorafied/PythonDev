import discord
from discord.ext import commands
import random
from main import function
from quotes import *

class osuEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        # Function to check if an embed is a choke
    async def chokeCheck(self, message):    
        #await client.process_commands(message)
        channel = message.channel

        # If the author is not the bot and the message is from a specific user
        if (message.author.id != function.botId and message.author.id == 289066747443675143) or (message.author.id != function.botId and message.author.id == 297073686916366336):
            if message.embeds:
                print(message.embeds)
                found = False
                embed = message.embeds[0]
                #await message.channel.send(embed=embed)

                # BathBot
                if message.author.id == 297073686916366336 and embed.fields:
                    try:
                        if embed.fields[6].name == '**If FC**: PP':
                            await channel.send(random.choice(quotes))
                        else:
                            await channel.send("Nice S rank!")
                    except IndexError:
                        pass

                elif message.author.id == 289066747443675143: 
                    if ":rankingS:" not in embed.description:
                        await channel.send(random.choice(quotes))
                    elif ":rankingS:" in embed.description:
                        await channel.send("Nice S rank!")


    # Function to insult users
    async def insult(self, message):
        #await client.process_commands(message)
        channel = message.channel

        # If insult toggle is on and the author is not the bot
        if function.noToggle == True:
            if message.author.id != function.botId:
                # Check if message is not a command or mention
                if len(message.content.split()) <= 1 and not message.content.startswith("<") and not message.content.startswith(">"):
                    print(message.content)
                    # Send insult
                    await channel.send("no {}".format(message.content))



