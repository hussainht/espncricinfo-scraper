import urllib, json
import pandas
import os

matchdata = pandas.read_csv("Match_IDS.csv")
scraped_data = []


for match in matchdata['matchid']:
    try:
        match = str(match)

        exists = os.path.isfile('data/' + match + '.csv')
        if exists:
            print(match + " was already processed.")
            continue
        else:
            print("MATCH " + match + " started.")

        scraped_data = []
        for period in range (1,3):
            pagenum = 1
            url = "http://site.web.api.espn.com/apis/site/v2/sports/cricket/8037/playbyplay?contentorigin=espn&event=" + match + "&page=" + str(pagenum) + "&period=" + str(period) + "&section=cricinfo"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            while len(data['commentary']['items'])>0:
                for item in data['commentary']['items']:
                    try:
                        full_text = item['text'].encode('utf-8')
                    except KeyError:
                        full_text = None

                    try:
                        short_text = item['shortText'].encode('utf-8')
                    except KeyError:
                        short_text = None

                    try:
                        batsman = item['batsman']['athlete']['name']
                    except:
                        batsman = None

                    try:
                        batsmantot_runs = item['batsman']['totalRuns']
                    except:
                        batsmantot_runs = None

                    try:
                        balls_faced = item['batsman']['faced']
                    except:
                        balls_faced = None

                    try:
                        balls = item['innings']['ballLimit'] - item['innings']['remainingBalls']
                    except:
                        balls = None

                    try:
                        otherbatsman = item['otherBatsman']['athlete']['name']
                    except KeyError:
                        otherbatsman = None

                    try:
                        bowler = item['bowler']['athlete']['name']
                    except:
                        bowler = None

                    try:
                        wicket_bool = item['dismissal']['dismissal']
                    except:
                        wicket_bool = None


                    try:
                        dismissal_type = item['dismissal']['type']
                    except:
                        dismissal_type = None

                    try:
                        dismissal_mins = item['dismissal']['minutes']
                    except:
                        dismissal_mins = None

                    try:
                        score = item['scoreValue']
                    except:
                        score = None

                    try:
                        batting_team = item['team']['name']
                    except:
                        batting_team = None
                    try:
                        bowling_team = item['bowler']['team']['name']
                    except:
                        bowling_team = None


                    try:
                        speedkph = item['speedKPH']
                    except KeyError:
                        speedkph = None

                    try:
                        bowler_conceded = item['bowler']['conceded']
                    except:
                        bowler_conceded = None

                    try:
                        bowler_maidens = item['bowler']['maidens']
                    except:
                        bowler_maidens = None

                    try:
                        bowler_balls = item['bowler']['balls']
                    except:
                        bowler_balls = None


                    try:
                        bowler_wickets = item['bowler']['wickets']
                    except:
                        bowler_wickets = None

                    try:
                        homescore = item['homeScore']
                    except:
                        homescore = None

                    try:
                        awayscore = item['awayScore']
                    except:
                        awayscore = None

                    scraped_data.append({"event_id":match,"full_text": full_text,"short_text":short_text,"homescore":("'" + str(homescore)),"batsman": batsman, "batsmantot_runs": batsmantot_runs,
                                         "balls_faced": balls_faced, "otherbatsman": otherbatsman, "balls": balls,
                                         "bowler": bowler, "wicket_bool": wicket_bool, "dismissal_type": dismissal_type,
                                         "score": score,"batting_team":batting_team,"bowling_team":bowling_team,"speedkph":speedkph,
                                         "dismissal_mins":dismissal_mins,"bowler_conceded":bowler_conceded,"bowler_maidens":bowler_maidens,
                                         "bowler_balls":bowler_balls,"bowler_wickets":bowler_wickets,"awayScore":("'" + str(awayscore))})

                pagenum +=1
                url = "http://site.web.api.espn.com/apis/site/v2/sports/cricket/8037/playbyplay?contentorigin=espn&event=" + match + "&page=" + str(pagenum) + "&period=" + str(period) + "&section=cricinfo"
                response = urllib.urlopen(url)
                data = json.loads(response.read())

        df = pandas.DataFrame(scraped_data)
        df.to_csv("data/" + str(match)+".csv")
    except:
        match = str(match)
        print("MATCH " + match + " failed.")