import requests
from ossapi import Ossapi
from ossapi import *

endpoint = "https://osu.ppy.sh/api/v2/"


client_id = 21156
client_secret = "JbqaosWSn9HeBgENlAuzYUWQSLLc48MKXbN7LbPe"

api = Ossapi(client_id, client_secret)

print(api.user(31987131, mode="osu").username)
print(api.beatmap(221777).id)

print(api.beatmap(221777).max_combo)


#user_data = api.user("OpBean", mode="osu", key="username")
#
#user_scores_data = api.user_scores(user_data.id, type="best", mode="osu", limit=5)
##print(user_scores_data)
#print(f"\n\n\n\n {api.beatmap(user_scores_data[0].id).max_combo} \n\n\n\n")

def getScore_max_combo(score):
    return api.beatmap(score.beatmap.id).max_combo

def handleGrade(grade):
    rank = grade

    if rank == grade.S:
        return "S"
    
    if rank == grade.A:
        return "A"
    
    if rank == grade.B:
        return "B"
    
    if rank == grade.C:
        return "C"
    
    if rank == grade.D:
        return "D"
    
    if rank == grade.F:
        return "F"
    
    if rank == grade.SH:
        return "SH"
    
    if rank == grade.SSH:
        return "SSH"