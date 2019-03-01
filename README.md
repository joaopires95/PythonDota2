# PythonDota2
Python3 API for DOTA 2 for AI development. 

This is PythonDota2 and it's a Python3 API developed for Ubuntu that can be used to control a hero through Python, just like the way you could control it through the DOTA 2 Bot API. This project was developed for my Master's Degree thesis and it can (and should!) be used for AI development for DOTA 2 heroes. Or you can just use it to mess around with a DOTA 2 hero through Python. 

The API receives data (state of each match) from matches where the hero to be controlled is in, and enables control of the hero through functions that write strings in LUA files (e.g. "ActionPush_MoveDirectly 0 0") that are interpreted by the hero's LUA file, using the respective DOTA 2 Bot API function in game (ActionPush_MoveDirectly(Vector(0, 0, 0))).

The API consists basically of a Python module named "PythonDota2.py" and a LUA template script for the hero to be controlled. The hero I used throughout the development of this project was Ursa so the LUA script for the hero is named "bot_ursa.lua", but you can copy the contents of it and copy them to a file named "bot_jakiro.lua" if you wish to control Jakiro through Python, or any other hero for that matter!

There are some other files present in this project such as:
- "bot_sven.lua" - that has a dummy function so that all the Svens in the lobby, that are not to be controlled, stay idle. 
- "bot_templar_assassin.lua" - that has a function that positions the opponent's Templar Assassin just a little bit North of the Radiant Middle Tier 1 Tower. If you wish to only have a Ursa in game to be controlled versus no adversaries you can erase the contents of the function "Think()" present on "bot_templar_assassin.lua". If you wish to have a Ursa versus an opponent like Templar Assassin you can just erase the file "bot_templar_assassin.lua" and the default DOTA 2 Templar Assassin's AI will take charge.
- "draw_circles.py" - the first of the two Python scripts I developed to ilustrate what this API can do. In this case, the hero Ursa will go near the Radiant Middle Tier 1 Tower and start to walk in circles.
- "heroes.txt" - that contains all the DOTA 2 heroes's names.
- "hero_selection.lua" - that will be edited by "PythonDota2.py" when a match starts, so that Ursa and Templar Assassin can be assigned to the respective teams, just the way you selected.
- "install_dir.cfg" - a file that you will edit with the path for the DOTA 2 installation directory in your PC. The path in my computer is "/home/joaop/.local/share/Steam/steamapps/common/dota 2 beta/".
- "stack_dire.py" - the other Python script I developed to demonstrate how this API can be used for programming a hard-coded policy that controls the hero in a way that he can keep stacking one of the hard camps present in the Dire jungle, based on the match state information retrieved.

The other files can be erased if you wish, but I'd keep at least "item_purchase_generic.lua" to prevent the idle Svens present in the match from buying items randomly.

I put all these files in the "bots" directory, present in "/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/scripts/vscripts/bots". 
You don't need to have your developed Python scripts in this directory.
If you wish to have the module "PythonDota2.py" in another directory, be sure that "install_dir.cfg" is present in that same directory, because this file's contents will be read by "PythonDota2.py".

In addition to these files, there are also two directories present in the "bots" directory:
- "scrsht" - that contains pieces of screenshots I took from DOTA 2 that will be recognised by "PythonDota2.py", in order to create local matches through automation via the game's GUI.
- "tmp" - that will contain the files written by "PythonDota2.py", when controls are sent to the hero. These files are the ones that will be interpreted by the hero's LUA file, so that the controls, sent by the module, result in actions taken by the hero.


So, here's what you'll need to do in order to use this API:

1. Have a Linux Ubuntu OS. I can't guarantee that this API will work on other Linux distributions, but feel free to try it out and tell me after how it went!

2. Have Python3 installed in your OS.

3. Have Steam and DOTA 2 installed in your OS.

4. Have an Internet connection so you can allow the creation of local matches in lobbies through the GUI automation present in this API. The lobbies are local but they can only be created if there is a connection to the Internet so each match has ,a unique ID.

5. Go to DOTA 2 Properties in Steam.
   1. In the tab "GENERAL" select "SET LAUNCH OPTIONS" and paste "-console -condebug".
   2. Click "OK".
   3. Close DOTA 2 Properties.

6. Go to  "~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/cfg/".
   1. Create a file named "autoexec.cfg" and add:
      1. "log_verbosity SteamNetSockets off | grep %" to the first line. 
      2. "sv_cheats 1" to the second line.
   2. Save and exit.

7. Start DOTA 2.
   1. Select DOTA 2 Settings (top left-hand corner).
      1. Select the tab "VIDEO".
      2. Under "RESOLUTION" select the option "Use my monitor's current resolution".
      3. Under "OPTIONS" select the option "OpenGL (-gl)" for rendering API.
      4. Under "RENDERING" select "Use basic settings" and select "Fastest".
      5. Under "RESOLUTION" click "APPLY" and exit DOTA 2 Settings.
   2. Select PLAY DOTA (bottom right-hand corner).
      1. Under "CUSTOM LOBBIES" select "CREATE".
      2. Near "LOBBY SETTINGS" select "EDIT".
      3. Under "GENERAL LOBBY SETTINGS" check the option "ENABLE CHEATS" (this will allow the match creation automation to be successful).
      4. Under "ADVANCED LOBBY SETTINGS", in "BOT SETTINGS", check the option "FILL EMPTY SLOTS WITH BOTS". Select for "RADIANT DIFFICULTY" and "DIRE DIFFICULTY" the option "UNFAIR" and for "RADIANT BOTS" and "DIRE BOTS" select the option "LOCAL DEV SCRIPT".
      5. Click "OK" and then click "LEAVE THIS LOBBY".
   3. Quit DOTA 2.

8. Copy this project's contents ("bots" directory) to "~/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/scripts/vscripts/".
The directory MUST be exactly named "bots", so that the LUA files can be read by DOTA 2!

9. Install, in your OS, the Python module "pyautogui". You can follow the steps under "Installing the pyautogui Module" in https://automatetheboringstuff.com/chapter18/

10. Install "xdotool" in your OS: https://github.com/jordansissel/xdotool

11. Try one of the two Python scripts provided to check if the API works on your system!
