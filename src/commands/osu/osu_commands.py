import discord
from discord.ext import commands
from osu import *
from imageRecgonition import *
from main import function

# Creates offset
def handlePagination(content):
    sub_string = " -i "
    print(f"CONTEEEEEEEEEENT .{content}.")
    index = content.find(sub_string)
    print(len(content))
    if index != -1:
        username = content[:-5]
        
        if len(content) == 5:
            return False, False

        lastIndex = int(content[-1])
        print(f"lastIndex: {lastIndex}")
        pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        if lastIndex in pages:
            return lastIndex*10, username
        else:
            return 0, content
    else:
        return 0, content
    
class osuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="top")
    async def giveDetails_username(self, ctx):
        Target_Channel_ID = ctx.channel.id
        content = ctx.message.content.strip()
        command_substring = "q.top"
        content = content.replace(command_substring, "")
        

        print(content)
        print(f"CONTEEEEEEEEEENT {content[:-5]}")

        offset, content = handlePagination(content)
        print(offset, content)
        if offset == False and content == False:
            ws.toSend_Message = "No username provided"
            if ctx.author.id == ui.ownId:
                ws.send_response(ui.targetChannelId)

            await self.bot.get_channel(Target_Channel_ID).send(ws.toSend_Message)
            return False
        
        # Update content to suit username after checking pagination
        content = content[1:]

        
        user_data = api.user(content, mode="osu", key="username")


        user_scores_data = api.user_scores(user_data.id, type="best", mode="osu", limit=10, offset=offset)
        #print(user_scores_data)
        stringToSend = ""
        # print(f"\n\n\n\n {api.beatmap(user_scores_data[0].beatmap.id).max_combo} \n\n\n\n")

        title = f"Top plays for {user_data.username}\n"
        stringToSend = title
        for index, map in enumerate(user_scores_data):
            score_grade = handleGrade(map.rank)
            
            map_details = f"**{index+offset+1}. {map.beatmapset.title} [{map.beatmap.version}]** {map.mods} [{map.beatmap.difficulty_rating}★]\n"
            score_details = f"> **{score_grade}**    **{int(map.pp)}PP**    {(map.accuracy*100):.2f}%\n> {map.score:,}    x{map.max_combo:,}/{getScore_max_combo(map):,}    "           
            score_hits = f"[{map.statistics.count_300}/{map.statistics.count_100}/{map.statistics.count_50}/{map.statistics.count_miss}]\n"
            stringToSend += map_details+score_details+score_hits
        print(stringToSend)

        if ctx.author.id == ui.ownId:
            ws.toSend_Message = stringToSend
            ws.send_response(ui.targetChannelId)

        await self.bot.get_channel(Target_Channel_ID).send(stringToSend)

    @commands.command(name="osu")
    async def getProfile(self, ctx):
        content = ctx.message.content.strip()
        command_substring = "q.osu "

        content = content.replace(command_substring, "")

        Target_channel_ID = ctx.channel.id
        user_data = api.user(content, mode="osu", key="username")

        Title = f"Profile for {user_data.username}\n"
        description = f"> **Global Rank**: #{user_data.statistics.global_rank}\n> **Level**: {user_data.statistics.level.current}\n> **PP**: {user_data.statistics.pp:.2f}\n> **Playcount**: {user_data.statistics.play_count} **Playtime**: {user_data.statistics.play_time}"
        string = Title+description
        print(string)

        if ctx.author.id == ui.ownId:
            ws.toSend_Message = string
            ws.send_response(ui.targetChannelId)
        
        await self.bot.get_channel(Target_channel_ID).send(string)
