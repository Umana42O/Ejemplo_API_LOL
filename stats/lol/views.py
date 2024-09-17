# Create your views here.
from django.shortcuts import render
import requests
import datetime
import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse

payload = {"api_key":"RGAPI-451938a3-feda-4286-acf2-bab4ddabba18"}

class Participant:
    def __init__(self, championName,gameName, tagLine, puuid ,spells, level, role, items, kills, deaths, assists, win):
        self.championName = championName
        self.gameName = gameName
        self.tagLine = tagLine
        self.puuid = puuid
        self.spells = spells
        self.level = level
        self.role = role
        self.items = items
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.win = win
        self.KDA = round((kills + assists)/deaths,2) if deaths > 0 else kills + assists

    def __repr__(self):
        return (f"Participants(championName={self.championName}, spells={self.spells}, "
                f"level={self.level}, lane={self.lane}, items={self.items}, "
                f"kills={self.kills}, deaths={self.deaths}, assists={self.assists})")

def index(request):
    return render(request,"lol/index.html")
def partidas(request):
    match_important_info = {
                "gameMode" : 0,
                "duration": 0,
                "isVictory": 0,
              "participants" : [
                ],
              }
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            gameName = data["gameName"]
            tagLine = data["tag"]
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=400)
        r = requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}',params=payload)
        if r.status_code != 200:
            return JsonResponse({"msg": "Summoner not found"}, status=404)
        result = r.json()
        puuid = result["puuid"] 
        summonerData = requests.get(f"https://la1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}",params=payload)
        print(summonerData.json())
        payload_matches = {
            "api_key" : payload["api_key"],
            "start": 0,
            "count":5
        }
        #Matches Logic
        matches_id = (requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids", params=payload_matches)).json()
        for i in matches_id:
            match = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}",params=payload).json()
            match_important_info["gameMode"] = match["info"]["gameMode"]
            match_important_info["duration"] = str(datetime.timedelta(seconds=match["info"]["gameDuration"]))
            for i in match["info"]["participants"]:
                a = Participant(i["championName"],i["riotIdGameName"], i["riotIdTagline"], i["puuid"], [i["summoner1Id"],i["summoner2Id"]], i["champLevel"],i["individualPosition"],[i["item1"],i["item2"],i["item3"],i["item4"],i["item5"],i["item6"]],i["kills"], i["deaths"], i["assists"],i["win"])
                if i["puuid"] == puuid:
                    match_important_info["isVictory"] = i["win"]
                    match_important_info["me"] = a.__dict__
                match_important_info["participants"].append(a.__dict__)
        #Mastery Logic
        return JsonResponse(match_important_info)
    else:
        return HttpResponse("Method post only")