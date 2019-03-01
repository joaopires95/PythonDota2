from multiprocessing import Process, Condition
from multiprocessing.managers import BaseManager

import re
import os
import sys
import shlex
import shutil
import subprocess
import signal
import time
import pyautogui
import select

class State(object):

	def __init__(self):

		self.loc_x = 0.1
		self.loc_y = 0.1
		self.hp = 1
		self.max_hp = 1
		self.mana = 1
		self.max_mana = 1
		self.time = 0.1
		self.n_queued_actions = 0
		self.neutrals = []
		self.lane_creeps = []
		self.enemy_heroes = []
		self.enemy_buildings = []
		self.time_of_day = 0.1
		self.tick = -1
		self.game_state = -1
		self.dire_win = False
		self.radiant_win = False
		self.user_over = False
		
		self.warn_user = False
		
		self.count = 1
        
	##################################SETTERS##################################
	
	def set_loc_x(self, value):
		self.loc_x = value
	
	
	def set_loc_y(self, value):
		self.loc_y = value
	
	
	def set_hp(self, value):
		self.hp = value
	
	
	def set_max_hp(self, value):
		self.max_hp = value
	
	
	def set_mana(self, value):
		self.mana = value
	
	
	def set_max_mana(self, value):
		self.max_mana = value
	
	
	def set_time(self, value):
		self.time = value
	
	
	def set_n_queued_actions(self, value):
		self.n_queued_actions = value
	
	
	def set_neutrals(self, value):
		self.neutrals = value
	
	def set_lane_creeps(self, value):
		self.lane_creeps = value
	
	
	def set_enemy_heroes(self, value):
		self.enemy_heroes = value
		
		
	def set_enemy_buildings(self, value):
		self.enemy_buildings = value
		
		
	def set_time_of_day(self, value):
		self.time_of_day = value
	
	
	def set_tick(self, value):
		self.tick = value
		
	def set_game_state(self, value):
		self.game_state = value
		
		
	def set_count(self, value):
		self.count = value
	
	
	def increment_count(self):
		self.count = self.count + 1
		
		
	def set_dire_win(self, value):
		self.dire_win = value
		
		
	def set_radiant_win(self, value):
		self.radiant_win = value
		
	def set_user_over(self, value):
		self.user_over = value
		
	def set_warn_user(self, value):
		self.warn_user = value

		
	##################################GETTERS##################################
	
	def get_loc_x(self):
		return self.loc_x
	
	
	def get_loc_y(self):
		return self.loc_y
	
	
	def get_hp(self):
		return self.hp
	
	
	def get_max_hp(self):
		return self.max_hp
	
	
	def get_mana(self):
		return self.mana
	
	
	def get_max_mana(self):
		return self.max_mana
	
	
	def get_time(self):
		return self.time
	
	
	def get_n_queued_actions(self):
		return self.n_queued_actions
	
	
	def get_neutrals(self):
		return self.neutrals
	
	
	def get_lane_creeps(self):
		return self.lane_creeps
	
	
	def get_enemy_heroes(self):
		return self.enemy_heroes
		
		
	def get_enemy_buildings(self):
		return self.enemy_buildings
		
		
	def get_time_of_day(self):
		return self.time_of_day
	
	
	def get_tick(self):
		return self.tick
		
	def get_game_state(self):
		return self.game_state


	def get_count(self):
		return self.count
	
		
	def get_dire_win(self):
		return self.dire_win
	
	
	def get_radiant_win(self):
		return self.radiant_win
		
	def get_user_over(self):
		return self.user_over
		
	def get_warn_user(self):
		return self.warn_user

	

class PythonDota2:

	pyautogui.PAUSE = 0.7
	pyautogui.FAILSAFE = True

	def __init__(self, team, hero, enemy, game_mode, n_episodes):
	
		"""
		team: select team for your hero
		hero: select your hero
		enemy: select the enemy for your hero
		game_mode: "all pick" or "1v1"
		n_episodes: the number of matches you want to play
		"""
	
		self.cond = Condition()
		
		self.install_dir = ""
		
		with open("install_dir.cfg") as file:  
			data = file.read() 
			self.install_dir = data.rstrip()
		
		# self.install_dir -> ~/.local/share/Steam/steamapps/common/dota 2 beta/
		
		self.logs_dir = self.install_dir+"/game/dota/"
		# ~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/

		self.bots_dir = self.logs_dir+"/scripts/vscripts/bots/"
		# ~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/scripts/vscripts/bots/
		
		self.tmp_dir = self.bots_dir+"/tmp/"
		# ~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/scripts/vscripts/bots/tmp/
		
		self.img_dir = self.bots_dir+"/scrsht/" 
		# ~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/scripts/vscripts/bots/scrsht/
		
		
		BaseManager.register('State', State)
		manager = BaseManager()
		manager.start()
		self.state = manager.State()
		
		self.team = team
		self.hero = hero
		self.enemy = enemy
		self.game_mode = game_mode.lower()
		self.n_episodes = n_episodes
		
		hero = self.hero.lower()
		team = self.team.lower()
		enemy = self.enemy.lower()

		
		self.neutrals_name_list = ["npc_dota_neutral_alpha_wolf",
			"npc_dota_neutral_centaur_khan",
			"npc_dota_neutral_centaur_outrunner",
			"npc_dota_neutral_dark_troll_warlord",
			"npc_dota_neutral_fel_beast",
			"npc_dota_neutral_ghost",
			"npc_dota_neutral_giant_wolf",
			"npc_dota_neutral_harpy_scout",
			"npc_dota_neutral_harpy_storm",
			"npc_dota_neutral_polar_furbolg_champion",
			"npc_dota_neutral_polar_furbolg_ursa_warrior",
			"npc_dota_neutral_dark_troll",
			"npc_dota_neutral_forest_troll_berserker",
			"npc_dota_neutral_forest_troll_high_priest",
			"npc_dota_neutral_kobold",
			"npc_dota_neutral_kobold_tunneler",
			"npc_dota_neutral_kobold_taskmaster",
			"npc_dota_neutral_mud_golem",
			"npc_dota_neutral_ogre_mauler",
			"npc_dota_neutral_ogre_magi",
			"npc_dota_neutral_satyr_trickster",
			"npc_dota_neutral_satyr_soulstealer",
			"npc_dota_neutral_satyr_hellcaller",
			"npc_dota_neutral_gnoll_assassin",
			"npc_dota_neutral_wildkin",
			"npc_dota_neutral_enraged_wildkin",
			"pc_dota_neutral_black_drake",
			"npc_dota_neutral_black_dragon",
			"npc_dota_neutral_blue_dragonspawn_sorcerer",
			"npc_dota_neutral_blue_dragonspawn_overseer",
			"pc_dota_neutral_granite_golem",
			"npc_dota_neutral_elder_jungle_stalker",
			"npc_dota_neutral_prowler_acolyte",
			"npc_dota_neutral_prowler_shaman",
			"npc_dota_neutral_rock_golem",
			"npc_dota_neutral_small_thunder_lizard",
			"npc_dota_neutral_jungle_stalker",
			"npc_dota_neutral_big_thunder_lizard",
			"npc_dota_roshan"]
			
		heroes = self.__get_hero_name()
		hero_to_pick = heroes[hero]
		enemy_to_pick = heroes[enemy]
		self.__edit_hero_selection(hero_to_pick, enemy_to_pick)
		
		
		p = Process(target=self.__read_log)
		p.daemon = True
		p.start()

		
		
	def __get_hero_name(self):
	
		heroes = {}
		hero_name = ""
		hero_code = ""
		counter = 0
		
		with open(self.bots_dir+'/heroes.txt','r') as f:
			for line in f:
				line = line.rstrip()
				if line.startswith('|-'):
					counter = 0
				else:
					counter += 1
					if counter == 1:
						hero_name = line.split('|')[1].lower()
					else:
						hero_code = line.split('|')[1]
						hero_code_list = hero_code.split()
						hero_code = hero_code_list[-1].lower()
					heroes[hero_name] = hero_code
		return heroes
		
	
	def __edit_hero_selection(self, hero_to_add, enemy_to_add):
	
		hero = self.hero.lower()
		team = self.team.lower()
		
		text = {}
		with open(self.bots_dir+"hero_selection.lua") as f: 
		# reads hero_selection.lua and keeps its text in memory
			for num, line in enumerate(f, 0):
				text[num] = line
				
		match = ""
		other = ""

		if team == 'radiant':
			match = "SelectHero( 2"
			other = "SelectHero( 7"
		
		elif team == 'dire':
			match = "SelectHero( 7"
			other = "SelectHero( 2"

		# if team radiant was chosen: changes pick 2 name with the name of the chosen hero 
		# and pick 7 name with the name of enemy hero
		
		# if team dire was chosen: changes pick 7 name with the name of the chosen hero 
		# and pick 2 name with the name of enemy hero
		
		# otherwise the picks [3:6] and [8:11] names with the name "sven"
		for number in text:
			line = text[number]
			
			if "SelectHero" in line:
				split = line.split()
				hero = split[2]
				parts = hero.split("_")
				hero_name = "_".join(parts[3:])
				
				if match in line: 
					new_hero_name = hero.replace(hero_name, hero_to_add+'"')
					
				elif other in line:

					new_hero_name = hero.replace(hero_name, enemy_to_add+'"')
				else:
					new_hero_name = hero.replace(hero_name, "sven"+'"')
					
				line = line.replace(hero, new_hero_name)
				text[number] = line	


		with open("hero_selection.lua", "w") as f: 
		# writes to hero_selection.lua the text kept in memory that was 
		# previously changed
			for number in text:
				f.write((text[number]))
				
	
	def __read_log(self):
		
		if self.n_episodes < 1:
			print("Number of Episodes must be 1 or more.")
			sys.exit()
		for i in range(self.n_episodes):
		
			if not os.path.isdir(self.tmp_dir):
				os.mkdir(self.tmp_dir)
				
			else:
				shutil.rmtree(self.tmp_dir)
				os.mkdir(self.tmp_dir)

			self.set_game_over(False)
		
			test = subprocess.Popen(["pidof","dota2"], stdout=subprocess.PIPE)
			pid = re.split("\n", test.communicate()[0].decode("utf-8"))[0] 
			# get Dota 2 pid
			
			file_name = "/console.log"
			
			new_path = self.logs_dir+file_name 
			# ~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/console.log
					
			while not os.path.exists(new_path):
			# if it's the first time that dota is opened with -condebug start 
			# option, the system waits for the main log file to be created
				pass
				
			files = os.listdir(self.logs_dir)
						
			file_list = []
			
			for f in files:
				if f.startswith("console."):
					part = f.split(".")
					if part[1] != "log":
						file_list.append(int(part[1]))

			if pid == "":
				file_name = "/console.log"
			else:
				file_no = str(max(file_list))
				file_name = "/console."+file_no+".log"
			
			new_path = self.logs_dir+file_name
			
			logfile = open(new_path,'r')

			# find the size of the file and move to the end
			st_results = os.stat(new_path)
			st_size = st_results[6]
			logfile.seek(st_size)
			
			no_new_logfile = True
			
			log_no = ""

			while no_new_logfile: # reads the first log file until DOTA 2 creates a new one, once a new match starts 
				where = logfile.tell()
				line = logfile.readline().rstrip()
				if not line:
					time.sleep(0.001)
					logfile.seek(where)
					
				else:
					line_split = line.split()
					
					if "Tearing" in line_split:
						log_no = line_split[-1]

					log_no = log_no[2:-1]
					if log_no != "":
						no_new_logfile = False
						
			logfile.close()
						
			new_path = self.logs_dir + '/console.'+log_no+'.log'
						
			while not os.path.isfile(new_path):
				pass		
			
			f = subprocess.Popen(['tail','-f',new_path], stdout=subprocess.PIPE,\
					stderr=subprocess.PIPE,	preexec_fn=os.setsid)
			p = select.poll()
			p.register(f.stdout)
			
			game_over = False
			unit_list = []
			tick = 0
			
			lines = []
			#loop_count = 0
			#total_time_elapsed = 0

			while not game_over and not self.state.get_user_over():
				#start_time = time.time()
				if p.poll(1):
					line = f.stdout.readline().decode("utf-8").rstrip()
					# print(line)

					if "[VScript] ;Vector" in line:
						line_split = line.split(";")

						
						with self.cond:
							try:
								self.state.set_loc_x(float(line_split[3][1:]))
								
								self.state.set_loc_y(float(line_split[4]))
								
								self.state.set_hp(int(line_split[6]))
								
								self.state.set_max_hp(int(line_split[7]))
								
								self.state.set_mana(int(line_split[8]))
								
								self.state.set_max_mana(int(line_split[9]))
								
								self.state.set_time(float(line_split[10]))
								
								self.state.set_n_queued_actions(int(line_split[11]))
								
								units_str = str(line_split[12])
								new_list = self.__get_units(units_str, unit_list)
								self.state.set_neutrals(new_list)
								
								self.state.set_time_of_day(float(line_split[13]))
									
								units_str = str(line_split[14])
								new_list = self.__get_units(units_str, unit_list)
								self.state.set_lane_creeps(new_list)
								
								units_str = str(line_split[15])
								new_list = self.__get_units(units_str, unit_list)
								self.state.set_enemy_heroes(new_list)
								
								units_str = str(line_split[16])
								new_list = self.__get_units(units_str, unit_list)
								self.state.set_enemy_buildings(new_list)
								
								self.state.set_tick(int(line_split[17]))
								
								self.state.set_game_state(int(line_split[18]))									
								
							except IndexError:
								pass
								#print("IndexError")
							except ValueError:
								pass
								#print("ValueError")

							finally:
								self.cond.notify_all()

					elif "npc_dota_badguys_fort destroyed" in line:
						print("Game Over, Radiant Win.")
						with self.cond:
							self.state.set_radiant_win(True)
						game_over = True

					elif "npc_dota_goodguys_fort destroyed" in line:
						print("Game Over, Dire Win.")
						with self.cond:
							self.state.set_dire_win(True)
						game_over = True
		
					else:
						pass
						
			os.killpg(os.getpgid(f.pid), signal.SIGTERM)

					
	def __get_units(self, units_str, unit_list):

		units_split = units_str.split() 
		try:
			if units_split:			
				indexes = []
				if "table:" in units_split:
					for i,n in enumerate(units_split):
						if n == "table:":
							indexes.append(i)
				
				unit_list = []
				for i in indexes:
					handle = units_split[i] + " " + units_split[i+1]
					name = units_split[i+2] # [3, 10, 17]
					hp = int(units_split[i+3]) # [4, 11, 18]
					maxHp = int(units_split[i+4]) # [5, 12, 19]
					mana = int(units_split[i+5]) # [6, 13, 20]
					maxMana = int(units_split[i+6]) # [7, 14, 21]
					attDmg = float(units_split[i+7]) # [8, 15, 22]
					armor = float(units_split[i+8]) # [9, 16, 23]
					distance = float(units_split[i+9][0:-1]) # [10, 17, 24]
					unit_list.append([handle,name,hp,maxHp,mana,maxMana,attDmg,armor,distance])
			else:
				unit_list = []
					
		except IndexError:
			unit_list = []
		except ValueError:
			unit_list = []
			
		finally:
			return unit_list
			
				
	def start_dota(self):
	
		test = subprocess.Popen(["pidof","dota2"], stdout=subprocess.PIPE)
		pid = re.split("\n", test.communicate()[0].decode("utf-8"))[0] 
		
		if pid == "":
			# if there is no pid, starts DOTA 2
			command = "steam steam://rungameid/570"
			args = shlex.split(command)
			p = subprocess.Popen(args)
		else:
			# if there is already a pid, changes focus to DOTA 2 window
			test = subprocess.Popen(["xdotool", "search", "--pid", pid], stdout=subprocess.PIPE)
			window_num = re.split("\n", test.communicate()[0].decode("utf-8"))[0] 
			
			subprocess.Popen(["xdotool", "windowactivate", window_num],\
			stdout=subprocess.PIPE).communicate()[0]



	def start_env_lobby(self):
		
		# checks whether there are or not files in /tmp directory
		# if there are files in /tmp directory, they are deleted
		# otherwise the program does nothing and continues
		
		if not os.path.isdir(self.tmp_dir):
			os.mkdir(self.tmp_dir)
			
		else:
			shutil.rmtree(self.tmp_dir)
			os.mkdir(self.tmp_dir)
				
		

		self.__set_count(1)
	
		hero = self.hero.lower()
		team = self.team.lower()

		self.close_env_lobby()
		
		pyautogui.typewrite("\\")
		pyautogui.typewrite("host_timescale 1.0")
		pyautogui.press('enter')
		pyautogui.typewrite("\\")

		locate_play_dota = None
		while locate_play_dota == None:
			locate_play_dota = pyautogui.locateOnScreen(self.img_dir+'play_dota.png')
		x, y = pyautogui.center(locate_play_dota)
		pyautogui.moveTo(x, y)
		pyautogui.click()
		
		locate_custom_lobby = None
		
		while locate_custom_lobby == None:
			locate_custom_lobby = pyautogui.locateOnScreen(self.img_dir+'custom_lobby.png')
		
		x, y = pyautogui.center(locate_custom_lobby)
		
		pyautogui.moveTo(x-75, y-45)
		pyautogui.click()
		
		locate_start_game = None
		
		while locate_start_game == None:
			locate_start_game = pyautogui.locateOnScreen(self.img_dir+'start_game.png')

			
		pyautogui.moveTo(1295, 575)	
		pyautogui.click()
		
		locate_lobby_settings = None
		
		while locate_lobby_settings == None:
			locate_lobby_settings = pyautogui.locateOnScreen(self.img_dir+'lobby_settings.png')
		
		pyautogui.moveTo(665, 165)	
		pyautogui.click()

		if self.game_mode == "all pick":
			pyautogui.moveTo(657, 193)	
			pyautogui.click()
			
		elif self.game_mode == "1v1":
			pyautogui.moveTo(650, 462)	
			pyautogui.click()
			
		else:
			print("You have to choose a correct game mode!")
			
		pyautogui.moveTo(913, 672)	
		pyautogui.click()
		
		locate_start_game = None
		
		while locate_start_game == None:
			locate_start_game = pyautogui.locateOnScreen(self.img_dir+'start_game.png')
			
		if team == 'radiant':
			pyautogui.moveTo(1071, 318)
		
		elif team == 'dire':
			pyautogui.moveTo(1309, 318)
		
		else:
			print("You have to choose 'radiant' or 'dire'!")
			self.close_dota()
			return
		
		pyautogui.click()
		
		pyautogui.moveTo(1208, 741)
		pyautogui.click()
		
		if team == 'radiant':
			locate_strategy_map = None

			while locate_strategy_map == None:
				locate_strategy_map = pyautogui.locateOnScreen(self.img_dir+'strategy_map_radiant.png')
		
		elif team == 'dire':
			locate_strategy_map = None

			while locate_strategy_map == None:
				locate_strategy_map = pyautogui.locateOnScreen(self.img_dir+'strategy_map_dire.png')
			
		pyautogui.typewrite("\\")
		pyautogui.typewrite("host_timescale 100.0")
		pyautogui.press('enter')

		time.sleep(1.1)

		pyautogui.typewrite("host_timescale 1")
		pyautogui.press('enter')
		pyautogui.typewrite("\\")
		locate_color = None
		
		#while locate_color == None:
			#locate_color = pyautogui.locateOnScreen(self.img_dir+'color_dota.png')
			
				
		"""if team == 'radiant':
			pyautogui.moveTo(405, 15)
			
		elif team == 'dire':
			pyautogui.moveTo(775,15)
		
		pyautogui.click()
		pyautogui.moveTo(485,720)
		pyautogui.doubleClick()"""
		
	
	def close_env_lobby(self):
	
		locate_color = None
		locate_play_dota = None
		locate_leave_game = None

		while locate_color == None and locate_play_dota == None and locate_leave_game == None:
			#pyautogui.moveTo(1200, 730)
			locate_color = pyautogui.locateOnScreen(self.img_dir+'color_dota.png')
			locate_play_dota = pyautogui.locateOnScreen(self.img_dir+'play_dota.png')
			locate_leave_game = pyautogui.locateOnScreen(self.img_dir+'leave_game.png')
			
		if locate_color != None:
			
			pyautogui.typewrite("\\")
			pyautogui.typewrite("host_timescale 1.0")
			pyautogui.press('enter')
			pyautogui.typewrite("\\")
		
			pyautogui.typewrite("\\")
			pyautogui.typewrite("disconnect")
			pyautogui.press('enter')
			pyautogui.typewrite("\\")
			
			locate_leave_game_b = None

			while locate_leave_game_b == None:
				locate_leave_game_b = pyautogui.locateOnScreen(self.img_dir+'leave_game.png')
			
			x, y = pyautogui.center(locate_leave_game_b)
			pyautogui.moveTo(x, y)
			pyautogui.click()

			pyautogui.moveTo(618, 430)
			pyautogui.click()
			
		if locate_play_dota != None:
			pass # No environment to be closed
			
		if locate_leave_game != None:
		
			pyautogui.typewrite("\\")
			pyautogui.typewrite("host_timescale 1.0")
			pyautogui.press('enter')
			pyautogui.typewrite("\\")
			
			x, y = pyautogui.center(locate_leave_game)
			pyautogui.moveTo(x, y)
			pyautogui.click()
			
			pyautogui.moveTo(618, 430)
			pyautogui.click()


	def close_dota(self):
	
		test = subprocess.Popen(["pidof","dota2"], stdout=subprocess.PIPE)
		pid = re.split("\n", test.communicate()[0].decode("utf-8"))[0]

		if pid == "": 
			pass
		else: 
			subprocess.Popen(["kill", "-KILL", pid],\
			stdout=subprocess.PIPE).communicate()[0]
	
	
	
	# actions useable to control the hero in game, just like the ones present in the DOTA 2 bot API
	
	# more actions can be added easily using function __send_command(self, command) as long as the
	# command (string) can be interpreted in the hero's Lua script
	
	def Action_MoveToLocation(self, x, y):
	
		command = "MoveToLocation " + str(x) + " " + str(y)
		self.__send_command(command)
		
		
	# MoveDirectly #############################################################
	def Action_MoveDirectly(self, x, y):
	
		command = "Action_MoveDirectly " + str(x) + " " + str(y)
		self.__send_command(command)	
		
		
	def ActionPush_MoveDirectly(self, x, y):
	
		command = "ActionPush_MoveDirectly " + str(x) + " " + str(y)
		self.__send_command(command)
		
		
	def ActionQueue_MoveDirectly(self, x, y):
	
		command = "ActionQueue_MoveDirectly " + str(x) + " " + str(y)
		self.__send_command(command)
		
	
	# AttackUnit ###############################################################
	def Action_AttackUnit(self, handle, once):
			
		command = "Action_AttackUnit " + str(handle) + " " + str(once)
		self.__send_command(command)
		
	
	def ActionPush_AttackUnit(self, handle, once):		
		
		command = "ActionPush_AttackUnit " + str(handle) + " " + str(once)
		self.__send_command(command)
		
	
	def ActionQueue_AttackUnit(self, handle, once):
		
		command = "ActionQueue_AttackUnit " + str(handle) + " " + str(once)
		self.__send_command(command)
		
	
	def Action_ClearActions(self, stop):
		command = "Action_ClearActions " + str(stop)
		self.__send_command(command)
		
		
	def Action_Delay(self, delay):
		command = "Action_Delay " + str(delay)
		self.__send_command(command)


	def ActionPush_Delay(self, delay):
		command = "ActionPush_Delay " + str(delay)
		self.__send_command(command)


	def ActionQueue_Delay(self, delay):
		command = "ActionQueue_Delay " + str(delay)
		self.__send_command(command)
		
	
	def __send_command(self, command):

		path = self.tmp_dir+str(self.__count())+".lua"
		
		with self.cond:
			f = open(path,"w") 
			# creates file "*.lua" that will be loaded by the bot script
			f.write('return ' +  '"' + command + '"')
			f.close()
			self.state.increment_count()		
	
	
	def loc_x(self):
		return self.state.get_loc_x()
	
	
	def loc_y(self):
		return self.state.get_loc_y()
		
		
	def hp(self):
		return self.state.get_hp()
	
	
	def max_hp(self):
		return self.state.get_max_hp()
	
	
	def mana(self):
		return self.state.get_mana()
	
	
	def max_mana(self):
		return self.state.get_max_mana()
	
	
	def time(self):
		#with self.cond:
		return self.state.get_time()
	
	
	def n_queued_actions(self):
		#with self.cond:
		return self.state.get_n_queued_actions()
	
	
	def neutrals(self):
		return self.state.get_neutrals()
	
	
	def lane_creeps(self):
		return self.state.get_lane_creeps()
	
	
	def enemy_heroes(self):
		return self.state.get_enemy_heroes()
	
	
	def enemy_buildings(self):
		return self.state.get_enemy_buildings()
	
	
	def time_of_day(self):
		return self.state.get_time_of_day()
	
	
	def tick(self):
		return self.state.get_tick()
		
	def __count(self):
		return self.state.get_count()
			
			
	def dire_win(self):
		return self.state.get_dire_win()
			
			
	def radiant_win(self):
		return self.state.get_radiant_win()
			
	def game_state(self):
		return self.state.get_game_state()
		
	def set_game_over(self, value):
		self.state.set_user_over(value)
		
	def __set_count(self, value):
		self.state.set_count(value)
		
	def set_warn_user(self, value):
		self.state.set_warn_user(value)
		
	def get_warn_user(self):
		return self.state.get_warn_user()
			
	def wait_for_new_tick(self):
		with self.cond:
			self.cond.wait()


