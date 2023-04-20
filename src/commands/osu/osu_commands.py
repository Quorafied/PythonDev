import discord
from discord.ext import commands
from osu import *
from imageRecgonition import *
from main import function

class osuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="top5")
    async def giveDetails_username(self, ctx):
        content = ctx.message.content.strip()
        command_substring = "q.top5 "

        content = content.replace(command_substring, "")
        print(content)
        print("")
        Target_Channel_ID = ctx.channel.id
        user_data = api.user(content, mode="osu", key="username")

        user_scores_data = api.user_scores(user_data.id, type="best", mode="osu", limit=5)
        #print(user_scores_data)
        stringToSend = ""

        for index, map in enumerate(user_scores_data):
            
            This_string = f"**{index+1}.** {map.beatmapset.title}\n> **{int(map.pp)}PP**\n> Accuracy: {(map.accuracy*100):.2f}% Combo: x{map.max_combo}/{map.beatmap.max_combo}\n"
            stringToSend += This_string
            print(stringToSend)
        print(stringToSend)
        ws.toSend_Message = stringToSend
        ws.send_response(ui.targetChannelId)

        await self.bot.get_channel(Target_Channel_ID).send(stringToSend)

    @commands.command(name="getUserProfile")
    async def getProfile(self, ctx):
        content = ctx.message.content.strip()
        command_substring = "q.getUserProfile "

        content = content.replace(command_substring, "")

        Target_channel_ID = ctx.channel.id
        user_data = api.user(content, mode="osu", key="username")

        Title = f"Profile for {user_data.username}\n"
        description = f"> **Global Rank**: #{user_data.statistics.global_rank}\n> **Level**: {user_data.statistics.level.current}\n> **PP**: {user_data.statistics.pp:.2f}\n> **Playcount**: {user_data.statistics.play_count} **Playtime**: {user_data.statistics.play_time}"
        string = Title+description
        print(string)

        ws.toSend_Message = string
        ws.send_response(ui.targetChannelId)
        
        print("ws.send_response")
        await self.bot.get_channel(Target_channel_ID).send(string)
