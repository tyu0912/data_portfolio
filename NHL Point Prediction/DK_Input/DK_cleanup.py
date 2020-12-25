IN = open('DKSalaries.csv','r')
OUT1 = open('players_playing.txt','w')
map = open('team_map.txt','r').read()
OUT2 = open('goalies_playing.txt','w')
#OUT2 = open('clean_data\games_playing.txt','w')

counter = 0
games_list = []
name_change = map.splitlines()


for x in IN:
	if counter <= 7:
		pass
	else:
		player_data = (x[10:])
		player_data = player_data.split(',')
		
		player_name = player_data[2]
		player_DKid = player_data[3]
		player_position = player_data[4]

		if player_position != 'G':
			player_position = player_position[:player_position.find('/')].strip()

		player_DKvalue = player_data[5]
		game = player_data[6]
		player_team = player_data[7].strip()
		player_points = player_data[8].strip()

		game = game[:game.find(' ')]
		match = game.split('@')
		
		for teams in match:	
			if player_team != teams:
				opponent = teams
				for x in name_change:
					y = x.split(',')
					if opponent == y[0]:
						opponent = y[1]
					else:
						pass
			else:
				for x in name_change:
					y = x.split(',')
					if player_team == y[0]:
						player_team = y[1]
					else:
						pass

		if player_position != 'G':
			OUT1.write(player_name + '\t' + player_DKid + '\t' + player_position + '\t' + player_DKvalue + '\t' + game + '\t' + player_team + '\t' + opponent + '\t' + player_points + '\n')
		else:
			OUT2.write(player_name + '\t' + player_DKid + '\t' + player_position + '\t' + player_DKvalue + '\t' + game + '\t' + player_team + '\t' + opponent + '\t' + player_points + '\n')
		
		games_list.append(game)

	
	counter = counter + 1

games_list2 = list(set(games_list))

#for game in games_list2:
#	OUT2.write(game[:game.find(' ')] + '\n')