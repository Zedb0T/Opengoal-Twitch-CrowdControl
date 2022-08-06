import socket
import threading
import os
import struct
import subprocess
import time
import sys
import random
from dotenv import load_dotenv
from os.path import exists
import shutil

"""
Created on Fri Apr 29 16:20:54 2022
@author: Yop Mike Zed
"""
#Set the working directory
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)

#COMMANDMODS, these users can use the REPL command to create custom commands!
COMMANDMODS = ["zed_b0t", "mikegamepro", "water112", "barg034"]

#env values
load_dotenv()
OAUTH = str(os.getenv("OAUTH"))
CONNECT_MSG = str(os.getenv("CONNECT_MSG"))
COOLDOWN_MSG = str(os.getenv("COOLDOWN_MSG"))
DISABLED_MSG = str(os.getenv("DISABLED_MSG"))
PREFIX = str(os.getenv("PREFIX"))

#bool that checks if its the launcher version
launcher_version = exists(application_path+"\OpenGOAL-Launcher.exe")

#paths
PATHTOGOALC = application_path + "\goalc.exe"
PATHTOGK = application_path +"\gk.exe -boot -fakeiso -debug -v"

#If its the launcher version update the paths!
if launcher_version:
	
	print("launcher version detected")
	shutil.copyfile(application_path+"/goalc.exe", os.getenv('APPDATA') +"\OpenGOAL-Launcher\\goalc.exe")
	time.sleep(1)
	PATHTOGOALC=os.getenv('APPDATA') +"\OpenGOAL-Launcher\\goalc.exe"
	extraGKCommand = "-proj-path "+os.getenv('APPDATA') +"\OpenGOAL-Launcher\\data "
	PATHTOGK = application_path +"\gk.exe "+extraGKCommand+"-boot -fakeiso -debug -v"

#
#Function definitions
#
def sendForm(form):
    header = struct.pack('<II', len(form), 10)
    clientSocket.sendall(header + form.encode())
    print("Sent: " + form)
    return

def run_check(id):
    if on_off[id] != "f":
    	global message
    	if (time.time() - last_used[id]) > cooldowns[id]:
    		last_used[id] = time.time()
    		return True
    	elif COOLDOWN_MSG == "t":
    		sendMessage(irc, "/me @"+user+" Command "+command_names[id]+" is on cooldown ("+str(int(last_used[id]-(time.time()-cooldowns[id])))+"s left).")
    		message = ""
    		return False
    	else:
    		message = ""
    		return False
    elif DISABLED_MSG == "t":
        sendMessage(irc, "/me @"+user+" Command "+command_names[id]+" is disabled.")
        message = ""
        return False
    else:
        message = ""
        return False

#
#Launch REPL, connect bot, and mi

#This splits the Gk commands into args for gk.exe
GKCOMMANDLINElist = PATHTOGK.split()

#Close Gk and goalc if they were open.
print("If it errors below that is O.K.")
subprocess.Popen("""taskkill /F /IM gk.exe""",shell=True)
subprocess.Popen("""taskkill /F /IM goalc.exe""",shell=True)
time.sleep(3)

#Open a fresh GK and goalc then wait a bit before trying to connect via socket.
print("opening " + PATHTOGK)
print("opening " + PATHTOGOALC)
subprocess.Popen(GKCOMMANDLINElist)
subprocess.Popen([PATHTOGOALC])
time.sleep(3)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientSocket.connect(("127.0.0.1", 8181))
time.sleep(1)
data = clientSocket.recv(1024)
print(data.decode())

#Int block these comamnds are sent on startup
sendForm("(lt)")
sendForm("(mi)")
sendForm("(send-event *target* 'get-pickup (pickup-type eco-red) 5.0)")
sendForm("(dotimes (i 1) (sound-play-by-name (static-sound-name \"cell-prize\") (new-sound-id) 1024 0 0 (sound-group sfx) #t))")
sendForm("(set! *cheat-mode* #f)")
sendForm("(set! *debug-segment* #f)")
#End Int block

#add all commands into an array so we can reference via index.
command_names = ["rjto","superjump","superboosted","noboosteds","fastjak","slowjak","pacifist","trip",
				 "shortfall","ghostjak","getoff","flutspeed","freecam","enemyspeed","give","collected",
				 "eco","sucksuck","noeco","die","gotopoint","randompoint","tp","shift","movetojak","ouch",
				 "burn","hp","melt","endlessfall","iframes","invertcam","normalcam","deload","frickstorage",
				 "dark","dax","smallnet","widefish","lod","moveplantboss","moveplantboss2","basincell","resetactors",
				 "repl"]

#intialize arrays same length as command_names
cooldowns = [0.0] * len(command_names)
last_used = [0.0] * len(command_names)
on_off = [0] * len(command_names)

#pull cooldowns set in env file and add to array.
for x in range(len(command_names)):
    cooldowns[x]=float(os.getenv(command_names[x]+"_cd"))
    on_off[x]=(os.getenv(command_names[x]))

#twitch irc stuff
SERVER = "irc.twitch.tv"
PORT = 6667

#Get Your OAUTH Code Here! https://twitchapps.com/tmi/

#What you'd like to name your bot
BOT = "jakopengoalbot"
#The channel you want to monitor
CHANNEL = str(os.getenv("TARGETCHANNEL")).lower()

#initialize empty strings to store user and message
message = ""
user = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((	"PASS " + OAUTH + "\n" +
			"NICK " + BOT + "\n" +
			"JOIN #" + CHANNEL + "\n").encode())

#array of valid checkpoints so user cant send garbage data
point_list = ["training-start", "game-start", "village1-hut", "village1-warp", "beach-start", "jungle-start", "jungle-tower", "misty-start", "misty-silo", "misty-bike", "misty-backside", "misty-silo2", "firecanyon-start", "firecanyon-end", "village2-start", "village2-warp", "village2-dock", "rolling-start", "sunken-start", "sunken1", "sunken2", "sunken-tube1", "sunkenb-start", "sunkenb-helix", "swamp-start", "swamp-dock1", "swamp-cave1", "swamp-dock2", "swamp-cave2", "swamp-game", "swamp-cave-3", "ogre-start", "ogre-race", "ogre-end", "village3-start", "village3-warp", "village3-farside", "maincave-start", "maincave-to-darkcave", "maincave-to-robocave", "darkcave-start", "robocave-start", "robocave-bottom", "snow-start snow-fort", "snow-snow-flut-flut", "snow-pass-to-fort", "snow-by-ice-lake", "snow-by-ice-lake-alt", "snow-outside-fort", "snow-outside-cave", "snow-across-from-flut"]

#sends a message to the irc channel.
def sendMessage(irc, message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
	irc.send((messageTemp + "\n").encode())

def gamecontrol():
	
	global message

	while True:
		#split a whole message into args so we can evaluate it one by one.
		args = message.split(" ")
		
		if PREFIX + "rjto" == str(args[0]).lower() and len(args) >= 2 and run_check(0):
			sendForm("(set! (-> *TARGET-bank* wheel-flip-dist) (meters " + str(args[1]) + "))")
			message = ""
		
		if PREFIX + "superjump" == str(args[0]).lower() and run_check(1):
			sendForm("(if (= (-> *TARGET-bank* jump-height-max)(meters 15.0))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 3.5))(set! (-> *TARGET-bank* jump-height-min)(meters 1.01))(set! (-> *TARGET-bank* double-jump-height-max)(meters 2.5))(set! (-> *TARGET-bank* double-jump-height-min)(meters 1)))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* jump-height-min)(meters 5.0))(set! (-> *TARGET-bank* double-jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* double-jump-height-min)(meters 5.0))))")
			message = ""
			
		if (PREFIX + "superboosted" == str(args[0]).lower() or PREFIX + "superboosteds" == str(args[0]).lower()) and run_check(2):
			sendForm("(if (not(=(-> *edge-surface* fric) 1.0))(set! (-> *edge-surface* fric) 1.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""

		if (PREFIX + "noboosteds" == str(args[0]).lower() or PREFIX + "noboosted" == str(args[0]).lower()) and run_check(3):
			sendForm("(if (not(=(-> *edge-surface* fric) 1530000.0))(set! (-> *edge-surface* fric) 1530000.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""
			
		if PREFIX + "fastjak" == str(args[0]).lower() and run_check(4):
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 99999.0))(begin(if (=(-> *walk-mods* target-speed) 20000.0)(pc-cheat-toggle-and-tune *pc-settings* eco-yellow))(set! (-> *walk-mods* target-speed) 99999.0)(set! (-> *double-jump-mods* target-speed) 99999.0)(set! (-> *jump-mods* target-speed) 99999.0)(set! (-> *jump-attack-mods* target-speed) 99999.0)(set! (-> *attack-mods* target-speed) 99999.0)(set! (-> *forward-high-jump-mods* target-speed) 99999.0)(set! (-> *jump-attack-mods* target-speed) 99999.0))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *forward-high-jump-mods* target-speed) 45056.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)))(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))")
			message = ""
		
		if PREFIX + "slowjak" == str(args[0]).lower() and run_check(5):
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 20000.0))(begin(set! (-> *walk-mods* target-speed) 20000.0)(set! (-> *double-jump-mods* target-speed) 20000.0)(set! (-> *jump-mods* target-speed) 20000.0)(set! (-> *jump-attack-mods* target-speed) 20000.0)(set! (-> *attack-mods* target-speed) 20000.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 0)))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
			message = ""
			
		if PREFIX + "pacifist" == str(args[0]).lower() and run_check(6):
			sendForm("(if(=(-> *TARGET-bank* punch-radius) -1.0)(begin(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 2.2))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1)))(begin(set! (-> *TARGET-bank* punch-radius) (meters -1.0))(set! (-> *TARGET-bank* spin-radius) (meters -1.0))(set! (-> *TARGET-bank* flop-radius) (meters -1.0))(set! (-> *TARGET-bank* uppercut-radius) (meters -1.0))))")
			message = ""
		
		if PREFIX + "trip" == str(args[0]).lower() and run_check(7):
			sendForm("(send-event *target* 'loading)")
			message = ""
			
		if PREFIX + "shortfall" == str(args[0]).lower() and run_check(8):
			sendForm("(if (= (-> *TARGET-bank* fall-far) (meters 1))(begin(set! (-> *TARGET-bank* fall-far) (meters 30))(set! (-> *TARGET-bank* fall-far-inc) (meters 20)))(begin (set! (-> *TARGET-bank* fall-far) (meters 1))(set! (-> *TARGET-bank* fall-far-inc) (meters 1))))")
			message = ""
				
		if PREFIX + "ghostjak" == str(args[0]).lower() and run_check(9):
			sendForm("(set! (-> *TARGET-bank* body-radius) (meters -1.0))")
			time.sleep(3)
			sendForm("(set! (-> *TARGET-bank* body-radius) (meters 0.7))")
			message = ""
			
		if PREFIX + "getoff" == str(args[0]).lower() and run_check(10):
			sendForm("(send-event *target* 'end-mode)")
			message = ""
			
		if (PREFIX + "setflutflut" == str(args[0]).lower() or PREFIX + "flutspeed" == str(args[0]).lower()) and len(args) >= 2 and run_check(11):
			sendForm("(set! (-> *flut-walk-mods* target-speed)(meters " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "freecam" == str(args[0]).lower() and run_check(12):
			sendForm("(stop 'debug)")
			time.sleep(6)
			sendForm("(start 'play (get-or-create-continue! *game-info*))")
			message = ""
			
		if PREFIX + "enemyspeed" == str(args[0]).lower() and len(args) >= 3 and run_check(13):
			sendForm("(set! (-> *" + str(args[1]) + "-nav-enemy-info* run-travel-speed) (meters " + str(args[2]) + "))")
			message = ""
			
		if PREFIX + "give" == str(args[0]).lower() and len(args) >= 3 and run_check(14):
			sendForm("(set! (-> *game-info* " + str(args[1]) + ") (+ (-> *game-info* " + str(args[1]) + ") " + str(args[2]) + "))")
			message = ""
			
		if (PREFIX + "setcollected" == str(args[0]).lower() or PREFIX + "collected" == str(args[0]).lower()) and len(args) >= 3 and run_check(15):
			sendForm("(set! (-> *game-info* " + str(args[1]) + ") (+ 0.0 " + str(args[2]) + "))")
			message = ""

		if PREFIX + "eco" == str(args[0]).lower() and len(args) >= 2 and run_check(16):
			sendForm("(send-event *target* 'get-pickup (pickup-type eco-" + str(args[1]) + ") 5.0)")
			message = ""
			
		if (PREFIX + "sucksuck" == str(args[0]).lower() or PREFIX + "setsucksuck" == str(args[0]).lower()) and len(args) >= 2 and run_check(17):
			sendForm("(set! (-> *FACT-bank* suck-suck-dist) (meters " + str(args[1]) + "))(set! (-> *FACT-bank* suck-bounce-dist) (meters " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "noeco" == str(args[0]).lower() and run_check(18):
			sendForm("(if (> (-> *FACT-bank* eco-full-timeout) 0.0)(set! (-> *FACT-bank* eco-full-timeout) (seconds 0.0))(set! (-> *FACT-bank* eco-full-timeout) (seconds 20.0)))")
			message = ""
			
		if PREFIX + "die" == str(args[0]).lower() and run_check(19):
			sendForm("(initialize! *game-info* 'die (the-as game-save #f) (the-as string #f))")
			message = ""
			
		if (PREFIX + "gotolevel" == str(args[0]).lower() or PREFIX + "gotopoint" == str(args[0]).lower()) and len(args) >= 2 and run_check(20):
			sendForm("(start 'play (get-continue-by-name *game-info* \"" + str(args[1]) + "\"))")
			message = ""
			
		if (PREFIX + "randompoint" == str(args[0]).lower() or PREFIX + "randomcheckpoint" == str(args[0]).lower()) and run_check(21):
			sendForm("(start 'play (get-continue-by-name *game-info* \"" + str(random.choice(point_list)) + "\"))")
			message = ""
			
		if PREFIX + "tp" == str(args[0]).lower() and len(args) >= 4 and run_check(22):
			sendForm("(set! (-> (target-pos 0) x) (meters " + str(args[1]) + "))  (set! (-> (target-pos 0) y) (meters " + str(args[2]) + ")) (set! (-> (target-pos 0) z) (meters " + str(args[3]) + "))")
			message = ""
			
		if PREFIX + "shift" == str(args[0]).lower() and len(args) >= 4 and run_check(23):
			sendForm("(set! (-> (target-pos 0) x) (+ (-> (target-pos 0) x)(meters " + str(args[1]) + ")))  (set! (-> (target-pos 0) y) (+ (-> (target-pos 0) y)(meters " + str(args[2]) + "))) (set! (-> (target-pos 0) z) (+ (-> (target-pos 0) z)(meters " + str(args[3]) + ")))")
			message = ""
			
		if PREFIX + "movetojak" == str(args[0]).lower() and len(args) >= 2 and run_check(24):
			sendForm("(when (process-by-ename \"" + str(args[1]) + "\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"" + str(args[1]) + "\"))root)trans) (-> (target-pos 0) x) (-> (target-pos 0) y) (-> (target-pos 0) z) 1.0))")
			message = ""

		if PREFIX + "ouch" == str(args[0]).lower() and run_check(25):
			sendForm("(send-event *target* 'attack #t (new 'static 'attack-info))")
			message = ""

		if PREFIX + "burn" == str(args[0]).lower() and run_check(26):
			sendForm("(target-attack-up *target* 'attack 'burnup)")
			message = ""
			
		if PREFIX + "hp" == str(args[0]).lower() and len(args) >= 2 and run_check(27):
			sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) (+ 0.0 " + str(args[1]) + "))")
			message = ""

		if PREFIX + "melt" == str(args[0]).lower() and run_check(28):
			sendForm("(target-attack-up *target* 'attack 'melt)")
			message = ""
			
		if PREFIX + "endlessfall" == str(args[0]).lower() and run_check(29):
			sendForm("(target-attack-up *target* 'attack 'endlessfall)")
			message = ""
			
		if PREFIX + "iframes" == str(args[0]).lower() and len(args) >= 2 and run_check(30):
			sendForm("(set! (-> *TARGET-bank* hit-invulnerable-timeout) (seconds " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "invertcam" == str(args[0]).lower() and len(args) >= 3 and run_check(31):
			sendForm("(set! (-> *pc-settings* " + str(args[1]) + "-camera-" + str(args[2]) + "-inverted?) (not (-> *pc-settings* " + str(args[1]) + "-camera-" + str(args[2]) + "-inverted?)))")
			message = ""
			
		if PREFIX + "normalcam" == str(args[0]).lower() and run_check(32):
			sendForm("(set! (-> *pc-settings* third-camera-h-inverted?) #t)(set! (-> *pc-settings* third-camera-v-inverted?) #t)(set! (-> *pc-settings* first-camera-v-inverted?) #t)(set! (-> *pc-settings* first-camera-h-inverted?) #f)")
			message = ""
			
		if PREFIX + "deload" == str(args[0]).lower() and run_check(33):
			sendForm("(set! (-> *load-state* want 0 display?) #f)")
			message = ""
			
		if PREFIX + "frickstorage" == str(args[0]).lower() and run_check(34):
			sendForm("(stop 'debug)", 34)
			time.sleep(0.001)
			sendForm("(start 'debug (get-or-create-continue! *game-info*))")
			message = ""
			
		if PREFIX + "dark" == str(args[0]).lower() and run_check(35):
			sendForm("(if (not (= (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss)) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-training))")
			message = ""
		
		if PREFIX + "dax" == str(args[0]).lower() and run_check(36):
			sendForm("(send-event *target* 'sidekick (not (not (send-event *target* 'sidekick #t))))")
			message = ""
			
		if PREFIX + "smallnet" == str(args[0]).lower() and run_check(37):
			sendForm("(if (=(-> *FISHER-bank* net-radius)(meters 0.0))(set!(-> *FISHER-bank* net-radius)(meters 0.7))(set! (-> *FISHER-bank* net-radius)(meters 0.0)))")
			message = ""

		if PREFIX + "widefish" == str(args[0]).lower() and run_check(38):
			sendForm("(if (=(-> *FISHER-bank* width)(meters 10.0))(set! (-> *FISHER-bank* width)(meters 3.3))(set! (-> *FISHER-bank* width)(meters 10.0)))")
			message = ""
		
		if PREFIX + "lod" == str(args[0]).lower() and run_check(39):
			sendForm("(if (= (-> *pc-settings* lod-force-tfrag) 2)(begin(set! (-> *pc-settings* lod-force-tfrag) 0)(set! (-> *pc-settings* lod-force-tie) 0)(set! (-> *pc-settings* lod-force-ocean) 0)(set! (-> *pc-settings* lod-force-actor) 0))(begin(set! (-> *pc-settings* lod-force-tfrag) 2)(set! (-> *pc-settings* lod-force-tie) 3)(set! (-> *pc-settings* lod-force-ocean) 2)(set! (-> *pc-settings* lod-force-actor) 3)))")
			message = ""
		
		if PREFIX + "moveplantboss" == str(args[0]).lower() and run_check(40):
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) 1.0)")
			time.sleep(2)
			sendForm("(set! (-> (target-pos 0) x) (meters 431.47))  (set! (-> (target-pos 0) y) (meters -44.00)) (set! (-> (target-pos 0) z) (meters -334.09))")
			message = ""
		
		if PREFIX + "moveplantboss2" == str(args[0]).lower() and run_check(41):
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			message = ""
			
		if PREFIX + "basincell" == str(args[0]).lower() and run_check(42):
			sendForm("(if (when (process-by-ename \"fuel-cell-45\") (= (-> (->(the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans x)  (meters -266.54)))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -248.92) (meters 52.11) (meters -1515.66) 1.0))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -266.54) (meters 52.11) (meters -1508.48) 1.0)))")
			message = ""
			
		if PREFIX + "resetactors" == str(args[0]).lower() and run_check(43):
			sendForm("(reset-actors 'debug)")
			message = ""
		
		#if PREFIX + "nopunching" == str(args[0]).lower():
		#	sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds 20 ))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
		#	message = ""
		
		if PREFIX + "actorson" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			message = ""
		
		if PREFIX + "actorsoff" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #f)")
			message = ""
		
		if PREFIX + "debug" == str(args[0]).lower():
			if COMMANDMODS.count(user) == 1:
				sendForm("(set! *debug-segment* (not *debug-segment*))(set! *cheat-mode* (not *cheat-mode*))")
				message = ""
			else:
				message = ""
			
		#if PREFIX + "heatmax" == str(args[0]).lower() and len(args) >= 2:
		#	sendForm("(set! (-> *RACER-bank* heat-max) " + str(args[1]) + ")")
		#	message = ""
			
		#if PREFIX + "loadlevel" == str(args[0]).lower() and len(args) >= 2:
		#	sendForm("(set! (-> *load-state* want 1 name) '" + str(args[1]) + ")(set! (-> *load-state* want 1 display?) 'display)")
		#	message = ""
			
		#if (PREFIX + "setecotime" == str(args[0]).lower() or PREFIX + "ecotime" == str(args[0]).lower()) and len(args) >= 2:
		#	sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds " + str(args[1]) + "))")
		#	message = ""
			
		if str(args[0]) == PREFIX + "repl" and len(args) >= 2 and run_check(44):
			if COMMANDMODS.count(user) == 1:
				args = message.split(" ", 1)
				sendForm(str(args[1]))
				message = ""
			else:
				sendMessage(irc, "/me @"+user+"Sorry, repl is currently only accessable to the devs.")
				message = ""
			
#Dont touch
def twitch():

	global user
	global message

	def joinchat():
		Loading = True
		while Loading:
			readbuffer_join = irc.recv(1024)
			readbuffer_join = readbuffer_join.decode()
			print(readbuffer_join)
			for line in readbuffer_join.split("\n")[0:-1]:
				print(line)
				Loading = loadingComplete(line)

	def loadingComplete(line):
		if("End of /NAMES list" in line):
			print("TwitchBot has joined " + CHANNEL + "'s Channel!")
			sendMessage(irc, "/me "+CONNECT_MSG)
			return False
		else:
			return True


	def getUser(line):
		#global user
		colons = line.count(":")
		colonless = colons-1
		separate = line.split(":", colons)
		user = separate[colonless].split("!", 1)[0]
		return user

	def getMessage(line):
		#global message
		print(line)
		try:
			colons = line.count(":")
			message = (line.split(":", colons))[colons]
		except:
			message = ""
		return message

	def console(line):
		if "PRIVMSG" in line:
			return False
		else:
			return True

	joinchat()
	irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
	while True:
		try:
			readbuffer = irc.recv(1024).decode()
		except:
			readbuffer = ""
		for line in readbuffer.split("\r\n"):
			if line == "":
				continue
			if "PING :tmi.twitch.tv" in line:
				print(line)
				msgg = "PONG :tmi.twitch.tv\r\n".encode()
				irc.send(msgg)
				print(msgg)
				continue
			else:
				try:
					user = getUser(line)
					message = getMessage(line)
					print("message is " + message)
				except Exception:
					pass

def main():
	if __name__ =='__main__':
		t1 = threading.Thread(target = twitch)
		t1.start()
		t2 = threading.Thread(target = gamecontrol)
		t2. start()
main()