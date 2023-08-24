import requests
from ossapi import Ossapi
from ossapi import *
import discord
from discord.ext import commands
endpoint = "https://osu.ppy.sh/api/v2/"


client_id = 21156
client_secret = "JbqaosWSn9HeBgENlAuzYUWQSLLc48MKXbN7LbPe"

api = Ossapi(client_id, client_secret)
#api.user("GUNFSJGDSF45", mode="osu", key="username")
#print(api.user(31987131, mode="osu").username)
#print(api.beatmap(221777).id)
#
#print(api.beatmap(221777))
#user_data = api.user("OpBean", mode="osu", key="username")
#
#user_scores_data = api.user_scores(user_data.id, type="best", mode="osu", limit=5)
##print(user_scores_data)
#print(f"\n\n\n\n {api.beatmap(user_scores_data[0].id).max_combo} \n\n\n\n")

def getScore_max_combo(score):
    return api.beatmap(score.beatmap.id).max_combo

def getMap_Max_combo(beatmap):
    return api.beatmap(beatmap.id).max_combo

#ranking = api.ranking(mode="osu", type="performance", cursor=Cursor(page=199))
#
#for user in ranking.ranking:
#    print(f"{user.user.username}: **{user.pp:.2f}PP** #{user.global_rank} Globally")



#api.beatmapset(221777)
#print(api.beatmapset(1283387))
#att = api.score(221777)


def getPP():
    score = api.score(mode="osu", score_id=22649116355)
    
