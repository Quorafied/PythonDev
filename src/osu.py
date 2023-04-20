import requests
from ossapi import Ossapi
from ossapi import *

endpoint = "https://osu.ppy.sh/api/v2/"


client_id = 21156
client_secret = "JbqaosWSn9HeBgENlAuzYUWQSLLc48MKXbN7LbPe"

api = Ossapi(client_id, client_secret)

print(api.user(31987131, mode="osu").username)
print(api.beatmap(221777).id)




