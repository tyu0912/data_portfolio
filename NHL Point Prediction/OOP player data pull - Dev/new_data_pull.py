import requests
import json
import numpy as np
import sqlite3
import pandas as pd
from itertools import groupby
from collections import defaultdict


# This is made by Tennison Yu
# Still on agenda:
	# Pull metrics by game (will need a function to get game id)
	# Pull metrics by player name/team. Will need to work on the second init and also the query. 
	# Submission by lists? 
	# Set up some different breakouts and summaries. Will probably need a whole new class. 


class GameInfo:
	
	def __init__(self, gamedate, team1, team2):
		conn = sqlite3.connect('../game_data.sqlite')
		cur = conn.cursor()

		teams = team1 + "','" + team2

		query_string = "select * from original_players_table where date(gameDate) = '" + gamedate + "' and teamAbbrev in ('" + teams + "') and opponentTeamAbbrev in ('" + teams + "') " + " limit 1000"

		df = pd.read_sql(query_string, conn)

		self.data = (df.to_dict('records'))

	def getAllData(self):
		return self.data

	def Summary(self):

		A = defaultdict(dict)
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key]['goals'] = 0
			A[key]['assists'] = 0
			A[key]['team'] = ''
			for item in group:
				A[key]['goals'] += item['goals']
				A[key]['assists'] += item['assists']
				A[key]['team'] += item['teamAbbrev']
		
		return A

		
class nhl_player_metrics:

	def __init__(self, **kwargs):
		conn = sqlite3.connect('../game_data.sqlite')
		cur = conn.cursor()

		player_addon = ""
		team_addon = ""

		if not bool(kwargs):
			self.playerId = 8471675
			self.Team = 'TOR'
			player_addon = "and playerId = " + str(self.playerId)
			team_addon = "and teamAbbrev = " + str(self.Team)
		else:
			for k,v in kwargs.items():
				setattr(self, k, v)
				if k == 'playerId':
					if isinstance(v, (list,)):
						try:
							player_addon = "and playerId in ('" + "','".join(self.playerId) + "') "
						except:
							print('Are the ids a string?')
					else:
						player_addon = "and playerId = " + str(self.playerId)
				elif k == 'Team':
					if isinstance(v, (list,)):
						try:
							team_addon = "and teamAbbrev in ('" + "','".join(self.Team) + "') "
						except:
							print('Something went wrong with team input')
					else:
						team_addon = "and teamAbbrev = " + str(self.Team)
				else:
					continue
			
		query_string = 'select * from original_players_table where gameId like "%" ' + player_addon + team_addon + ' limit 1000'


		df = pd.read_sql(query_string, conn)

		self.data = (df.to_dict('records'))
		

	def getAllData(self):
		return self.data

	def test(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['goals']
		
		return A
		

	def getPlayerGoals(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['goals']
		
		return A
		
	def getPlayerAssists(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['assists']
		
		return A
		
	def getPlayerTOI(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['timeOnIcePerGame']
		
		return A

	def getPlayerBockedShots(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['blockedShots']
		
		return A

	def getPlayerShots(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['shots']
		
		return A

	def getPlayerHits(self):
		A = dict()
		for key, group in groupby(self.data, lambda item: item["playerName"]):
			A[key] = 0
			for item in group:
				A[key] += item['hits']
		
		return A

class nhl_references:

	def __init__(self):
		self.startyear = 2017
		self.endyear = 2018

	def getPlayerIdName(self):
		url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=false&reportName=skatersummary&cayenneExp=gameTypeId=2%20and%20seasonId%3E=20172018%20and%20seasonId%3C=20172018'
		resp = requests.get(url).text
		resp = json.loads(resp)
		data  = resp['data']
		
		name2id = {}
		id2name = {}
		
		for items in data:
			id2name[items['playerId']] = items['playerName']
			name2id[items['playerName']] = items['playerId']
		
		return name2id, id2name

#Test Cases

#nhl_player_metrics = nhl_player_metrics(playerId = [str(8478402),str(8471675)], Team = ['PIT','TOR'])
#nhl_player_metrics = nhl_player_metrics(playerId = [str(8478402),str(8471675)]) #, Team = ['PIT','TOR'])
#print(nhl_player_metrics.getPlayerGoals())

GameInfo = GameInfo(gamedate='2017-10-14',team1='TOR',team2='MTL')
print(GameInfo.Summary())
