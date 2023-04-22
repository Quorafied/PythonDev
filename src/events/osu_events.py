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

                if embed.fields:
                    # Check if the embed has a field with a specific name
                    for field in embed.fields:

                        # Check if a field's name has a specific description
                        if "**If FC**: PP" in field.name:
                            # Sends a choke message and set found as True
                            found = True
                            await message.channel.send("A choke, what a surprise..")
                            await channel.send(random.choice(quotes))
                            break
                    
                    # If the name with the description has not been found, say the opposite.
                    if found == False:
                        found = True
                        await message.channel.send("Nice S rank!")

                # Description was not found within the message of the specific user.
                else:
                    print("No fields")
                
                    # If description not found yet, find if there is a choke in another specific user.
                    if found == False:
                        if "FC" in embed.description:
                            found = True
                            await message.channel.send("A choke, what a surprise..")
                            await channel.send(random.choice(quotes))
                        else:
                            await message.channel.send("Nice S rank!")

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



