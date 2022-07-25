from ast import arg
import socket
import threading
from ahk import AHK
import os
import struct
import subprocess
import time
import sys
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
PATHTOAHK = str(os.getenv("PATHTOAHK"))
CONNECTIONMESSAGE = str(os.getenv("CONNECTIONMESSAGE"))
MOTD = "u playing jak?"
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

ahk = AHK(executable_path=PATHTOAHK)

SERVER = "irc.twitch.tv"
PORT = 6667

#Your OAUTH Code Here https://twitchapps.com/tmi/


#What you'd like to name your bot
BOT = "TwitchBot"
#The channel you want to monitor
CHANNEL = str(os.getenv("TARGETCHANNEL"))

message = ""
user = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((	"PASS " + OAUTH + "\n" +
			"NICK " + BOT + "\n" +
			"JOIN #" + CHANNEL + "\n").encode())

def gamecontrol():

	global message

	while True:

		if "!trip" == message.lower():
			print(message)
			sendForm("(send-event *target* 'loading)")
			message = ""

		if "!superjump" == message.lower():
			sendForm("(if (= (-> *TARGET-bank* jump-height-max)(meters 15.0))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 3.5))(set! (-> *TARGET-bank* jump-height-min)(meters 1.01))(set! (-> *TARGET-bank* double-jump-height-max)(meters 2.5))(set! (-> *TARGET-bank* double-jump-height-min)(meters 1)))(begin (set! (-> *TARGET-bank* jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* jump-height-min)(meters 5.0))(set! (-> *TARGET-bank* double-jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* double-jump-height-min)(meters 5.0))))")
			message = ""

		if "!pacifist" == message.lower():
			sendForm("(if(=(-> *TARGET-bank* punch-radius) 0.0)(begin(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 2.2))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1)))(begin(set! (-> *TARGET-bank* punch-radius) (meters 0.0))(set! (-> *TARGET-bank* spin-radius) (meters 0.0))(set! (-> *TARGET-bank* flop-radius) (meters 0.0))(set! (-> *TARGET-bank* uppercut-radius) (meters 0.0))))")
			message = ""

		if "!superboosted" == message.lower():
			sendForm("(if (not(=(-> *edge-surface* fric) 1.0))(set! (-> *edge-surface* fric) 1.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""

		if "!noboosteds" == message.lower():
			sendForm("(if (not(=(-> *edge-surface* fric) 1530000.0))(set! (-> *edge-surface* fric) 1530000.0)(set! (-> *edge-surface* fric) 30720.0))")
			message = ""

		if "!smallnet" == message.lower():
			sendForm("(if (=(-> *FISHER-bank* net-radius)(meters 0.0))(set!(-> *FISHER-bank* net-radius)(meters 0.7))(set! (-> *FISHER-bank* net-radius)(meters 0.0)))")
			message = ""

		if "!widefish" == message.lower():
			sendForm("(if (=(-> *FISHER-bank* width)(meters 10.0))(set! (-> *FISHER-bank* width)(meters 3.3))(set! (-> *FISHER-bank* width)(meters 10.0)))")
			message = ""

		if "!melt" == message.lower():
			sendForm("(target-attack-up *target* 'attack 'melt)")
			message = ""

		if "!endlessfall" == message.lower():
			sendForm("(target-attack-up *target* 'attack 'endlessfall)")
			message = ""

		if "!burn" == message.lower():
			sendForm("(target-attack-up *target* 'attack 'burnup)")
			message = ""

		if "!moveplantboss" == message.lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) 1.0)")
			time.sleep(2)
			sendForm("(set! (-> (target-pos 0) x) (meters 431.47))  (set! (-> (target-pos 0) y) (meters -44.00)) (set! (-> (target-pos 0) z) (meters -334.09))")
			message = ""
		
		if "!moveplantboss2" == message.lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			time.sleep(0.050)
			sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
			message = ""
		
		if "!nopunching" == message.lower():
			sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds 20 ))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
			message = ""
		
		if "!deload" == message.lower():
			sendForm("(set! (-> *load-state* want 0 display?) #f)")
			message = ""
		
		if "!noeco" == message.lower():
			sendForm("(send-event *target* 'get-pickup (pickup-type eco-yellow) 0.1)(send-event *target* 'get-pickup (pickup-type eco-red) 0.1)(set! (-> *FACT-bank* eco-full-timeout) (seconds 0.0001 ))")
			time.sleep(10)
			sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds 20))")
			message = ""
		
		if "!randomcheckpoint" == message.lower():
			sendForm("")
			message = ""
		
		if "!getoff" == message.lower():
			sendForm("(send-event *target* 'end-mode)")
			message = ""
		
		if "!dax" == message.lower():
			sendForm("(send-event *target* 'sidekick (not (not (send-event *target* 'sidekick #t))))")
			message = ""
		
		if "!ouch" == message.lower():
			sendForm("(send-event *target* 'attack #t (new 'static 'attack-info))")
			message = ""
		
		if "!lod" == message.lower():
			sendForm("(if (= (-> *pc-settings* lod-force-tfrag) 2)(begin(set! (-> *pc-settings* lod-force-tfrag) 0)(set! (-> *pc-settings* lod-force-tie) 0)(set! (-> *pc-settings* lod-force-ocean) 0)(set! (-> *pc-settings* lod-force-actor) 0))(begin(set! (-> *pc-settings* lod-force-tfrag) 2)(set! (-> *pc-settings* lod-force-tie) 3)(set! (-> *pc-settings* lod-force-ocean) 2)(set! (-> *pc-settings* lod-force-actor) 3)))")
			message = ""
		
		if "!dark" == message.lower():
			sendForm("(if (not (= (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss)) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-finalboss) (set! (-> (level-get-target-inside *level*) mood-func)update-mood-training))")
			message = ""
		
		if "!heal" == message.lower():
			sendForm("(send-event *target* 'get-pickup 4 1.0)")
			message = ""
		
		if "!fastjak" == message.lower():
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 99999.0))(begin(if (=(-> *walk-mods* target-speed) 20000.0)(pc-cheat-toggle-and-tune *pc-settings* eco-yellow))(set! (-> *walk-mods* target-speed) 99999.0)(set! (-> *double-jump-mods* target-speed) 99999.0)(set! (-> *jump-mods* target-speed) 99999.0)(set! (-> *jump-attack-mods* target-speed) 99999.0)(set! (-> *attack-mods* target-speed) 99999.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3)))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))))")
			message = ""
		
		if "!slowjak" == message.lower():
			sendForm("(if (not(=(-> *jump-attack-mods* target-speed) 20000.0))(begin(set! (-> *walk-mods* target-speed) 20000.0)(set! (-> *double-jump-mods* target-speed) 20000.0)(set! (-> *jump-mods* target-speed) 20000.0)(set! (-> *jump-attack-mods* target-speed) 2000.0)(set! (-> *attack-mods* target-speed) 20000.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 0)))(begin(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))))(pc-cheat-toggle-and-tune *pc-settings* eco-yellow)")
			message = ""
		
		if "!actorson" == message.lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #t)")
			message = ""
		
		if "!actorsoff" == message.lower():
			sendForm("(set! (-> *pc-settings* force-actors?) #f)")
			message = ""
		
		if "!debug" == message.lower():
			sendForm("(set! *debug-segment* (not *debug-segment*))(set! *cheat-mode* (not *cheat-mode*))")
			message = ""
		
		if "!shortfall" == message.lower():
			sendForm("(if (= (-> *TARGET-bank* fall-far) (meters 1))(begin(set! (-> *TARGET-bank* fall-far) (meters 30))(set! (-> *TARGET-bank* fall-far-inc) (meters 20)))(begin (set! (-> *TARGET-bank* fall-far) (meters 1))(set! (-> *TARGET-bank* fall-far-inc) (meters 1))))")
			message = ""
		
		if "!basincell" == message.lower():
			sendForm("(if (when (process-by-ename \"fuel-cell-45\") (= (-> (->(the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans x)  (meters -266.54)))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -248.92) (meters 52.11) (meters -1515.66) 1.0))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -266.54) (meters 52.11) (meters -1508.48) 1.0)))")
			message = ""
		
		if "!frickstorage" == message.lower():
			sendForm("(stop 'debug)")
			time.sleep(0.001)
			sendForm("(start 'debug (get-or-create-continue! *game-info*))")
			message = ""
		
		if "!freecam" == message.lower():
			sendForm("(stop 'debug)")
			time.sleep(6)
			sendForm("(start 'play (get-or-create-continue! *game-info*))")
			message = ""
		
		if "!invertcam" == message.lower():
			sendForm("(stop 'debug)")
			time.sleep(6)
			sendForm("(set! (-> *pc-settings* " + arg(1) + "-camera-" + arg(2) + "-inverted?) (not (-> *pc-settings* " + arg(1) + "-camera-" + arg(2) + "-inverted?)))")
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
					print(user + " : " + message)
				except Exception:
					pass

def main():
	if __name__ =='__main__':
		t1 = threading.Thread(target = twitch)
		t1.start()
		t2 = threading.Thread(target = gamecontrol)
		t2. start()
main()