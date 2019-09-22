import urllib.request, json

baseurl = "https://www.openligadb.de/api/getmatchdata/" 
years = range(2016,2019)
days = range(1,35)
leagues = {
    "bl1" : "erste_bundesliga_"
    , "bl2" : "zweite_bundesliga_"
}
deli = ";"
teamnamename = "TeamName"
for leagueid, leaguename in leagues.items():
    for year in years:
        out = open(leaguename + str(year) + ".csv","w")
        out.write("spieltag"+deli+"spielminute"+deli+"heim"+deli+"strafstoss"+deli+"heimtore"+deli+"auswaertstore"+deli+"istheimtor"+deli+"istauswaertstor"+deli+"heimmannschaft"+deli+"auswaertsmannschaft\n")
        for day in days:
            with urllib.request.urlopen(baseurl + leagueid + "/" + str(year) + "/" + str(day)) as url:
                data = json.loads(url.read().decode())
                for match in data:
                    matchday = match['Group']['GroupOrderID']
                    team1 = match["Team1"][teamnamename]
                    team2 = match["Team2"][teamnamename]
                    team1sum = 0
                    team2sum = 0
                    for goal in match['Goals']:
                        minute = goal['MatchMinute']
                        if minute is None:
                            minute = -1
                        team1score = goal["ScoreTeam1"]
                        team2score = goal["ScoreTeam2"]
                        team1scored = team1score - team1sum > 0
                        team2scored = team2score - team2sum > 0
                        if(team1scored or team2scored):
                            home = 0
                            if(team1scored):
                                home = 1
                            strafstoss = 0
                            if(goal["IsPenalty"]):
                                strafstoss = 1
                            out.write(str(matchday) + deli + str(minute) + deli + str(home) + deli + str(strafstoss) + deli + str(team1score) + deli + str(team2score) + deli + str(team1scored) + deli + str(team2scored) + deli + str(team1) + deli + str(team2))  
                            out.write("\n")
                        team1sum = team1score
                        team2sum = team2score
        out.close()
