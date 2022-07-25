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
CONNECTIONMESSAGE = str(os.getenv("CONNECTIONMESSAGE"))
MOTD = "u playing jak?"
#GPATH = r"c:\Users\Yop\source\repos\jak-project"
print(PATHTOGK)
print(PATHTOGOALC)

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

sendForm("(lt)")
sendForm("(mi)")

sendForm("(send-event *target* 'get-pickup (pickup-type eco-blue) 1.0)")








#Download Autohotkey at https://www.autohotkey.com/ and provide the address to
#AutoHotkey.exe below!
PATHTOAHK = str(os.getenv("PATHTOAHK"))

ahk = AHK(executable_path=PATHTOAHK)

SERVER = "irc.twitch.tv"
PORT = 6667

#Your OAUTH Code Here https://twitchapps.com/tmi/


#What you'd like to name your bot
BOT = "TwitchBot"

#The channel you want to monitor
CHANNEL = str(os.getenv("TARGETCHANNEL"))

#Your account
OWNER = "zed_b0t"

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

		if "trip" == message.lower():
			sendForm("(send-event *target* 'loading)")
			message = ""

		if "down" == message.lower():
			ahk.key_press('down')
			message = ""

		if "left" == message.lower():
			ahk.key_press('left')
			message = ""

		if "right" == message.lower():
			ahk.key_press('right')
			message = ""

		if "a" == message.lower():
			ahk.key_press('z')
			message = ""

		if "b" == message.lower():
			ahk.key_press('x')
			message = ""

		if "lb" == message.lower():
			ahk.key_press('a')
			message = ""

		if "rb" == message.lower():
			ahk.key_press('s')
			message = ""

		if "select" == message.lower():
			ahk.key_press('d')
			message = ""

		if "start" == message.lower():
			ahk.key_press('enter')
			message = ""

		if "test" == message.lower():
			print("test")
			print(message)
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