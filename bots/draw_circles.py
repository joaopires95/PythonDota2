#import pythondota2
import time
from PythonDota2 import *

n_episodes = 1
bot = PythonDota2("dire", "ursa", "templar assassin", "all pick", n_episodes)

print(bot.team, bot.hero)

bot.start_dota()

for i in range(n_episodes):
	bot.start_env_lobby()
	
	while bot.game_state() != 4:
		pass # wait for match delay time start
		

	#--bot.Action_MoveToLocation(0, 0) #-6000.0 -5300.0

	not_done = True

	while True:
		bot.wait_for_new_tick()
		#pass
		#time.sleep(0.5)
		hpPercentage = bot.hp()/bot.max_hp()
		
		if not_done and bot.n_queued_actions() < 1:
				bot.ActionPush_MoveDirectly(0, 0)
				bot.ActionPush_MoveDirectly(400, 0) # 		#4
				bot.ActionPush_MoveDirectly(400, 400) #		#3
				bot.ActionPush_MoveDirectly(0, 400) # 		#2
				bot.ActionPush_MoveDirectly(0, 0) # 		#1
							
				bot.ActionQueue_MoveDirectly(3000, 3000);#10
				bot.ActionQueue_MoveDirectly(3400, 3400);#9
				bot.ActionQueue_MoveDirectly(3900, 2900);#8
				bot.ActionQueue_MoveDirectly(3400, 2600);#7
				bot.ActionQueue_MoveDirectly(3000, 3000);#6
				not_done = False
		elif not not_done and bot.n_queued_actions() == 0:
			not_done = True
			
		elif not not_done and bot.n_queued_actions() > 0:
			not_done = False
			
		

			
		
		#print(bot.loc_x(), bot.loc_y(), bot.hp(), bot.max_hp(), bot.mana(), bot.max_mana(), bot.time(), bot.n_queued_actions(), bot.neutrals(), bot.lane_creeps(), bot.enemy_heroes(), bot.enemy_buildings(), bot.time_of_day(), bot.tick())
		
		"""if 0.0 < hpPercentage < 0.5:
			print("DYING!")
		if bot.hp() == 0:
			print("Bot is dead!")"""
		#print()



