import requests #pip install requests //to install requests module
import re
import os
from time import sleep
import json


def popup(title, message):
    os.system('cls')
    print("\n")
    print("------------------------------------------------------------------------------")
    print("\n%s \n%s  " % (title, message))
    print("------------------------------------------------------------------------------")
    print("\n")
    return


def getscore():
	url = "http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/match/656493.json" #change json file here
	r = requests.get(url)
	while r.status_code is not 200:
		r = requests.get(url)
	data = json.loads(r.text)
	player_status = data['match']['current_summary'].strip()
	team1_name = data['other_scores']['international'][0]['team1_name'].strip()
	team1_score = data['other_scores']['international'][0]['team1_desc'].replace('&nbsp;ov',' ov').strip()
	team2_name = data['other_scores']['international'][0]['team2_name'].strip()
	team2_score = data['other_scores']['international'][0]['team2_desc'].replace('&nbsp;ov',' ov').strip()
	if not team1_score:
		team1_score = 'Yet to bat'
	if not team2_score:
		team2_score = 'Yet to bat'
	score = str(team1_name) + ' : ' + str(team1_score) + '\n\n' + str(team2_name) + ' : ' + str(team2_score)
	player_status = re.sub(r'.*ov,','', str(player_status))
	score = score + '\nPlayer status: ' + player_status
	popup("Score Board:-", score)
	sleep(20) #change time here



if __name__ == "__main__":
	while True:
		getscore()
