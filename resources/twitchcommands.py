import socket
import threading
import os
import struct
import subprocess
import time
import sys
import random
from dotenv import load_dotenv

load_dotenv()





"""
Created on Fri Apr 29 16:20:54 2022
@author: Yop
"""

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)

print(application_path)
OAUTH = str(os.getenv("OAUTH"))
PATHTOGOALC = application_path + "\goalc.exe"
PATHTOGK = application_path + "\gk.exe -boot -fakeiso -debug -v"

CONNECTIONMESSAGE = str(os.getenv("CONNECTIONMESSAGE"))
MOTD = "u playing jak?"
COMMANDMODS = ["zed_b0t", "mikegamepro", "water112", "barg034"]
PREFIX = str(os.getenv("PREFIX"))
#GPATH = r"c:\Users\Yop\source\repos\jak-project"

#
#Function definitions
#
def sendForm(form):
    header = struct.pack('<II', len(form), 10)
    clientSocket.sendall(header + form.encode())
    print("Sent: " + form)
    return

#
#Launch REPL, connect bot, and mi
#
#os.system(r'start "'+ MOTD +'" /d "C:\\Users\\Zed\\Documents\\GitHub\\OpenGoalCheckpointRandomizer\\Checkpoint randomizer\\goalc.exe"') #repl cmd window
#"%mypath%/gk.exe" -boot -fakeiso -debug -v
GKCOMMANDLINE = PATHTOGK
GKCOMMANDLINElist = GKCOMMANDLINE.split()
print("If it errors below that is O.K.")
subprocess.Popen("""taskkill /F /IM gk.exe""",shell=True)
subprocess.Popen("""taskkill /F /IM goalc.exe""",shell=True)
time.sleep(3)
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


#Int block
sendForm("(lt)")
sendForm("(mi)")
sendForm("(send-event *target* 'get-pickup (pickup-type eco-red) 5.0)")
sendForm("(dotimes (i 1) (sound-play-by-name (static-sound-name \"cell-prize\") (new-sound-id) 1024 0 0 (sound-group sfx) #t))")
sendForm("(set! *cheat-mode* #f)")
sendForm("(set! *debug-segment* #f)")
#End Int block



SERVER = "irc.twitch.tv"
PORT = 6667

#Your OAUTH Code Here https://twitchapps.com/tmi/


#What you'd like to name your bot
BOT = "jakopengoalbot"
#The channel you want to monitor
CHANNEL = str(os.getenv("TARGETCHANNEL")).lower()

message = ""
user = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((	"PASS " + OAUTH + "\n" +
			"NICK " + BOT + "\n" +
			"JOIN #" + CHANNEL + "\n").encode())

point_list = ["training-start", "game-start", "village1-hut", "village1-warp", "beach-start", "jungle-start", "jungle-tower", "misty-start", "misty-silo", "misty-bike", "misty-backside", "misty-silo2", "firecanyon-start", "firecanyon-end", "village2-start", "village2-warp", "village2-dock", "rolling-start", "sunken-start", "sunken1", "sunken2", "sunken-tube1", "sunkenb-start", "sunkenb-helix", "swamp-start", "swamp-dock1", "swamp-cave1", "swamp-dock2", "swamp-cave2", "swamp-game", "swamp-cave-3", "ogre-start", "ogre-race", "ogre-end", "village3-start", "village3-warp", "village3-farside", "maincave-start", "maincave-to-darkcave", "maincave-to-robocave", "darkcave-start", "robocave-start", "robocave-bottom", "snow-start snow-fort", "snow-snow-flut-flut", "snow-pass-to-fort", "snow-by-ice-lake", "snow-by-ice-lake-alt", "snow-outside-fort", "snow-outside-cave", "snow-across-from-flut"]

def gamecontrol():

	global message

	while True:
		args = message.split(" ")
		
		if PREFIX + "trip" == str(args[0]).lower():
			sendForm("(send-event *target* 'loading)")
			message = ""

		if PREFIX + "superjump" == str(args[0]).lower():
			sendForm("(if (= (-> *TARGET-bank* jump-height-max)(meters 15.0))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 3.5))(set! (-> *TARGET-bank* jump-height-min)(meters 1.01))(set! (-> *TARGET-bank* double-jump-height-max)(meters 2.5))(set! (-> *TARGET-bank* double-jump-height-min)(meters 1)))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* jump-height-min)(meters 5.0))(set! (-> *TARGET-bank* double-jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* double-jump-height-min)(meters 5.0))))")
			message = ""

		if PREFIX + "pacifist" == str(args[0]).lower():
			sendForm("(if(=(-> *TARGET-bank* punch-radius) -1.0)(begin(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 2.2))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1)))(begin(set! (-> *TARGET-bank* punch-radius) (meters -1.0))(set! (-> *TARGET-bank* spin-radius) (meters -1.0))(set! (-> *TARGET-bank* flop-radius) (meters -1.0))(set! (-> *TARGET-bank* uppercut-radius) (meters -1.0))))")
			message = ""
			
		if PREFIX + "ghostjak" == str(args[0]).lower():
			sendForm("(set! (-> *TARGET-bank* body-radius) (meters -1.0))")
			time.sleep(3)
			sendForm("(set! (-> *TARGET-bank* body-radius) (meters 0.7))")
			message = ""

		if PREFIX + "superboosted" == str(args[0]).lower():
			sendForm("(if (not(=(-> *edge-surface* fric) 1.0))(set! (-> *edge-surface* fric) 1.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""

		if PREFIX + "noboosteds" == str(args[0]).lower():
			sendForm("(if (not(=(-> *edge-surface* fric) 1530000.0))(set! (-> *edge-surface* fric) 1530000.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""

		if PREFIX + "smallnet" == str(args[0]).lower():
			sendForm("(if (=(-> *FISHER-bank* net-radius)(meters 0.0))(set!(-> *FISHER-bank* net-radius)(meters 0.7))(set! (-> *FISHER-bank* net-radius)(meters 0.0)))")
			message = ""

		if PREFIX + "widefish" == str(args[0]).lower():
			sendForm("(if (=(-> *FISHER-bank* width)(meters 10.0))(set! (-> *FISHER-bank* width)(meters 3.3))(set! (-> *FISHER-bank* width)(meters 10.0)))")
			message = ""
		
		if PREFIX + "die" == str(args[0]).lower():
			sendForm("(initialize! *game-info* 'die (the-as game-save #f) (the-as string #f))")
			message = ""

		if PREFIX + "melt" == str(args[0]).lower():
			sendForm("(target-attack-up *target* 'attack 'melt)")
			message = ""

		if PREFIX + "endlessfall" == str(args[0]).lower():
			sendForm("(target-attack-up *target* 'attack 'endlessfall)")
			message = ""

		if PREFIX + "burn" == str(args[0]).lower():
			sendForm("(target-attack-up *target* 'attack 'burnup)")
			message = ""
			
		if PREFIX + "hp" == str(args[0]).lower():
			sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) (+ 0.0 " + str(args[1]) + "))")
			message = ""

		if PREFIX + "moveplantboss" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) 1.0)")
			time.sleep(2)
			sendForm("(set! (-> (target-pos 0) x) (meters 431.47))  (set! (-> (target-pos 0) y) (meters -44.00)) (set! (-> (target-pos 0) z) (meters -334.09))")
			message = ""
		
		if PREFIX + "moveplantboss2" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			message = ""
		
		if PREFIX + "nopunching" == str(args[0]).lower():
			sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds 20 ))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
			message = ""
		
		if PREFIX + "deload" == str(args[0]).lower():
			sendForm("(set! (-> *load-state* want 0 display?) #f)")
			message = ""
		
		if PREFIX + "noeco" == str(args[0]).lower():
			sendForm("(if (> (-> *FACT-bank* eco-full-timeout) 0.0)(set! (-> *FACT-bank* eco-full-timeout) (seconds 0.0))(set! (-> *FACT-bank* eco-full-timeout) (seconds 20.0)))")
			message = ""
			
		if PREFIX + "randomcheckpoint" == str(args[0]).lower():
			sendForm("")
			message = ""
		
		if PREFIX + "getoff" == str(args[0]).lower():
			sendForm("(send-event *target* 'end-mode)")
			message = ""
		
		if PREFIX + "dax" == str(args[0]).lower():
			sendForm("(send-event *target* 'sidekick (not (not (send-event *target* 'sidekick #t))))")
			message = ""
		
		if PREFIX + "ouch" == str(args[0]).lower():
			sendForm("(send-event *target* 'attack #t (new 'static 'attack-info))")
			message = ""
		
		if PREFIX + "lod" == str(args[0]).lower():
			sendForm("(if (= (-> *pc-settings* lod-force-tfrag) 2)(begin(set! (-> *pc-settings* lod-force-tfrag) 0)(set! (-> *pc-settings* lod-force-tie) 0)(set! (-> *pc-settings* lod-force-ocean) 0)(set! (-> *pc-settings* lod-force-actor) 0))(begin(set! (-> *pc-settings* lod-force-tfrag) 2)(set! (-> *pc-settings* lod-force-tie) 3)(set! (-> *pc-settings* lod-force-ocean) 2)(set! (-> *pc-settings* lod-force-actor) 3)))")
			message = ""
		
		if PREFIX + "dark" == str(args[0]).lower():
			sendForm("(if (not (= (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss)) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-training))")
			message = ""
		
		if PREFIX + "heal" == str(args[0]).lower():
			sendForm("(send-event *target* 'get-pickup 4 1.0)")
			message = ""
		
		if PREFIX + "fastjak" == str(args[0]).lower():
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 99999.0))(begin(if (=(-> *walk-mods* target-speed) 20000.0)(pc-cheat-toggle-and-tune *pc-settings* eco-yellow))(set! (-> *walk-mods* target-speed) 99999.0)(set! (-> *double-jump-mods* target-speed) 99999.0)(set! (-> *jump-mods* target-speed) 99999.0)(set! (-> *jump-attack-mods* target-speed) 99999.0)(set! (-> *attack-mods* target-speed) 99999.0)(set! (-> *forward-high-jump-mods* target-speed) 99999.0)(set! (-> *jump-attack-mods* target-speed) 99999.0))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *forward-high-jump-mods* target-speed) 45056.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)))(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))")
			message = ""
		
		if PREFIX + "slowjak" == str(args[0]).lower():
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 20000.0))(begin(set! (-> *walk-mods* target-speed) 20000.0)(set! (-> *double-jump-mods* target-speed) 20000.0)(set! (-> *jump-mods* target-speed) 20000.0)(set! (-> *jump-attack-mods* target-speed) 20000.0)(set! (-> *attack-mods* target-speed) 20000.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 0)))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
			message = ""
		
		if PREFIX + "actorson" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			message = ""
		
		if PREFIX + "actorsoff" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #f)")
			message = ""
		
		if PREFIX + "debug" == str(args[0]).lower():
			sendForm("(set! *debug-segment* (not *debug-segment*))(set! *cheat-mode* (not *cheat-mode*))")
			message = ""
		
		if PREFIX + "shortfall" == str(args[0]).lower():
			sendForm("(if (= (-> *TARGET-bank* fall-far) (meters 1))(begin(set! (-> *TARGET-bank* fall-far) (meters 30))(set! (-> *TARGET-bank* fall-far-inc) (meters 20)))(begin (set! (-> *TARGET-bank* fall-far) (meters 1))(set! (-> *TARGET-bank* fall-far-inc) (meters 1))))")
			message = ""
		
		if PREFIX + "basincell" == str(args[0]).lower():
			sendForm("(if (when (process-by-ename \"fuel-cell-45\") (= (-> (->(the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans x)  (meters -266.54)))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -248.92) (meters 52.11) (meters -1515.66) 1.0))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -266.54) (meters 52.11) (meters -1508.48) 1.0)))")
			message = ""
		
		if PREFIX + "frickstorage" == str(args[0]).lower():
			sendForm("(stop 'debug)")
			time.sleep(0.001)
			sendForm("(start 'debug (get-or-create-continue! *game-info*))")
			message = ""
		
		if PREFIX + "freecam" == str(args[0]).lower():
			sendForm("(stop 'debug)")
			time.sleep(6)
			sendForm("(start 'play (get-or-create-continue! *game-info*))")
			message = ""
		
		if PREFIX + "invertcam" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* " + str(args[1]) + "-camera-" + str(args[2]) + "-inverted?) (not (-> *pc-settings* " + str(args[1]) + "-camera-" + str(args[2]) + "-inverted?)))")
			message = ""
			
		if PREFIX + "normalcam" == str(args[0]).lower():
			sendForm("(set! (-> *pc-settings* third-camera-h-inverted?) #t)(set! (-> *pc-settings* third-camera-v-inverted?) #t)(set! (-> *pc-settings* first-camera-v-inverted?) #t)(set! (-> *pc-settings* first-camera-h-inverted?) #f)")
			message = ""
			
		if PREFIX + "randompoint" == str(args[0]).lower() or PREFIX + "randomcheckpoint" == str(args[0]).lower():
			sendForm("(start 'play (get-continue-by-name *game-info* \"" + str(random.choice(point_list)) + "\"))")
			message = ""
			
		if PREFIX + "gotolevel" == str(args[0]).lower() or PREFIX + "gotopoint" == str(args[0]).lower():
			sendForm("(start 'play (get-continue-by-name *game-info* \"" + str(args[1]) + "\"))")
			message = ""
		
		if PREFIX + "rjto" == str(args[0]).lower():
			sendForm("(set! (-> *TARGET-bank* wheel-flip-dist) (meters " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "movetojak" == str(args[0]).lower():
			sendForm("(when (process-by-ename \"" + str(args[1]) + "\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"" + str(args[1]) + "\"))root)trans) (-> (target-pos 0) x) (-> (target-pos 0) y) (-> (target-pos 0) z) 1.0))")
			message = ""
			
		if PREFIX + "eco" == str(args[0]).lower():
			sendForm("(send-event *target* 'get-pickup (pickup-type eco-" + str(args[1]) + ") 5.0)")
			message = ""
		
		if PREFIX + "heatmax" == str(args[0]).lower():
			sendForm("(set! (-> *RACER-bank* heat-max) " + str(args[1]) + ")")
			message = ""
			
		if PREFIX + "iframes" == str(args[0]).lower():
			sendForm("(set! (-> *TARGET-bank* hit-invulnerable-timeout) (seconds " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "give" == str(args[0]).lower():
			sendForm("(set! (-> *game-info* " + str(args[1]) + ") (+ (-> *game-info* " + str(args[1]) + ") " + str(args[2]) + "))")
			message = ""
			
		if PREFIX + "setcollected" == str(args[0]).lower() or PREFIX + "collected" == str(args[0]).lower():
			sendForm("(set! (-> *game-info* " + str(args[1]) + ") (+ 0.0 " + str(args[2]) + "))")
			message = ""
			
		if PREFIX + "enemyspeed" == str(args[0]).lower():
			sendForm("(set! (-> *" + str(args[1]) + "-nav-enemy-info* run-travel-speed) (meters " + str(args[2]) + "))")
			message = ""
			
		if PREFIX + "tp" == str(args[0]).lower():
			sendForm("(set! (-> (target-pos 0) x) (meters " + str(args[1]) + "))  (set! (-> (target-pos 0) y) (meters " + str(args[2]) + ")) (set! (-> (target-pos 0) z) (meters " + str(args[3]) + "))")
			message = ""
			
		if PREFIX + "shift" == str(args[0]).lower():
			sendForm("(set! (-> (target-pos 0) x) (+ (-> (target-pos 0) x)(meters " + str(args[1]) + ")))  (set! (-> (target-pos 0) y) (+ (-> (target-pos 0) y)(meters " + str(args[2]) + "))) (set! (-> (target-pos 0) z) (+ (-> (target-pos 0) z)(meters " + str(args[3]) + ")))")
			message = ""
		
		if PREFIX + "loadlevel" == str(args[0]).lower():
			sendForm("(set! (-> *load-state* want 1 name) '" + str(args[1]) + ")(set! (-> *load-state* want 1 display?) 'display)")
			message = ""
			
		if PREFIX + "sucksuck" == str(args[0]).lower() or PREFIX + "setsucksuck" == str(args[0]).lower():
			sendForm("(set! (-> *FACT-bank* suck-suck-dist) (meters " + str(args[1]) + "))(set! (-> *FACT-bank* suck-bounce-dist) (meters " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "setecotime" == str(args[0]).lower() or PREFIX + "ecotime" == str(args[0]).lower():
			sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds " + str(args[1]) + "))")
			message = ""
			
		if PREFIX + "setflutflut" == str(args[0]).lower() or PREFIX + "flutspeed" == str(args[0]).lower():
			sendForm("(set! (-> *flut-walk-mods* target-speed)(meters " + str(args[1]) + "))")
			message = ""
			
		if str(args[0]) == PREFIX + "repl":
			if COMMANDMODS.count(user) == 1:
				args = message.split(" ", 1)
				sendForm(str(args[1]))
				message = ""
			if COMMANDMODS.count(user) != 1:
				message = ""
			

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
			sendMessage(irc, CONNECTIONMESSAGE)
			return False
		else:
			return True

	def sendMessage(irc, message):
		messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
		irc.send((messageTemp + "\n").encode())

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