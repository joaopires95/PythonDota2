import math
import time
from PythonDota2 import *

#print(bot.team, bot.hero, bot.enemy)
n_episodes = 2
bot = PythonDota2("dire", "ursa", "templar assassin", "all pick", n_episodes)

for i in range(n_episodes):

	bot.start_dota()
	bot.start_env_lobby()
	
	not_done = True
	not_waiting = True
	not_stacked = True
	not_attacked = True
	
	while bot.game_state() != 4:
		pass # wait for match delay time start

	while not bot.dire_win() and not bot.radiant_win() and bot.time() < 300: # 120: #300
		bot.wait_for_new_tick() # this function should be used to synchronize every iteration in this loop with each new state of a match
		# it is also very important to use this function so that your PC doesn't waste redundant CPU cycles   
		
		#print(bot.loc_x(), bot.loc_y(), bot.hp(), bot.max_hp(), bot.mana(), bot.max_mana(), bot.time(), bot.n_queued_actions(), bot.neutrals(), bot.lane_creeps(), bot.enemy_heroes(), bot.enemy_buildings(), bot.time_of_day(), bot.tick())
		hpPercentage = bot.hp()/bot.max_hp()
		
		seconds, minutes = math.modf(bot.time()/60)
		seconds = seconds * 60
	


		#if bot.neutrals():
		#	print(bot.neutrals())
			
		#if bot.enemy_heroes():
		#	print(bot.enemy_heroes())
		
		#if bot.hp() > 0:
			#bot.Action_MoveToLocation(0, 0)
		if not_waiting:
			#bot.ActionQueue_Delay(1)
			bot.ActionQueue_MoveDirectly(1000, 3950)
			not_waiting = False
			
		if 50 < seconds < 51:
			not_stacked = True
			not_attacked = True
			
		if seconds > 52.2 and minutes > 0 and not_stacked and 0.25 < bot.time_of_day() < 0.75: # day
			bot.ActionQueue_MoveDirectly(1300, 3400) # aggro
			bot.ActionQueue_MoveDirectly(500, 5000) # run away
			bot.ActionQueue_MoveDirectly(1000, 3950)
			not_stacked = False
		
		elif seconds > 52.5 and minutes > 0 and not_stacked and not_attacked and (bot.time_of_day() > 0.75 or bot.time_of_day() < 0.25): # night
			if bot.neutrals():
				for neutral in bot.neutrals():
					handle = neutral[0]
					name = neutral[1]
					if name in bot.neutrals_name_list and not_attacked:
						bot.ActionQueue_AttackUnit(handle, True) # hit once
						bot.ActionQueue_MoveDirectly(500, 5000) # run away
						bot.ActionQueue_MoveDirectly(1000, 3950)
						not_stacked = False
						not_attacked = False
						break
						
		"""
		if 0.0 < hpPercentage < 0.5:
			print("DYING!")
		if bot.hp() == 0:
			print("Bot is dead!")"""
	bot.set_game_over(True)

bot.close_env_lobby()


