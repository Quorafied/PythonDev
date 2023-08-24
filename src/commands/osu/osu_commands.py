from _ownLibrary import *
from osu import *
from imageRecgonition import *
from database._database import *
from main import function
from commands.osu.pp_calculate import ppCalculator
from datetime import datetime, timedelta
from commands.osu.cmdHandler import cmdHandler

class osuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gradeSS = "<:gradeSS:1102283167769055353>"
        self.gradeS = "<:gradeS:1102283126220275763>"
        self.gradeA = "<:gradeA:1102279988763439236>"
        self.gradeB = "<:gradeB:1102282758476288030>"
        self.gradeC = "<:gradeC:1102283066396901477>"
        self.gradeD = "<:gradeD:1102283093425016922>"
        self.gradeF = "<:gradeF:1102285620115669053>"
        self.gradeSH = "<:gradeSH:1102283196466483261>"
        self.gradeSSH = "<:gradeSSH:1102283225348452533>"
        self.fc = "<:gradeFC:1102283256021397748>"

        self.lastScoreSent = None
        
    def createTimestamp(self, timestamp):
        time_stamp = timestamp

        previous_time = datetime.fromisoformat(time_stamp)

        time_stamp = int(previous_time.timestamp())
        return f"<t:{time_stamp}:R>"

    def handleGrade(self, grade):
        rank = grade
        if rank == grade.SS:
            return self.gradeSS, "SS"
        
        if rank == grade.S:
            return self.gradeS, "S"
        
        if rank == grade.A:
            return self.gradeA, "A"
        
        if rank == grade.B:
            return self.gradeB, "B"
        
        if rank == grade.C:
            return self.gradeC, "C"
        
        if rank == grade.D:
            return self.gradeD, "D"
        
        if rank == grade.F:
            return self.gradeF, "F"
        
        if rank == grade.SH:
            return self.gradeSH, "SH"
        
        if rank == grade.SSH:
            return self.gradeSSH, "SSH"
        
    def handleScore(self, score, user_data):
        score_grade = self.handleGrade(score.rank)
        self.lastScoreSent = score

        # Calculate score
        ppCalculator.newScore(score, self.lastScoreSent.beatmap)
        pp = f"{ppCalculator.computeValues():.2f}"
        beatmapMaxCombo = getScore_max_combo(score)

        self.lastScoreSent = score.beatmap

        diffRating = f"{ppCalculator.beatmapDifficultyAttribute.attributes.star_rating:.2f}"

        score_url = f"https://osu.ppy.sh/beatmapsets/{score.beatmapset.id}#osu/{score.beatmap.id}"

        sendString = ""
        
        title = f"Recent play for {user_data.username}\n"
        map_details = f"**{score.beatmapset.title} [{score.beatmap.version}]** {score.mods} [{diffRating}★]\n"
        score_details = f"**{score_grade[0]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
        score_hits = f"[{score.statistics.count_300}/{score.statistics.count_100}/{score.statistics.count_50}/{score.statistics.count_miss}]\n"
        
        set_at = self.createTimestamp(str(score.created_at))

        wsMap_details = f"**{score.beatmapset.title} [{score.beatmap.version}]** {score.mods} [{diffRating}★]\n"
        wsScore_details = f"> **{score_grade[1]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n > {score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
        
        
        # Check if FC and provide prediction if not FC
        if (beatmapMaxCombo - score.max_combo) > (int(beatmapMaxCombo/100)):
            
            reAccuracy = ppCalculator.recalculateAccuracy(ppCalculator.num300, ppCalculator.num100, ppCalculator.num50, ppCalculator.numMiss)
            
            ppCalculator.num300 += ppCalculator.numMiss
            ppCalculator.numMiss = 0

            ppCalculator.recalculateComb()
            rePP = f"{ppCalculator.computeValues():.2f}"

            score_details = f"**{score_grade[0]}**    **{pp}PP**  ({rePP}PP for {reAccuracy}%)  {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
            wsScore_details = f"> **{score_grade[1]}**    **{pp}PP**  ({rePP}PP for {reAccuracy}%)  {(score.accuracy*100):.2f}%\n> {score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "

        else:
            score_details = f"**{score_grade[0]}**  {self.fc}   **{pp}PP**  {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
            wsScore_details = f"> **{score_grade[1]}**  **FC**   **{pp}PP**  {(score.accuracy*100):.2f}%\n> {score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
        
        
        sendString = title+wsMap_details+wsScore_details+score_hits+f"**{set_at}**"
        
        embed = Embed(
            title=f"{map_details}",
            url = score_url,
            timestamp = score.created_at,
            color=Color.from_rgb(243, 205, 140)
        )

        embed.add_field(name = "", value = f"{score_details}{score_hits}**{set_at}**")

        # embed.set_image(url = user_data.avatar_url)
        embed.set_image(url = score.beatmapset.covers.cover_2x)
        embed.set_thumbnail(url = user_data.avatar_url)
        embed.set_author(name = f"{title}", url = f"https://osu.ppy.sh/users/{user_data.id}", icon_url = user_data.avatar_url)
        embed.set_footer(text = "Played")


        embedMsg = [title, embed]

        # embed.add_field(name="Uptime:", value=self.show_upTime(), inline=True)

        return embedMsg, sendString, pp


    @commands.command(name="osulink")
    async def osuLink(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        osuUsername, Target_Channel_ID, error = cmdHandler.handle_osulink(ctx)

        if error:
            await self.bot.get_channel(Target_Channel_ID).send(error)
            return False

        try:
            api.user(osuUsername, mode="osu", key="username")
        except ValueError:
            await self.bot.get_channel(Target_Channel_ID).send("User not found")
            return False

        if db.linkUsers(ctx.author.id, osuUsername) == True:
            await self.bot.get_channel(Target_Channel_ID).send(f"Linked {ctx.author.name} to Osu! Username: {osuUsername}")

        elif db.linkUsers(ctx.author.id, osuUsername) == "Existing":
            await self.bot.get_channel(Target_Channel_ID).send(f"You are already linked to Osu! Username: {osuUsername}")

        else:
            await self.bot.get_channel(Target_Channel_ID).send(f"Could not link {ctx.author.name} to Osu! Username: {osuUsername}")
    

    @commands.command(name="rs")
    async def recentPlay2(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        await self.recentPlay(ctx, "q.rs")
    
    @commands.command(name="recent")
    async def recentPlay(self, ctx, command_substring=None):
        if ctx.guild.id == 1131290601233600662:
            return False

        if command_substring == "q.rs": command_substring = "q.rs"
        else: command_substring = "q.recent"
        
        try:
            username, Target_Channel_ID, authorId, error = cmdHandler.hamdle_recent(ctx, command_substring, ctx.message.raw_mentions)
            if error:
                self.bot.get_channel(Target_Channel_ID).send(error)
                return False
        except Exception as e:
            await self.bot.get_channel(1100401940719992853).send(e.with_traceback(e.__traceback__))
            
        if not username:
            username = db.associateUsernames(authorId)

            if username:
                user_data = api.user(username, mode="osu", key="username")

            else:
                await self.bot.get_channel(Target_Channel_ID).send("You are not currently linked to an osu account. Please use `q.osulink <username>` and try again.")
                return False
            
        else:
            try:
                print(username)
                user_data = api.user(username, mode="osu", key="username")
            except ValueError:
                await self.bot.get_channel(Target_Channel_ID).send(f"No user found")
                return False

        last_score = api.user_scores(user_data.id, type="recent", mode="osu", limit=1, include_fails=True)
        
        if len(last_score) == 0:
            await self.bot.get_channel(Target_Channel_ID).send(f"**`{user_data.username}` has no recent osu! Standard plays.**")

        latest_score = last_score[0]
        self.lastScoreSent = latest_score

        embedMsg, sendString, _ = self.handleScore(latest_score, user_data)

        await self.bot.get_channel(Target_Channel_ID).send(embed = embedMsg[1])
            

    @commands.command(name="top")
    async def giveDetails_username(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        command_substring = "q.top"
        # Check aliases and username (if no mentions, handled inside the function.)
        try:
            username, Target_Channel_ID, authorId, offset, playIndex, error = cmdHandler.handle_top(ctx, command_substring, ctx.message.raw_mentions)
            # debug 
            # await self.bot.get_channel(Target_Channel_ID).send(f"{username}, {Target_Channel_ID}, {authorId}, {offset}, {playIndex}")
            if error:
                await self.bot.get_channel(Target_Channel_ID).send(error)
                return False

        except Exception as e:
            await self.bot.get_channel(1100401940719992853).send(e.with_traceback(e.__traceback__))

        # If the there are no usernames given, associate the authorId with an osu username, otherwise, username is used to get information.
        if not username:
            username = db.associateUsernames(authorId)

            if username:
                user_data = api.user(username, mode="osu", key="username")

            else:
                await self.bot.get_channel(Target_Channel_ID).send("You are not currently linked to an osu account. Please use `q.osulink <username>` and try again.")
                return False
            
        else:
            try:
                user_data = api.user(username, mode="osu", key="username")
            except ValueError:
                await self.bot.get_channel(Target_Channel_ID).send(f"No user found")
                return False

        # Set offset to 0 if no offset given.
        if not offset:
            offset = 0
        
        # If playIndex provided, give the top play with given playIndex.
        if playIndex:
            score = (api.user_scores(user_data.id, type="best", mode="osu", limit=1, offset=playIndex-1))[0]
            self.lastScoreSent = score.beatmap

            title = f"Top play #{playIndex} for {user_data.username}\n"
            
            wsToSend = title
            score_EmbedData = ""

            # Calculate score
            ppCalculator.newScore(score, self.lastScoreSent)
            pp = f"{ppCalculator.computeValues():.2f}"
            beatmapMaxCombo = getScore_max_combo(score)

            diffRating = f"{ppCalculator.beatmapDifficultyAttribute.attributes.star_rating:.2f}"
            score_grade = self.handleGrade(score.rank)

            score_url = f"https://osu.ppy.sh/beatmapsets/{score.beatmapset.id}#osu/{score.beatmap.id}"

            
            map_details = f"**{score.beatmapset.title} [{score.beatmap.version}]** {score.mods} [{diffRating}★]\n"
            score_details = f"**{score_grade[0]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
            score_hits = f"[{score.statistics.count_300}/{score.statistics.count_100}/{score.statistics.count_50}/{score.statistics.count_miss}]\n"
            
            set_at = self.createTimestamp(str(score.created_at))

            wsMap_details = f"**{score.beatmapset.title} [{score.beatmap.version}]** {score.mods} [{diffRating}★]\n"
            wsScore_details = f"> **{score_grade[1]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n > {score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "

            wsToSend = title+wsMap_details+wsScore_details+score_hits+f"**{set_at}**"

            # Setting up embed
            embed = Embed(
                title=f"{map_details}",
                url = score_url,
                timestamp = score.created_at,
                color=Color.from_rgb(243, 205, 140)
            )
            
            embed.add_field(name = "", value = f"{score_details}{score_hits}**{set_at}**")

            embed.set_image(url = score.beatmapset.covers.cover_2x)
            embed.set_thumbnail(url = user_data.avatar_url)
            embed.set_author(name = f"{title}", url = f"https://osu.ppy.sh/users/{user_data.id}", icon_url = user_data.avatar_url)
            embed.set_footer(text = "Played")

            # Checking author.id for WS.
            if ctx.author.id == ui.ownId:
                ws.toSend_Message = wsToSend
                ws.send_response(ui.targetChannelId)
            
            await self.bot.get_channel(Target_Channel_ID).send(embed=embed)


        elif playIndex is False:
            user_scores_data = api.user_scores(user_data.id, type="best", mode="osu", limit=10, offset=offset)
            
            title = f"Top plays for {user_data.username}\n"

            wsToSend = title
            score_EmbedData = ""


            embed = Embed(color=Color.from_rgb(243, 205, 140))
            
            for index, map in enumerate(user_scores_data):
                diffRating = api.beatmap_attributes(map.beatmap.id, mods=map.mods, ruleset='osu')
                diffRating = f"{diffRating.attributes.star_rating:.2f}"
                beatmapMaxCombo = getScore_max_combo(map)

                set_at = self.createTimestamp(str(map.created_at))

                score_grade = self.handleGrade(map.rank)

                url = f"https://osu.ppy.sh/beatmapsets/{map.beatmapset.id}#osu/{map.beatmap.id}"

                map_details = f"**{index+offset+1}**. **[{map.beatmapset.title} [{map.beatmap.version}]]({url})** {map.mods} [{diffRating}★]\n"
                score_details = f"**{score_grade[0]}**    **{map.pp:.2f}PP**    {(map.accuracy*100):.2f}%\n{map.score:,}    x{map.max_combo:,}/{beatmapMaxCombo:,}    "           
                score_hits = f"[{map.statistics.count_300}/{map.statistics.count_100}/{map.statistics.count_50}/{map.statistics.count_miss}]"


                if (beatmapMaxCombo - map.max_combo) < (int(beatmapMaxCombo/100)):
                    score_details = f"**{score_grade[0]}**  {self.fc}    **{map.pp:.2f}PP**    {(map.accuracy*100):.2f}%\n{map.score:,}    x{map.max_combo:,}/{beatmapMaxCombo:,}    "

                    wsMap_details = f"**{index+offset+1}**. **{map.beatmapset.title} [{map.beatmap.version}]** {map.mods} [{diffRating}★]\n"
                    wsScore_details = f"> **{score_grade[1]}**  **FC**    **{map.pp:.2f}PP**    {(map.accuracy*100):.2f}%\n> {map.score:,}    x{map.max_combo:,}/{beatmapMaxCombo:,}    "
                    
                else:
                    score_details = f"**{score_grade[0]}**    **{map.pp:.2f}PP**    {(map.accuracy*100):.2f}%\n{map.score:,}    x{map.max_combo:,}/{beatmapMaxCombo:,}    "   
                    
                    wsMap_details = f"**{index+offset+1}**. **{map.beatmapset.title} [{map.beatmap.version}]** {map.mods} [{diffRating}★]\n"
                    wsScore_details = f"> **{score_grade[1]}**    **{map.pp:.2f}PP**    {(map.accuracy*100):.2f}%\n> {map.score:,}    x{map.max_combo:,}/{beatmapMaxCombo:,}    "

                wsToSend += f"{wsMap_details}{wsScore_details}{score_hits} **{set_at}**\n"
                score_EmbedData = f"{map_details}  {score_details}  {score_hits}  **{set_at}**"

                embed.add_field(name = "", value = score_EmbedData, inline=False)

            if ctx.author.id == ui.ownId:
                ws.toSend_Message = wsToSend
                ws.send_response(ui.targetChannelId)

            embed.set_thumbnail(url = user_data.avatar_url)
            embed.set_author(url = f"https://osu.ppy.sh/users/{user_data.id}", name = title, icon_url = user_data.avatar_url)
            
            await self.bot.get_channel(Target_Channel_ID).send(embed=embed)

    @commands.command(name="osu")
    async def getProfile(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        Target_Channel_ID = ctx.channel.id
        content = ctx.message.content.strip()
        
        # Assign authorId based on rawmentions, if there are no mentions, authorId is the one who invoked the command instead.
        if ctx.message.raw_mentions:
            authorId = ctx.message.raw_mentions[0]
        else:
            authorId = ctx.author.id

        username, _, _, _ = cmdHandler.handle_osuprofile(ctx, "q.osu", ctx.message.raw_mentions)
        print("hello")

        if not username:
            username = db.associateUsernames(authorId)

            if username:
                user_data = api.user(username, mode="osu", key="username")

            else:
                if ctx.author.id == ui.ownId:
                    ws.toSend_Message = "You are not currently linked to an osu account. Please use `q.osulink <username>` and try again."
                    ws.send_response(ui.targetChannelId)
                await self.bot.get_channel(Target_Channel_ID).send("You are not currently linked to an osu account. Please use `q.osulink <username>` and try again.")
                return False

        else:
            try:
                user_data = api.user(username, mode="osu", key="username")
            except ValueError:
                await self.bot.get_channel(Target_Channel_ID).send(f"No user found")
                return False


        playtime = user_data.statistics.play_time
        playtime = int(round((playtime / 3600), 0))


        Title = f"Profile for {user_data.username}\n"
        description = f"> **Global Rank**: #{user_data.statistics.global_rank:,}\n> **Level**: {user_data.statistics.level.current} + {user_data.statistics.level.progress}%\n> **PP**: {user_data.statistics.pp:,.2f}\n> **Playcount**: {user_data.statistics.play_count:,} **Playtime**: {playtime:,} hrs\n"
        ranks = f"> **Ranks**: {self.gradeSSH}`{user_data.statistics.grade_counts.ssh}`{self.gradeSS}`{user_data.statistics.grade_counts.ss}`{self.gradeSH}`{user_data.statistics.grade_counts.sh}`{self.gradeS}`{user_data.statistics.grade_counts.s}`{self.gradeA}`{user_data.statistics.grade_counts.a}`"
        string = Title+description+ranks



        if ctx.author.id == ui.ownId:
            ws.toSend_Message = string
            ws.send_response(ui.targetChannelId)
        
        
        url = f"https://osu.ppy.sh/users/{user_data.id}"
        embed = Embed(
            description = f"**Global Rank**: #{user_data.statistics.global_rank:,}\n**Level**: {user_data.statistics.level.current} + {user_data.statistics.level.progress:.2f}%\n**PP**: {user_data.statistics.pp:,.2f}\n**Playcount**: {user_data.statistics.play_count:,} [{playtime:,} hrs]\n**Ranks**: {self.gradeSSH}`{user_data.statistics.grade_counts.ssh}`{self.gradeSS}`{user_data.statistics.grade_counts.ss}`{self.gradeSH}`{user_data.statistics.grade_counts.sh}`{self.gradeS}`{user_data.statistics.grade_counts.s}`{self.gradeA}`{user_data.statistics.grade_counts.a}`",
            color=Color.from_rgb(243, 205, 140)
        )

        embed.set_image(url = user_data.cover_url)
        embed.set_thumbnail(url = user_data.avatar_url)
        embed.set_author(url = url, name = f"Osu Profile for {user_data.username}", icon_url = user_data.avatar_url)

        await self.bot.get_channel(Target_Channel_ID).send(embed=embed)


    @commands.command(name="c")
    async def compareScores2(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        await self.compareScores(ctx, "q.c")
    
    @commands.command(name="compare")
    async def compareScores(self, ctx, command_substring=None):
        if ctx.guild.id == 1131290601233600662:
            return False
        Target_Channel_ID = ctx.channel.id
        if command_substring == "q.c": command_substring = "q.c"
        else: command_substring = "q.compare"

        
        if ctx.message.reference:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)

            if msg.embeds:
                import re
                embed = msg.embeds[0]
                if embed.fields[0].value.find("beatmapsets/") != -1:
                    map_url = embed.fields[0].value

                elif embed.url.find("beatmapsets/") != -1:
                    map_url = embed.url

                match = re.search(r'#osu/(\d+)', map_url)
                if match: 
                    beatmapId = int(match.group(1)) # The first group is the id.

                self.lastScoreSent = api.beatmap(beatmapId)

        
        content = ctx.message.content.strip()

        if ctx.message.raw_mentions:
            authorId = ctx.message.raw_mentions[0]
        else:
            authorId = ctx.author.id
        print('hello')
        # username, _, _, _ = cmdHandler.handle_osuprofile(content, command_substring, ctx.message.raw_mentions)
        username = False
        if not username:
            username = db.associateUsernames(authorId)

            if username:
                user_data = api.user(username, mode="osu", key="username")

            else:
                if ctx.author.id == ui.ownId:

                    ws.toSend_Message = "You are not currently linked to an osu account. Please use `q.osulink <username>` and try again."
                    ws.send_response(ui.targetChannelId)

                await self.bot.get_channel(Target_Channel_ID).send("You are not currently linked to an osu account. Please use `q.osulink <username>` and try again.")
                return False
            
        else:
            try:
                user_data = api.user(username, mode="osu", key="username")

            except ValueError:
                await self.bot.get_channel(Target_Channel_ID).send(f"No user found")
                return False


        if self.lastScoreSent != None:
            try: 
                print("userid: " + str(user_data.id))
                print(self.lastScoreSent.id)
                compareTo = api.beatmap_user_scores(self.lastScoreSent.id, user_data.id, mode="osu")
                print(compareTo)
                
                if len(compareTo) == 0:
                    raise ValueError
                
                beatmap = self.lastScoreSent
                beatmapset = beatmap.beatmapset()
                beatmapMaxCombo = getMap_Max_combo(beatmap)
                score_url = f"https://osu.ppy.sh/beatmapsets/{beatmapset.id}#osu/{beatmap.id}"

                version = beatmap.version

            except Exception as e:
                print(e.with_traceback(e.__traceback__)) 
                await self.bot.get_channel(Target_Channel_ID).send("User has no scores on this map.")
                return False
            
            try:
                title = f"Highscore on this map for {user_data.username}\n"

                wsToSend = title
            
                # Setting up embed
                embed = Embed(
                    url = score_url,
                    color=Color.from_rgb(243, 205, 140)
                )


                for index, score in enumerate(compareTo):
                    # Calculate score
                    ppCalculator.newScore(score, beatmap)
                    pp = f"{ppCalculator.computeValues():.2f}"

                    diffRating = f"{ppCalculator.beatmapDifficultyAttribute.attributes.star_rating:.2f}"
                    score_grade = self.handleGrade(score.rank)


                    map_details = f"**{beatmapset.title} [{version}]** {score.mods} [{diffRating}]★"
                    score_hits = f"[{score.statistics.count_300}/{score.statistics.count_100}/{score.statistics.count_50}/{score.statistics.count_miss}]\n"
                    score_details = f"**{score_grade[0]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "

                    set_at = self.createTimestamp(str(score.created_at))

                    wsMap_details = f"**{beatmapset.title} [{version}]** {score.mods} [{diffRating}★]\n"
                    wsScore_details = f"> **{score_grade[1]}**    **{pp}PP**    {(score.accuracy*100):.2f}%\n > {score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "

                    # wsToSend = title+wsMap_details+wsScore_details+score_hits+f"**{set_at}**"

                    if (beatmapMaxCombo - score.max_combo) <= (int(beatmapMaxCombo/100)):
                        score_details = f"**{score_grade[0]}**  {self.fc}    **{pp}PP**    {(score.accuracy*100):.2f}%\n{score.score:,}    x{score.max_combo:,}/{beatmapMaxCombo:,}    "
                    
                    embed.add_field(name = "", value = f"**{index+1}.** [{map_details}]({score_url})\n{score_details}{score_hits}**{set_at}**", inline = False)
                
                if len(compareTo) == 1:
                    embed.timestamp = score.created_at

                embed.set_image(url = beatmapset.covers.cover_2x)
                embed.set_thumbnail(url = user_data.avatar_url)
                embed.set_author(name = f"{title}", url = f"https://osu.ppy.sh/users/{user_data.id}", icon_url = user_data.avatar_url)
                embed.set_footer(text = "Played")


                # Checking author.id for WS.
                if ctx.author.id == ui.ownId:
                    ws.toSend_Message = wsToSend
                    ws.send_response(ui.targetChannelId)
                
                await self.bot.get_channel(Target_Channel_ID).send(embed=embed)
            except Exception as e:
                print(e.with_traceback(e.__traceback__)) 
        else:
            await self.bot.get_channel(Target_Channel_ID).send("No score is mentioned to compare.")


    @commands.command(name = "background")
    async def getBackground(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        Target_Channel_ID = ctx.channel.id
        import re
        try:
            if ctx.message.reference:
                msg = await ctx.fetch_message(ctx.message.reference.message_id)

            else:
                msg = ctx.message

            map_url = ctx.message.content.strip()

            match = re.search(r'#osu/(\d+)', map_url)
            match2 = re.search(r'(\d+)/(\d+)#', map_url)
            match3 = re.search(r'beatmapsets/(\d+)', map_url)

            if match:
                beatmapId = match.group(1)
                beatmap = api.beatmap(beatmapId)
            
            elif match2:
                beatmapId = match2.group(1)
                beatmap = api.beatmap(beatmapId)

            elif match3:
                beatmapsetId = match.group(1)

                # fetch all beatmaps in beatmapset
                beatmapset = api.beatmapset(beatmapsetId)
                beatmaps = beatmapset.beatmaps

                # choose beatmap with highest star rating
                beatmap = max(beatmaps, key=lambda b: b.difficulty_rating)
                beatmapId = beatmap.id


            elif msg.embeds:
                embed = msg.embeds[0]

                if embed.fields[0].value.find("beatmapsets/") != -1:
                    map_url = embed.fields[0].value

                elif embed.url.find("beatmapsets/") != -1:
                    map_url = embed.url

                match = re.search(r'#osu/(\d+)', map_url)

                if match: 
                    beatmapId = match.group(1) # The first group is the id.
                
                else:
                    await self.bot.get_channel(Target_Channel_ID).send("No beatmap id found")
                    return False
                
                beatmap = api.beatmap(beatmapId)
                beatmapset = beatmap.beatmapset()

            else:
                await self.bot.get_channel(Target_Channel_ID).send("No beatmap id found")
                return False
                

        except Exception as e:
            print(f"Error: {e.with_traceback(e.__traceback__)}")

        beatmapset = beatmap.beatmapset()
        
        card = beatmapset.covers.card_2x
        list = beatmapset.covers.list_2x
        slimcover = beatmapset.covers.slimcover_2x
        cover = beatmapset.covers.cover_2x


        embed = Embed()
        embed.set_author(name = "Background variants for this map")
        embed.add_field(name = "**Card**:", value = card, inline=False)
        embed.add_field(name = "**List**:", value = list, inline=False)
        embed.add_field(name = "**Slimcover**:", value = slimcover, inline=False)
        embed.add_field(name = "**Cover**:", value = cover, inline=False)

        embed.set_image(url = cover)

        await self.bot.get_channel(Target_Channel_ID).send(embed=embed)





        #newembed = Embed()
        #newembed.set_author(name = "This new embed", url = "https://google.com", icon_url=f"https://osu.ppy.sh/images/flags/{user_data.country_code}.png")
        #print(user_data.country_code)
        #await ctx.channel.send(f"Title: {embed.title}, URL: {embed.url}\nAuthor Name: {embed.author.name}, Icon_URL: {embed.author.icon_url}", embed=newembed)

    @commands.command(name = "bg")
    async def getBackground2(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        await self.getBackground(ctx)


    @commands.command(name = "ranking")
    async def getRanking(self, ctx):
        if ctx.guild.id == 1131290601233600662:
            return False
        Target_Channel_ID = ctx.channel.id
        command_substring = "q.ranking"

        content = ctx.message.content.strip()
        content = content.replace(command_substring, "")
        content = content.split()
        

        if len(content) == 1 and content[0].isdigit():
            if int(content[0]) < 0:
                return False
            
            page = content[0]

            ranking = api.ranking(mode="osu", type="performance", cursor=Cursor(page=page))

            string = ""

            for user in ranking.ranking:
                string += f"{user.user.username}: **{user.pp:.2f}PP** #{user.global_rank} Globally\n"

        await self.bot.get_channel(Target_Channel_ID).send(string)
    

    
    @commands.command(name = "m")
    async def getMap2(self, ctx):
        await self.getMap(ctx, "m")
        if ctx.guild.id == 1131290601233600662:
            return False

    @commands.command(name = "map")
    async def getMap(self, ctx, command_substring=None):
        if ctx.guild.id == 1131290601233600662:
            return False
        Target_Channel_ID = ctx.channel.id
        if command_substring == "q.m": command_substring = "q.m"
        else: command_substring = "q.map"
        import re
        try:
            if ctx.message.reference:
                msg = await ctx.fetch_message(ctx.message.reference.message_id)

            else:
                msg = ctx.message

            map_url = ctx.message.content.strip()

            split_mapUrl = map_url.split()

            mods = "NM"
            if len(split_mapUrl) == 2:
                if len(split_mapUrl[1]) < 10:
                    mods = split_mapUrl[1].upper()

            elif len(split_mapUrl) == 3:
                if len(split_mapUrl[2]) < 10:
                    mods = split_mapUrl[2].upper()
                if len(split_mapUrl[1]) < 10:
                    mods = split_mapUrl[1].upper()


            await self.bot.get_channel(Target_Channel_ID).send(f"Mods: {mods}")

            match = re.search(r'#osu/(\d+)', map_url)
            match2 = re.search(r'(\d+)/(\d+)#', map_url)
            match3 = re.search(r'beatmapsets/(\d+)', map_url)

            if match:
                beatmapId = match.group(1)
                beatmap = api.beatmap(beatmapId)
            
            elif match2:
                beatmapId = match2.group(1)
                beatmap = api.beatmap(beatmapId)

            elif match3:
                beatmapsetId = match.group(1)

                # fetch all beatmaps in beatmapset
                beatmapset = api.beatmapset(beatmapsetId)
                beatmaps = beatmapset.beatmaps

                # choose beatmap with highest star rating
                beatmap = max(beatmaps, key=lambda b: b.difficulty_rating)
                beatmapId = beatmap.id

            elif msg.embeds:
                embed = msg.embeds[0]

                if embed.fields[0].value.find("beatmapsets/") != -1:
                    map_url = embed.fields[0].value

                elif embed.url.find("beatmapsets/") != -1:
                    map_url = embed.url

                match = re.search(r'#osu/(\d+)', map_url)

                if match: 
                    beatmapId = match.group(1) # The first group is the id.
                
                else:
                    await self.bot.get_channel(Target_Channel_ID).send("No beatmap id found")
                    return False
                
                beatmap = api.beatmap(beatmapId)
                beatmapset = beatmap.beatmapset()

            else:
                await self.bot.get_channel(Target_Channel_ID).send("No beatmap id found")
                return False
                

        except Exception as e:
            print(f"Error: {e.with_traceback(e.__traceback__)}")

        try: 
            diffAttributes = api.beatmap_attributes(beatmapId, mods=mods, ruleset="osu")
            modified_od = round(diffAttributes.attributes.overall_difficulty, 0)
            modified_ar = round(diffAttributes.attributes.approach_rate, 1)

            beatmapset = beatmap.beatmapset()
            beatmapsetId = beatmapset.id
            cover = beatmapset.covers.cover_2x 

            embed = Embed(title=beatmapset.title, url=f'https://osu.ppy.sh/beatmapsets/{beatmapsetId}#osu/{beatmap.id}')

            embed.set_author(name = "Map details")
            embed.set_image(url = cover)

            # create embed with beatmap details
            embed.add_field(name='AR', value=modified_ar)
            embed.add_field(name='OD', value=modified_od)
            await self.bot.get_channel(Target_Channel_ID).send(embed=embed)

        except Exception as e:
            await self.bot.get_channel(Target_Channel_ID).send(e.with_traceback(e.__traceback__))
            return False