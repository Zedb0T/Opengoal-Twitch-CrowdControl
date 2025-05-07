import socket
import threading
import os
import struct
import subprocess
import time
import sys
import psutil
import random
from dotenv import load_dotenv
from os.path import exists
from tkinter import ttk
import shutil
import tkinter as tk
import math

"""
Created on Fri Apr 29 16:20:54 2022
@author: Yop Mike Zed
"""
# Set the working directory
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)

if (exists(".env.txt")):
    if(exists(".env")):
        shutil.remove(".env")
    os.replace(".env.txt", ".env")

if(exists("env")):
    os.replace("env",".env")

# env values
load_dotenv()
OAUTH = os.getenv("OAUTH")
CONNECT_MSG = os.getenv("CONNECT_MSG")
COOLDOWN_MSG = os.getenv("COOLDOWN_MSG") != "f"
DISABLED_MSG = os.getenv("DISABLED_MSG") != "f"
ACTIVATION_MSG = os.getenv("ACTIVATION_MSG") != "f"
DEACTIVATION_MSG = os.getenv("DEACTIVATION_MSG") != "f"
VALUE_MSG = os.getenv("VALUE_MSG") != "f"
PROTECT_SACRIFICE = "f"
SACRIFICE_DURATION = os.getenv("SACRIFICE_DURATION")
PREFIX = os.getenv("PREFIX")
TARGET_ID = os.getenv("TARGET_ID")

FIRST_CAMERA_V_INVERTED = os.getenv("first-camera-vertical-inverted")
FIRST_CAMERA_H_INVERTED = os.getenv("first-camera-horizontal-inverted")
THIRD_CAMERA_V_INVERTED = os.getenv("third-camera-vertical-inverted")
THIRD_CAMERA_H_INVERTED = os.getenv("third-camera-horizontal-inverted")

TOPOINT_PAST_CRATER = os.getenv("TOPOINT_PAST_CRATER") != "f"
ALL_ACTORS = os.getenv("ALL_ACTORS") != "f"
cost_mode = os.getenv("COST_MODE") != "f"

SHIFTX_MIN = os.getenv("SHIFTX_MIN")
SHIFTX_MAX = os.getenv("SHIFTX_MAX")
SHIFTY_MIN = os.getenv("SHIFTY_MIN")
SHIFTY_MAX = os.getenv("SHIFTY_MAX")
SHIFTZ_MIN = os.getenv("SHIFTZ_MIN")
SHIFTZ_MAX = os.getenv("SHIFTZ_MAX")
GIVE_MIN = os.getenv("GIVE_MIN")
GIVE_MAX = os.getenv("GIVE_MAX")
RJTO_MIN = os.getenv("RJTO_MIN")
RJTO_MAX = os.getenv("RJTO_MAX")
SCALE_MIN = os.getenv("SCALE_MIN")
SCALE_MAX = os.getenv("SCALE_MAX")
MINUSCELL_AMT = os.getenv("MINUSCELL_AMT")
PLUSCELL_AMT = os.getenv("PLUSCELL_AMT")
MINUSORBS_AMT = os.getenv("MINUSORBS_AMT")
PLUSORBS_AMT = os.getenv("PLUSORBS_AMT")
SUCK_MIN = os.getenv("SUCK_MIN")
SUCK_MAX = os.getenv("SUCK_MAX")
BLIND_MIN = os.getenv("BLIND_MIN")
BLIND_MAX = os.getenv("BLIND_MAX")
MAXFISH_MIN = os.getenv("MAXFISH_MIN")
MAXFISH_MAX = os.getenv("MAXFISH_MAX")

game = os.getenv("LOAD_STARTED") != "f"
FINALBOSS_MUL = 2
finalboss_mode = False
target_mode = os.getenv("TARGET_MODE") != "f"
INIT_BALANCE = 1000

# bool that checks if its the launcher version
launcher_version = exists(application_path+"\\OpenGOAL-Launcher.exe")

# checks
if not exists(".env"):
    print("ERROR: .env file not found -- please check if it is in the same folder as gk.exe and Jak1Twitch.exe")
    time.sleep(936814)

if (len(OAUTH) != 36) or (OAUTH[0:6] != "oauth:"):
    print("ERROR: Invalid ouath -- please get new oauth from: https://twitchapps.com/tmi/")
    time.sleep(936814)
    
# paths
PATHTOGOALC = application_path + "\\goalc.exe"
PATHTOGK = application_path +"\\gk.exe -v -- -boot -fakeiso -debug"

# If its the launcher version update the paths!
if launcher_version:
    print("launcher version detected")
    shutil.copyfile(application_path+"/goalc.exe", os.getenv('APPDATA') +"\\OpenGOAL-Launcher\\goalc.exe")
    time.sleep(1)
    PATHTOGOALC=os.getenv('APPDATA') +"\\OpenGOAL-Launcher\\goalc.exe"
    extraGKCommand = "-proj-path "+os.getenv('APPDATA') +"\\OpenGOAL-Launcher\\data "
    PATHTOGK = application_path +"\\gk.exe "+extraGKCommand+" -v -- -boot -fakeiso -debug"

# Function definitions
def sendForm(form):
    header = struct.pack('<II', len(form), 10)
    clientSocket.sendall(header + form.encode())
    print("Sent: " + form)
    return

active_list = []
active_list_times = []

def display_text_in_window():
    # Create a new window
    window = tk.Tk()
    window.title("J1T Active Effects")
    window.geometry("300x320")  # Set a window size

    # Position the window on the right side of the screen
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = screen_width - 450  # Align to the right side
    y = (screen_height // 2) - (320 // 2)
    window.geometry(f'{300}x{320}+{x}+{y}')

    # Create a frame to hold the text widget and scrollbar
    frame = ttk.Frame(window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    light_mode = {
        "bg": "#ffffff",
        "fg": "#000000",
        "insertbackground": "#000000",
        "highlightbackground": "#cccccc",
    }

    dark_mode = {
        "bg": "#333333",
        "fg": "#ffffff",
        "insertbackground": "#00ff00",
        "highlightbackground": "#4d4d4d",
    }

    current_mode = dark_mode

    # Create a text widget with a scrollbar
    text_widget = tk.Text(frame, wrap="word", height=10, width=30, 
                          bg=current_mode["bg"],  
                          fg=current_mode["fg"],  
                          insertbackground=current_mode["insertbackground"],  
                          highlightbackground=current_mode["highlightbackground"], 
                          highlightcolor=current_mode["highlightbackground"], 
                          borderwidth=0, 
                          relief="flat")
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.config(yscrollcommand=scrollbar.set)

    # Configure the font
    font_style = ("Franklin Gothic Medium", 14, "bold")
    text_widget.configure(font=font_style)

    # Function to update text in the text widget
    def update_text():
        text_content = ''
        for effect, time_remaining in zip(active_list, active_list_times):
            hours = int(time_remaining) // 3600
            minutes = (int(time_remaining) % 3600) // 60
            seconds = int(time_remaining) % 60
            if hours > 0:
                formatted_time = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                formatted_time = f"{minutes}:{seconds:02d}"
            if effect != "fakewarp":
                text_content += f"{effect} ~ {formatted_time}\n"
        
        text_widget.delete(1.0, tk.END)  # Clear existing text
        text_widget.insert(tk.END, text_content)

        for i in range(len(active_list_times)):
            total_duration = durations[command_names.index(active_list[i])]
            start_time = activated[command_names.index(active_list[i])]
            elapsed_time = time.time() - start_time
            remaining_time = max(0, total_duration - elapsed_time)
            active_list_times[i] = math.floor(remaining_time)
        
        # Schedule the next update
        if window.winfo_exists():
            window.after(1000, update_text)
    
    update_text()

    # Function to toggle between light and dark mode
    def toggle_mode():
        nonlocal current_mode
        current_mode = light_mode if current_mode == dark_mode else dark_mode
        
        text_widget.configure(
            bg=current_mode["bg"],
            fg=current_mode["fg"],
            insertbackground=current_mode["insertbackground"],
            highlightbackground=current_mode["highlightbackground"],
            highlightcolor=current_mode["highlightbackground"]
        )

    # Add a button to toggle light/dark mode
    toggle_button = ttk.Button(window, text="Toggle Light/Dark Mode", command=toggle_mode)
    toggle_button.pack(pady=10)

    window.mainloop()

# Main program logic
def main_program_logic():
    print(f"Main Program:")

main_thread = threading.Thread(target=main_program_logic)
main_thread.start()

# Start the thread for displaying text in the window
display_thread = threading.Thread(target=display_text_in_window)
display_thread.start()

# Wait for the main program thread to finish
main_thread.join()

def target_check(line):
    if target_mode:
        if line[len(line) - 1].lower() == TARGET_ID.lower() or line[len(line) - 1].lower() == "all":
            return True
        else:
            return False
    else:
        return True

def cd_check(cmd):
    global message
    idx = command_names.index(cmd)
    if (time.time() - last_used[idx]) > cooldowns[idx]:
        last_used[idx] = time.time()
        return True
    elif COOLDOWN_MSG:
        remaining_time = int(cooldowns[idx] - (time.time() - last_used[idx]))
        
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        
        if hours > 0:
            time_string = f"{hours}:{minutes:02}:{seconds:02}s"
        else:
            time_string = f"{minutes}:{seconds:02}s"
        
        sendMessage(irc, f"/me @{user} {TARGET_ID} -> Command '{command_names[idx]}' is on cooldown ({time_string} left).")
        return False
    else:
        return False

def enabled_check(cmd):
    global message
    try:
        if enabled[command_names.index(cmd)] and not active[command_names.index("protect")] and not (finalboss_mode and cmd in finalboss_toggle_commands):
            return cost_check(cmd, user) 
        elif DISABLED_MSG:
            sendMessage(irc, f"/me @{user} {TARGET_ID} -> Command '{command_names[command_names.index(cmd)]}' is disabled.")
            #message = ""
            return False
        else:
            #message = ""
            return False
    except (ValueError, TypeError):
        sendMessage(irc, f"/me @{user} {TARGET_ID} -> Error processing command.")
        return False

def active_check(cmd, line1):
    if not active[command_names.index(cmd)]:
        sendForm(line1)
        activate(cmd)
    else:
        sendForm(command_deactivation[cmd])
        deactivate(cmd)

command_deactivation = {
    "rjto": "(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))(set! (-> *TARGET-bank* wheel-flip-height) (meters 3.52))",
    "superjump": "(set! (-> *TARGET-bank* jump-height-max)(meters 3.5))(set! (-> *TARGET-bank* jump-height-min)(meters 1.01))(set! (-> *TARGET-bank* double-jump-height-max)(meters 2.5))(set! (-> *TARGET-bank* double-jump-height-min)(meters 1))",
    "leapfrog": "(set! (-> *TARGET-bank* duck-jump-height-max)(meters 7))(set! (-> *TARGET-bank* duck-jump-height-min)(meters 5))",
    "superboosted": "(set! (-> *edge-surface* fric) 30720.0)",
    "noboosteds": "(set! (-> *edge-surface* fric) 30720.0)",
    "nojumps": "(logclear! (-> *target* state-flags) (state-flags prevent-jump))",
    "nodive": "(set! (-> *TARGET-bank* min-dive-depth) (meters 2))",
    "noduck": "(logclear! (-> *target* state-flags) (state-flags prevent-duck))",
    "noledge": "(set! (-> *collide-edge-work* max-dir-cosa-delta) 0.6)",
    "fastjak": "(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *forward-high-jump-mods* target-speed) 45056.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *flip-jump-mods* target-speed) 51200.0)(set! (-> *high-jump-mods* target-speed) 26624.0)(set! (-> *smack-jump-mods* target-speed) 40960.0)(set! (-> *duck-attack-mods* target-speed) 16384.0)(set! (-> *flop-mods* target-speed) 40960.0)(set! (-> *stone-surface* target-speed) 1.25)",
    "slowjak": "(set! (-> *walk-mods* target-speed) 40960.0)(set! (-> *double-jump-mods* target-speed) 32768.0)(set! (-> *jump-mods* target-speed) 40960.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *attack-mods* target-speed) 40960.0)(set! (-> *forward-high-jump-mods* target-speed) 45056.0)(set! (-> *jump-attack-mods* target-speed) 24576.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))(set! (-> *TARGET-bank* wheel-flip-height) (meters 3.52))",
    "pacifist": "(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 2.2))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1))",
    #"bigspin": "(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 2.2))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1))(set! (-> *TARGET-bank* spin-offset y) 6553.6)",
    "shortfall": "(set! (-> *TARGET-bank* fall-far) (meters 30))(set! (-> *TARGET-bank* fall-far-inc) (meters 20))",
    "ghostjak": "(set! (-> *TARGET-bank* body-radius) (meters 0.7))",
    "freecam": "(start 'play (get-or-create-continue! *game-info*))",
    "sucksuck": "(set! (-> *FACT-bank* suck-suck-dist) (meters 12))(set! (-> *FACT-bank* suck-bounce-dist) (meters 12))",
    "noeco": "(set! (-> *FACT-bank* eco-full-timeout) (seconds 20.0))",
    "rapidfire": "(set! (-> *TARGET-bank* yellow-projectile-speed) (meters 60))(set! (-> *TARGET-bank* yellow-attack-timeout) (seconds 0.2))",
    "invertcam": f"(set! (-> *pc-settings* third-camera-h-inverted?) #{THIRD_CAMERA_H_INVERTED})(set! (-> *pc-settings* third-camera-v-inverted?) #{THIRD_CAMERA_V_INVERTED})(set! (-> *pc-settings* first-camera-v-inverted?) #{FIRST_CAMERA_V_INVERTED})(set! (-> *pc-settings* first-camera-h-inverted?) #{FIRST_CAMERA_H_INVERTED})",
    "stickycam": "(send-event *target* 'no-look-around (seconds 0))(send-event *camera* 'change-state cam-string 0)",
    "cam": "(send-event *camera* 'change-state cam-string 0)",
    "tiktok": "(set! (-> *pc-settings* aspect-ratio) *chosen-ratio*)",
    "askew": "(set! (-> *standard-dynamics* gravity x) 0.0)",
    "gravity": "(set! (-> *standard-dynamics* gravity-length) GRAVITY_AMOUNT)(set! (-> *standard-dynamics* gravity y) GRAVITY_AMOUNT)",
    "dark": "(set! (-> *dark-level* mood-func)update-mood-darkcave)",
    "nodax": "(send-event *target* 'sidekick #t)",
    "smallnet": "(when (process-by-ename \"fisher-1\")(set! (-> *FISHER-bank* net-radius)(meters 0.7)))",
    "widefish": "(when (process-by-ename \"fisher-1\")(set! (-> *FISHER-bank* width)(meters 3.3)))",
    "hardfish": "(when (process-by-ename \"fisher-1\")(set! (-> (the fisher (process-by-ename \"fisher-1\")) difficulty) 0)(set! (-> *FISHER-bank* max-caught) 200))",
    "lowpoly": "(set! (-> *pc-settings* lod-force-tfrag) 0)(set! (-> *pc-settings* lod-force-tie) 0)(set! (-> *pc-settings* lod-force-ocean) 0)(set! (-> *pc-settings* lod-force-actor) 0)",
    "widejak": "(set! (-> (-> (the-as target *target* )root)scale x) 1.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)",
    "flatjak": "(set! (-> (-> (the-as target *target* )root)scale x) 1.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)",
    "smalljak": "(set! (-> (-> (the-as target *target* )root)scale x) 1.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))",
    "bigjak": "(set! (-> (-> (the-as target *target* )root)scale x) 1.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)",
    "color": "(set! (-> *target* draw color-mult x) 1.0)(set! (-> *target* draw color-mult y) 1.0)(set! (-> *target* draw color-mult z) 1.0)",
    "scale": "(set! (-> (-> (the-as target *target* )root)scale x) 1.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)",
    "slippery": "(set! (-> *stone-surface* slope-slip-angle) 8192.0)(set! (-> *stone-surface* slip-factor) 1.0)(set! (-> *stone-surface* transv-max) 1.0)(set! (-> *stone-surface* turnv) 1.0)(set! (-> *stone-surface* nonlin-fric-dist) 5120.0)(set! (-> *stone-surface* fric) 153600.0)(set! (-> *grass-surface* slope-slip-angle) 16384.0)(set! (-> *grass-surface* slip-factor) 1.0)(set! (-> *grass-surface* transv-max) 1.0)(set! (-> *grass-surface* turnv) 1.0)(set! (-> *grass-surface* nonlin-fric-dist) 4096.0)(set! (-> *grass-surface* fric) 122880.0)(set! (-> *ice-surface* slip-factor) 0.7)(set! (-> *ice-surface* nonlin-fric-dist) 4091904.0)(set! (-> *ice-surface* fric) 23756.8)",
    "pinball": "(set! (-> *stone-surface* fric) 153600.0)",
    "protect": "",
    "iframes": "(set! (-> *TARGET-bank* hit-invulnerable-timeout) (seconds 3.0))",
    "rocketman": "(set! (-> *standard-dynamics* gravity-normal y) 1.0)",
    "bighead": "(logclear! (-> *pc-settings* cheats) (pc-cheats big-head))",
    "smallhead": "(logclear! (-> *pc-settings* cheats) (pc-cheats small-head))",
    "bigfist": "(logclear! (-> *pc-settings* cheats) (pc-cheats big-fist))",
    "bigheadnpc": "(logclear! (-> *pc-settings* cheats) (pc-cheats big-head-npc))",
    "hugehead": "(logclear! (-> *pc-settings* cheats) (pc-cheats huge-head))",
    "mirror": "(logclear! (-> *pc-settings* cheats) (pc-cheats mirror))",
    "invuln": "(logclear! (-> *pc-settings* cheats) (pc-cheats invinc))(logclear! (-> *target* state-flags) (state-flags invulnerable))",
    "notex": "(logclear! (-> *pc-settings* cheats) (pc-cheats no-tex))",
    "noactors": "(set! *spawn-actors* #t) (reset-actors 'debug)",
    "spiderman": "(set! (-> *pat-mode-info* 1 wall-angle) 2.0) (set! (-> *pat-mode-info* 2 wall-angle) 0.82)",
    "statue": "(logclear! (-> *target* mask) (process-mask sleep))",
    "fakewarp": "(set! (-> *setting-control* default music-volume) *target-music-volume*)(set! (-> *setting-control* default sfx-volume) *target-sfx-volume*)(set! (-> *setting-control* default ambient-volume) *target-ambient-volume*)(set! (-> *setting-control* default dialog-volume) *target-dialog-volume*)",
    "crazyplats": "(when (process-by-ename \"pontoonten-10\")(set! (-> *pontoonten-constants* player-weight) (meters 35)))(when (process-by-ename \"pontoonfive-6\")(set! (-> *pontoonfive-constants* player-weight) (meters 35)))(when (process-by-ename \"tra-pontoon-3\")(set! (-> *tra-pontoon-constants* player-weight) (meters 35)))(when (process-by-ename \"citb-chain-plat-14\")(set! (-> *citb-chain-plat-constants* player-weight) (meters 35)))(when (process-by-ename \"qbert-plat-7\")(set! (-> *qbert-plat-constants* player-weight) (meters 35)))(when (process-by-ename \"tar-plat-21\")(set! (-> *tar-plat-constants* player-weight) (meters 60)))(when (process-by-ename \"ogre-step-a-2\")(set! (-> *ogre-step-constants* player-weight) (meters 35)))(when (process-by-ename \"ogre-isle-c-1\")(set! (-> *ogre-isle-constants* player-weight) (meters 35)))(when (process-by-ename \"bone-platform-4\")(set! (-> *bone-platform-constants* player-weight) (meters 35)))"
}
        
def active_sweep():
    for i, cmd in enumerate(active_list):
        try:
            if (time.time() - activated[command_names.index(cmd)]) >= durations[command_names.index(cmd)]:
                deactivate(cmd)
        except (ValueError, TypeError):
            None

def activate(cmd):
    idx = command_names.index(cmd)
    if ACTIVATION_MSG:
        sendMessage(irc, f"/me {TARGET_ID} -> '{command_names[idx]}' activated!")
    activated[idx] = time.time()
    active[idx] = True
    active_list.append(cmd)
    active_list_times.append(durations[idx])

def deactivate(cmd):
    idx = command_names.index(cmd)
    if active[idx]:
        if DEACTIVATION_MSG:
            sendMessage(irc, f"/me {TARGET_ID} -> '{command_names[idx]}' deactivated!")
        active[idx] = False
        del active_list_times[active_list.index(cmd)]
        active_list.remove(cmd)
        sendForm(command_deactivation[cmd])


def range_check(val, min, max):
    global message
    try:
        float(val)
        if float(val) <= float(max) and float(val) >= float(min):
            return True
        else:
            if VALUE_MSG:
                sendMessage(irc, f"/me @{user} Use values between {min} and {max}. (val {val})")
            #message = ""
            return False
    except ValueError:
        return False
    
def cost_check(cmd, user):
    if cost_mode:
        user_credit = credit_list[user_list.index(user)]
        cost = costs[command_names.index(cmd)]
        if user_credit >= cost:
            credit_list[user_list.index(user)] -= cost
            return True
        else:
            sendMessage(irc, f"/me @{user} Not enough credit! Have: {user_credit} Need: {cost}.")
        #message = ""
    else:
        return True
    
def get_random_point(nickname):
    points = point_nicknames.get(nickname)
    if points:
        return random.choice(points)
    return None

def adjust_finalboss_cooldowns(commands, multiplier, divide=False):
    for command in commands:
        if divide:
            cooldowns[command_names.index(command)] /= multiplier
        else:
            cooldowns[command_names.index(command)] *= multiplier

# Launch REPL, connect bot, and mi

# This splits the Gk commands into args for gk.exe
GKCOMMANDLINElist = PATHTOGK.split()

# Close Gk and goalc if they were open.
print("If it errors below that is O.K.")
subprocess.Popen("""taskkill /F /IM gk.exe""",shell=True)  # COMMENT OUT FOR TEAMRUNS
subprocess.Popen("""taskkill /F /IM goalc.exe""",shell=True)
time.sleep(2)

def terminate_other_instances(process_name):
    """
    Terminates all processes with the given name, except the current process.
    :param process_name: The name of the process to kill (e.g., 'example.exe').
    """
    current_pid = os.getpid()
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == process_name and proc.info['pid'] != current_pid:
                print(f"Terminating process {proc.info['name']} with PID {proc.info['pid']}")
                # Use taskkill via subprocess to terminate the process by its PID
                subprocess.Popen(f'taskkill /F /PID {proc.info["pid"]}', shell=True)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

terminate_other_instances('Jak1Twitch.exe') # Jak1TwitchTR.exe FOR TEAMRUNS

# Open a fresh GK and goalc then wait a bit before trying to connect via socket
print("opening " + PATHTOGK)  # COMMENT OUT FOR TEAMRUNS
print("opening " + PATHTOGOALC)
GK_WIN = subprocess.Popen(GKCOMMANDLINElist)  # COMMENT OUT FOR TEAMRUNS
GOALC_WIN = subprocess.Popen([PATHTOGOALC])
time.sleep(3)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("127.0.0.1", 8181))
time.sleep(1)
data = clientSocket.recv(1024)
print(data.decode())

# Int block these comamnds are sent on startup
sendForm("(lt)")
sendForm("(mi)")
sendForm("(send-event *target* 'get-pickup (pickup-type eco-red) 5.0)")
#sendForm("(dotimes (i 1) (sound-play-by-name (static-sound-name \"cell-prize\") (new-sound-id) 1024 0 0 (sound-group sfx) #t))")
sendForm("(set! *cheat-mode* #f)")
sendForm("(set! *debug-segment* #f)")  # COMMENT OUT FOR TEAMRUNS
sendForm("(define *dark-level* (level-get-target-inside *level*))")
sendForm("(define *chosen-ratio* (-> *pc-settings* aspect-ratio))")
sendForm("(define *target-dialog-volume* (-> *setting-control* default dialog-volume))(define *target-sfx-volume* (-> *setting-control* default sfx-volume))(define *target-music-volume* (-> *setting-control* default music-volume))(define *target-ambient-volume* (-> *setting-control* default ambient-volume))")
if ALL_ACTORS:
    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #f)")
else:
    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #t)")
sendForm("(set! (-> *pc-settings* speedrunner-mode?) #f)")
# End Int block

# add all commands into an array so we can reference via index
command_names = ["protect","rjto","superjump","leapfrog","superboosted","noboosteds","nojumps","nodive","noduck","noledge","fastjak","slowjak","pacifist","nuka","invuln","trip",
                 "shortfall","ghostjak","getoff","freecam","give","minuscell","pluscell","minusorbs","plusorbs","collected",
                 "eco","rapidfire","sucksuck","noeco","die","topoint","randompoint","tp","shift","movetojak","ouch",
                 "burn","hp","melt","drown","endlessfall","iframes","invertcam","cam","stickycam","deload","earthquake","fakewarp",
                 "quickcam","dark","blind","nodax","smallnet","widefish","maxfish","hardfish","customfish","lowpoly","moveplantboss","moveplantboss2",
                 "basincell","resetactors","noactors","repl","debug","save","actors-on","actors-off","askew",
                 "widejak","flatjak","smalljak","bigjak","color","scale","slippery","gravity","pinball","playhint","rocketman","sfx",
                 "unzoom","bighead","smallhead","bigfist","bigheadnpc","hugehead","mirror","notex","spiderman","press","pause",
                 "lang","timeofday","statue","turn-left","turn-right","turn-180","cam-left","cam-right","cam-in","cam-out","tiktok","crazyplats","setpoint"]

# array of valid checkpoints so user cant send garbage data
point_list = ["training-start","game-start","village1-hut","village1-warp","beach-start",
              "jungle-start","jungle-tower","misty-start","misty-silo","misty-bike",
              "misty-backside","misty-silo2","firecanyon-start","firecanyon-end",
              "village2-start","village2-warp","village2-dock","rolling-start",
              "sunken-start","sunken1","sunken2","sunken-tube1","sunkenb-start",
              "sunkenb-helix","swamp-start","swamp-dock1","swamp-cave1","swamp-dock2",
              "swamp-cave2","swamp-game","swamp-cave3","ogre-start","ogre-race","ogre-end",
              "village3-start","village3-warp","village3-farside","maincave-start",
              "maincave-to-darkcave","maincave-to-robocave","darkcave-start","robocave-start",
              "robocave-bottom","snow-start","snow-fort","snow-flut-flut","snow-pass-to-fort",
              "snow-by-ice-lake","snow-by-ice-lake-alt","snow-outside-fort","snow-outside-cave",
              "snow-across-from-flut","lavatube-start","lavatube-middle","lavatube-after-ribbon",
              "lavatube-end","citadel-start","citadel-entrance","citadel-warp","citadel-launch-start",
              "citadel-launch-end","citadel-generator-start","citadel-generator-end","citadel-plat-start",
              "citadel-plat-end","citadel-elevator","finalboss-start","finalboss-fight"]

point_nicknames = {
    "geyser": ("training-start"),
    "training": ("training-start"),
    "sandover": ("village1-hut", "village1-warp"),
    "village1": ("village1-hut", "village1-warp"),
    "misty": ("misty-start", "misty-silo", "misty-bike", "misty-backside", "misty-silo2"),
    "sentinel": ("beach-start"),
    "beach": ("beach-start"),
    "fj": ("jungle-start", "jungle-tower"),
    "jungle": ("jungle-start", "jungle-tower"),
    "fc": ("firecanyon-start", "firecanyon-end"),
    "firecanyon": ("firecanyon-start", "firecanyon-end"),
    "rv": ("village2-start", "village2-warp", "village2-dock"),
    "rockvillage": ("village2-start", "village2-warp", "village2-dock"),
    "village2": ("village2-start", "village2-warp", "village2-dock"),
    "lpc": ("sunken-start", "sunken1", "sunken2", "sunken-tube1", "sunkenb-start", "sunkenb-helix"),
    "sunken": ("sunken-start", "sunken1", "sunken2", "sunken-tube1", "sunkenb-start", "sunkenb-helix"),
    "basin": ("rolling-start"),
    "rolling": ("rolling-start"),
    "boggy": ("swamp-start", "swamp-dock1", "swamp-cave1", "swamp-dock2", "swamp-cave2", "swamp-game", "swamp-cave3"),
    "boggyswamp": ("swamp-start", "swamp-dock1", "swamp-cave1", "swamp-dock2", "swamp-cave2", "swamp-game", "swamp-cave3"),
    "swamp": ("swamp-start", "swamp-dock1", "swamp-cave1", "swamp-dock2", "swamp-cave2", "swamp-game", "swamp-cave3"),
    "mp": ("ogre-start", "ogre-end"),
    "mountainpass": ("ogre-start", "ogre-end"),
    "ogre": ("ogre-start", "ogre-end"),
    "vc": ("village3-start", "village3-warp", "village3-farside"),
    "crater": ("village3-start", "village3-warp", "village3-farside"),
    "village3": ("village3-start", "village3-warp", "village3-farside"),
    "sc": ("maincave-start", "maincave-to-darkcave", "maincave-to-robocave", "darkcave-start", "robocave-start", "robocave-bottom"),
    "cave": ("maincave-start", "maincave-to-darkcave", "maincave-to-robocave", "darkcave-start", "robocave-start", "robocave-bottom"),
    "spidercave": ("maincave-start", "maincave-to-darkcave", "maincave-to-robocave", "darkcave-start", "robocave-start", "robocave-bottom"),
    "snowy": ("snow-start", "snow-fort", "snow-flut-flut", "snow-pass-to-fort", "snow-by-ice-lake", "snow-by-ice-lake-alt", "snow-outside-fort", "snow-outside-cave", "snow-across-from-flut"),
    "snow": ("snow-start", "snow-fort", "snow-flut-flut", "snow-pass-to-fort", "snow-by-ice-lake", "snow-by-ice-lake-alt", "snow-outside-fort", "snow-outside-cave", "snow-across-from-flut"),
    "lt": ("lavatube-start", "lavatube-middle", "lavatube-after-ribbon", "lavatube-end"),
    "lavatube": ("lavatube-start", "lavatube-middle", "lavatube-after-ribbon", "lavatube-end"),
    "citadel": ("citadel-start", "citadel-entrance", "citadel-warp", "citadel-launch-start", "citadel-launch-end", "citadel-generator-start", "citadel-generator-end", "citadel-plat-start", "citadel-plat-end", "citadel-elevator", "finalboss-start", "finalboss-fight"),
    "gmc": ("citadel-start", "citadel-entrance", "citadel-warp", "citadel-launch-start", "citadel-launch-end", "citadel-generator-start", "citadel-generator-end", "citadel-plat-start", "citadel-plat-end", "citadel-elevator", "finalboss-start", "finalboss-fight"),
    "gamc": ("citadel-start", "citadel-entrance", "citadel-warp", "citadel-launch-start", "citadel-launch-end", "citadel-generator-start", "citadel-generator-end", "citadel-plat-start", "citadel-plat-end", "citadel-elevator", "finalboss-start", "finalboss-fight")
}

sfx_names = {
    "shark": "bigshark-idle",
    "breathe": "breathe-in-loud",
    "breathe2": "breath-out-loud",
    "breathe3": "swim-noseblow",
    "explode": "dcrate-break",
    "explode2": "explosion",
    "explode3": "explosion-2",
    "explode4": "zoomer-explode",
    "explode5": "blob-explode",
    "launch": "launch-fire",
    "menu": "select-menu",
    "menu2": "menu-close",
    "menu3": "select-option2",
    "powerup": "powercell-out",
    "uppercut": "uppercut",
    "punch": "punch-hit",
    "bonk": "smack-surface",
    "cell": "cell-prize",
    "shutdown": "shut-down",
    "startup": "start-up",
    "warning": "warning",
    "warning2": "robo-warning",
    "death": "jak-deatha",
    "drown": "death-drown",
    "fall": "death-fall",
    "melt": "death-melt",
    "darkeco": "death-darkeco",
    "grunt": "grunt",
    "stretch": "jak-stretch",
    "clap": "jak-clap",
    "orb": "money-pickup",
    "eel": "caught-eel",
    "shock": "get-shocked",
    "shock2": "jak-shocked",
    "allorbs": "get-all-orbs",
    "dizzy": "hit-dizzy",
    "miss": "fish-miss",
    "ring": "close-racering"
}

lang_list = ["english","french","german","spanish","italian","japanese","uk-english"]
pad_list = ["square","circle","x","triangle","up","down","left","right","l1","r1"]
cam_list = ["endlessfall","eye","standoff","bike","stick"]
fish_list = ["timeout","vel","swing-min","swing-max","period","fish-vel","bad-percent","powerup-percent"]
eco_list = ["blue","yellow","red","green"]

# intialize arrays same length as command_names
enabled = [True] * len(command_names)
cooldowns = [0.0] * len(command_names)
costs = [0.0] * len(command_names)
last_used = [0.0] * len(command_names)
activated = [0.0] * len(command_names)
durations = [0.0] * len(command_names)
active = [False] * len(command_names)
user_list = []
credit_list = []

finalboss_toggle_commands = [
    "die", "drown", "melt", "endlessfall", "resetactors", "deload", "noledge",
    "ghostjak", "shift", "tp", "topoint", "randompoint", "movetojak", "noactors", "pinball"]

def increase_credits():
    while True:
        if cost_mode:
            for i in range(len(user_list)):
                credit_list[i] += 5
                #print(f"{user_list[i]} now has {credit_list[i]} credits.")
        time.sleep(30)

thread = threading.Thread(target=increase_credits)
thread.daemon = True
thread.start()

# pull cooldowns and costs set in env file and add to array
for x in range(len(command_names)):
    try:
        cooldowns[x] = float(os.getenv(command_names[x]+"_cd"))
        #print(f"{command_names[x]}_cd = {cooldowns[x]}")
    except (TypeError, ValueError):
        print(f"Could not find cooldown for {command_names[x]}")
    try:
        enabled[x] = os.getenv(command_names[x]) != "f"
        #print(f"{command_names[x]} = {enabled[x]}")
    except (TypeError, ValueError):
        print(f"Could not find {command_names[x]}")
    try:
        costs[x] = float(os.getenv(command_names[x]+"_cost"))
        #print(f"{command_names[x]}_cost = {costs[x]}")
    except (TypeError, ValueError):
        print(f"Could not find cost for {command_names[x]}")

# pull durations set in env file and add to array
for x in range(len(command_names)):
    try:
        durations[x] = float(os.getenv(command_names[x]+"_dur"))
        #print(f"{command_names[x]}_dur = {durations[x]}")
    except (TypeError, ValueError):
        print(f"Could not find duration for {command_names[x]}")
    
# twitch irc stuff
SERVER = "irc.twitch.tv"
PORT = 6667

# Get Your OAUTH Code Here! https://twitchapps.com/tmi/

# What you'd like to name your bot
BOT = "jakopengoalbot"
# The channel you want to monitor
CHANNEL = os.getenv("TARGET_CHANNEL").lower()

# these users can use the REPL command to create custom commands!
COMMAND_ADMINS = ["zed_b0t", "mikegamepro", "water112", "barg034", CHANNEL]
COMMAND_MODS = os.getenv("COMMAND_MODS").lower().split(",")

# initialize empty strings to store user and message
message = ""
user = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((    "PASS " + OAUTH + "\n" +
            "NICK " + BOT + "\n" +
            "JOIN #" + CHANNEL + "\n").encode())

# sends a message to the irc channel.
def sendMessage(irc, message):
    messageTemp = f"PRIVMSG #{CHANNEL} :{message}"
    irc.send((messageTemp + "\n").encode())


def gamecontrol():
    
    global message, game, cost_mode, target_mode

    while True:
        # split a whole message into args so we can evaluate it one by one
        args = message.split(" ")
        command = str(args[0])[1:].lower()

        if target_check(args) and str(args[0]).lower().startswith(PREFIX):

            if command in ["start"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):          
                if game:
                    sendMessage(irc, f"/me {TARGET_ID} -> Game has already started! Use {PREFIX}stop to stop.")
                else:
                    game = True 
                    sendMessage(irc, f"/me {TARGET_ID} -> Game has started! Use {PREFIX}stop to stop.")

            elif command in ["stop"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):          
                if game:
                    game = False
                    sendMessage(irc, f"/me {TARGET_ID} -> Game stopped! Use {PREFIX}start to start.")
                else:
                    sendMessage(irc, f"/me {TARGET_ID} -> Game has not started! Use {PREFIX}start to start.")
                
            if game:

                if cost_mode and user not in user_list:
                    user_list.append(user)
                    credit_list.append(INIT_BALANCE)

                if cost_mode and command in ["balance", "credit"]:
                    sendMessage(irc, f"/me {TARGET_ID} -> @{user} Balance: {credit_list[user_list.index(user)]}") 

                elif command in ["costmode"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):           
                    cost_mode = not cost_mode
                    if cost_mode:
                        sendMessage(irc, f"/me {TARGET_ID} -> Cost Mode enabled!")
                    else:
                        sendMessage(irc, f"/me {TARGET_ID} -> Cost Mode disabled.")

                elif command in ["targetmode"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):           
                    target_mode = not target_mode
                    if target_mode:
                        sendMessage(irc, f"/me {TARGET_ID} -> Target Mode enabled!")
                    else:
                        sendMessage(irc, f"/me {TARGET_ID} -> Target Mode disabled.")

                elif command in ["protect"] and enabled_check("protect") and cd_check("protect"):
                    deactivate("protect")
                    activate("protect")
                    # if PROTECT_SACRIFICE:
                        # sendMessage(irc, "/timeout " + user + " " + str(SACRIFICE_DURATION))
                        # sendMessage(irc, "/me " + user + " sacrificed themselves to protect "+ TARGET_ID + " for " + str(int(durations[command_names.index("protect")])) +"s!")

                elif command in ["rjto", "rj"] and len(args) >= 2 and enabled_check("rjto") and range_check(args[1], RJTO_MIN, RJTO_MAX) and cd_check("rjto"):
                    deactivate("rjto")
                    activate("rjto")
                    sendForm(f"(set! (-> *TARGET-bank* wheel-flip-dist) (meters {args[1]}))(set! (-> *TARGET-bank* wheel-flip-height) (meters {min(max(abs(float(args[1]) / 4.91), 3.52), 7)}))")

                elif command in ["superjump"] and enabled_check("superjump") and cd_check("superjump"):
                    active_check("superjump", 
                    "(set! (-> *TARGET-bank* jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* jump-height-min)(meters 5.0))(set! (-> *TARGET-bank* double-jump-height-max)(meters 15.0))(set! (-> *TARGET-bank* double-jump-height-min)(meters 5.0))")

                elif command in ["leapfrog"] and enabled_check("leapfrog") and cd_check("leapfrog"):
                    active_check("leapfrog", 
                    "(set! (-> *TARGET-bank* duck-jump-height-max)(meters 70))(set! (-> *TARGET-bank* duck-jump-height-min)(meters 50))")

                elif command in ["superboosted", "superboosteds"] and enabled_check("superboosted") and cd_check("superboosted"):
                    deactivate("noboosteds")
                    active_check("superboosted", 
                    "(set! (-> *edge-surface* fric) 1.0)")

                elif command in ["noboosteds", "noboosted"] and enabled_check("noboosteds") and cd_check("noboosteds"):
                    deactivate("superboosted")
                    active_check("noboosteds", 
                    "(set! (-> *edge-surface* fric) 1530000.0)")

                elif command in ["nojumps", "nojump"] and enabled_check("nojumps") and cd_check("nojumps"):
                    active_check("nojumps", 
                    "(logior! (-> *target* state-flags) (state-flags prevent-jump))")

                elif command in ["noduck", "nocrouch"] and enabled_check("noduck") and cd_check("noduck"):
                    active_check("noduck",
                    "(logior! (-> *target* state-flags) (state-flags prevent-duck))")

                elif command in ["nodive", "nodives"] and enabled_check("nodive") and cd_check("nodive"):
                    active_check("nodive",
                    "(set! (-> *TARGET-bank* min-dive-depth) (meters 999))")

                elif command in ["noledge", "noledgegrab"] and enabled_check("noledge") and cd_check("noledge"):
                    active_check("noledge", 
                    "(set! (-> *collide-edge-work* max-dir-cosa-delta) 999.0)")

                elif command in ["fastjak", "fast"] and enabled_check("fastjak") and cd_check("fastjak"):
                    deactivate("slowjak")
                    if not active[command_names.index("smalljak")]:
                        sendForm("(set! (-> *TARGET-bank* wheel-flip-dist) (meters 17.3))")
                    active_check("fastjak", 
                    "(set! (-> *walk-mods* target-speed) 77777.0)(set! (-> *double-jump-mods* target-speed) 77777.0)(set! (-> *jump-mods* target-speed) 77777.0)(set! (-> *jump-attack-mods* target-speed) 77777.0)(set! (-> *attack-mods* target-speed) 77777.0)(set! (-> *forward-high-jump-mods* target-speed) 77777.0)(set! (-> *jump-attack-mods* target-speed) 77777.0)(set! (-> *flip-jump-mods* target-speed) 77777.0)(set! (-> *high-jump-mods* target-speed) 77777.0)(set! (-> *smack-jump-mods* target-speed) 77777.0)(set! (-> *duck-attack-mods* target-speed) 77777.0)(set! (-> *flop-mods* target-speed) 77777.0)(set! (-> *stone-surface* target-speed) 1.25)")

                elif command in ["slowjak", "slow"] and enabled_check("slowjak") and cd_check("slowjak"):
                    deactivate("fastjak")
                    active_check("slowjak",
                    "(send-event *target* 'reset-pickup 'eco)(set! (-> *walk-mods* target-speed) 22000.0)(set! (-> *double-jump-mods* target-speed) 20000.0)(set! (-> *jump-mods* target-speed) 22000.0)(set! (-> *jump-attack-mods* target-speed) 20000.0)(set! (-> *attack-mods* target-speed) 22000.0)(set! (-> *stone-surface* target-speed) 1.0)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 7))(set! (-> *TARGET-bank* wheel-flip-height) (meters 3.52))")

                elif command in ["pacifist"] and enabled_check("pacifist") and cd_check("pacifist"):
                    #deactivate("bigspin")
                    active_check("pacifist", 
                    "(set! (-> *TARGET-bank* punch-radius) (meters -1.0))(set! (-> *TARGET-bank* spin-radius) (meters -1.0))(set! (-> *TARGET-bank* flop-radius) (meters -1.0))(set! (-> *TARGET-bank* uppercut-radius) (meters -1.0))")

                #elif command in ["bigspin"] and enabled_check("bigspin") and cd_check("bigspin"):
                #    deactivate("pacifist")
                #    active_check("bigspin", 
                #    "(set! (-> *TARGET-bank* punch-radius) (meters 1.3))(set! (-> *TARGET-bank* spin-radius) (meters 25))(set! (-> *TARGET-bank* flop-radius) (meters 1.4))(set! (-> *TARGET-bank* uppercut-radius) (meters 1))(set! (-> *TARGET-bank* spin-offset y) 655.6)")
                
                elif command in ["nuka"] and enabled_check("nuka") and cd_check("nuka"):
                    sendForm("(logior! (-> *target* state-flags) (state-flags dying))")

                elif command in ["invuln", "invul"] and enabled_check("invuln") and cd_check("invuln"):
                    active_check("invuln",
                                 "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats invinc)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats invinc)))")

                elif command in ["earthquake", "shake"] and enabled_check("earthquake") and cd_check("earthquake"):
                    sendForm("(activate! *camera-smush-control* 1500.6 12 350 1.0 0.9)")

                elif command in ["trip"] and enabled_check("trip") and cd_check("trip"):
                    sendForm("(send-event *target* 'loading)")

                #elif command in ["bonk"] and enabled_check("bonk") and cd_check("bonk"):
                #    sendForm("(dummy-10 (-> *target* skel effect) 'group-smack-surface (the-as float 0.0) 5)(send-event *target* 'shove)(sound-play \"smack-surface\")")
    
                elif command in ["shortfall"] and enabled_check("shortfall") and cd_check("shortfall"):
                    active_check("shortfall", 
                    "(set! (-> *TARGET-bank* fall-far) (meters 2.5))(set! (-> *TARGET-bank* fall-far-inc) (meters 3.5))")

                elif command in ["ghostjak","ghost"] and enabled_check("ghostjak") and cd_check("deload"):
                    active_check("ghostjak", 
                    "(set! (-> *TARGET-bank* body-radius) (meters -1.0))")              

                elif command in ["getoff", "dismount"] and enabled_check("getoff") and cd_check("getoff"):
                    sendForm("(when (not (movie?))(send-event *target* 'end-mode))")

                elif command in ["unzoom"] and enabled_check("unzoom") and cd_check("unzoom"):
                    sendForm("(send-event *target* 'no-look-around (seconds 0.1))")

                #elif command in ["flutspeed", "setflutflut"] and len(args) >= 2 and enabled_check("flutspeed") and range_check(args[1], -200, 200) and cd_check("flutspeed"):
                #    active_check("flutspeed",
                #                  f"(set! (-> *flut-walk-mods* target-speed)(meters {args[1]}))")
                
                elif command in ["freecam"] and enabled_check("freecam") and cd_check("freecam"):
                    active_check("freecam", 
                    "(stop 'debug)")

                #elif command in ["enemyspeed"] and len(args) >= 3 and enabled_check("enemyspeed") and range_check(args[2], -200, 200) and cd_check("enemyspeed"):
                #    sendForm(f"(set! (-> *{args[1]}-nav-enemy-info* run-travel-speed) (meters {args[2]}))")

                elif command in ["give"] and len(args) >= 3 and enabled_check("give") and range_check(args[2], GIVE_MIN, GIVE_MAX) and cd_check("give"):
                    item = args[1].lower()
                    if item == "cell" or item == "cells":
                        item = "fuel"
                    elif item == "orb" or item == "orbs":
                        item = "money"
                    sendForm("(set! (-> *game-info* " + item + ") (+ (-> *game-info* " + item + ") " + str(args[2]) + "))")

                elif command in ["minuscell", "minuscells"] and enabled_check("minuscell") and cd_check("minuscell"):
                    sendForm("(set! (-> *game-info* fuel)(max 0.0 (- (-> *game-info* fuel) " + MINUSCELL_AMT + ")))")                

                elif command in ["pluscell", "pluscells"] and enabled_check("pluscell") and cd_check("pluscell"):
                    sendForm("(set! (-> *game-info* fuel)(max 0.0 (+ (-> *game-info* fuel) " + PLUSCELL_AMT + ")))")

                elif command in ["minusorbs", "minusorb"] and enabled_check("minusorbs") and cd_check("minusorbs"):
                    sendForm("(set! (-> *game-info* money)(max 0.0 (- (-> *game-info* money) " + MINUSORBS_AMT + ")))")

                elif command in ["plusorbs", "plusorb"] and enabled_check("plusorbs") and cd_check("plusorbs"):
                    sendForm("(set! (-> *game-info* money)(max 0.0 (+ (-> *game-info* money) " + PLUSORBS_AMT + ")))")

                elif command in ["collected", "setcollected"] and len(args) >= 3 and enabled_check("collected") and cd_check("give"):
                    item = args[1].lower()
                    if item == "cell":
                        item = "fuel"
                    elif item == "orb":
                        item = "money"
                    sendForm(f"(set! (-> *game-info* {args[1]}) (+ 0.0 {args[2]}))")

                elif command in ["eco"] and len(args) >= 2 and str(args[1]).lower() in eco_list and enabled_check("eco") and cd_check("eco"):
                    sendForm(f"(send-event *target* 'get-pickup (pickup-type eco-{args[1]}) 5.0)")

                elif command in ["rapidfire"] and enabled_check("rapidfire") and cd_check("rapidfire"):
                    active_check("rapidfire", 
                    "(set! (-> *TARGET-bank* yellow-projectile-speed) (meters 100))(set! (-> *TARGET-bank* yellow-attack-timeout) (seconds 0))")

                elif command in ["sucksuck", "setsucksuck", "suck"] and len(args) >= 2 and enabled_check("sucksuck") and range_check(args[1], SUCK_MIN, SUCK_MAX) and cd_check("sucksuck"):
                    active_check("sucksuck",
                    f"(set! (-> *FACT-bank* suck-suck-dist) (meters {args[1]}))(set! (-> *FACT-bank* suck-bounce-dist) (meters {args[1]}))")

                elif command in ["noeco"] and enabled_check("noeco") and cd_check("noeco"):
                    active_check("noeco", 
                    "(send-event *target* 'reset-pickup 'eco)(set! (-> *FACT-bank* eco-full-timeout) (seconds 0.0))")

                elif command in ["die", "kill"] and enabled_check("die") and cd_check("die"):
                    sendForm("(when (not (movie?))(initialize! *game-info* 'die (the-as game-save #f) (the-as string #f)))")

                elif command in ["topoint", "tolevel"] and len(args) >= 2 and (point_list.count(str(args[1]).lower()) >= 1 or str(args[1]).lower() in point_nicknames) and enabled_check("topoint") and cd_check("topoint"):
                    arg1_lower = str(args[1]).lower()
                    point = None
                    if arg1_lower in point_nicknames:
                        point = get_random_point(arg1_lower)
                    elif point_list.count(arg1_lower) == 1:
                        point = arg1_lower

                    if point:
                        if not TOPOINT_PAST_CRATER and (point.startswith("lavatube") or point.startswith("citadel") or point.startswith("finalboss") or point.startswith("lt")):
                            sendMessage(irc, "/me @"+user+" Cannot go past Volcanic Crater.")
                            last_used[command_names.index("topoint")] = 0
                            
                            pass
                        else:
                            sendForm(f"(start 'play (get-continue-by-name *game-info* \"{point}\"))(auto-save-command 'auto-save 0 0 *default-pool*)")

                elif command in ["randompoint", "randomcheckpoint"] and enabled_check("randompoint") and cd_check("topoint"):
                    sendForm(f"(start 'play (get-continue-by-name *game-info* \"{point_list[random.choice(range(0,52))]}\"))(auto-save-command 'auto-save 0 0 *default-pool*)")

                elif command in ["sfx", "sound"] and len(args) >= 2 and str(args[1]).lower() in sfx_names and enabled_check("sfx") and cd_check("sfx"):
                    sfx = sfx_names[str(args[1])]
                    sendForm(f"(sound-play \"{sfx}\")")
                
                elif command in ["playhint", "hint"] and len(args) >= 2 and enabled_check("playhint") and cd_check("playhint"):
                    hint = args[1].replace("\"","")
                    sendForm("(kill-current-level-hint '() '() 'exit)")
                    time.sleep(0.05)
                    sendForm(f"(ambient-hint-spawn \"{hint}\" (-> *target* root trans) *entity-pool* 'ambient)")

                elif command in ["crazyplats"] and enabled_check("crazyplats") and cd_check("crazyplats"):
                    active_check("crazyplats", 
                    "(when (process-by-ename \"bone-platform-4\")(set! (-> *bone-platform-constants* player-weight) (meters -350)))(when (process-by-ename \"pontoonten-10\")(set! (-> *pontoonten-constants* player-weight) (meters -350)))(when (process-by-ename \"pontoonfive-6\")(set! (-> *pontoonfive-constants* player-weight) (meters -350)))(when (process-by-ename \"tra-pontoon-3\")(set! (-> *tra-pontoon-constants* player-weight) (meters -350)))(when (process-by-ename \"citb-chain-plat-14\")(set! (-> *citb-chain-plat-constants* player-weight) (meters -350)))(when (process-by-ename \"qbert-plat-7\")(set! (-> *qbert-plat-constants* player-weight) (meters -350)))(when (process-by-ename \"tar-plat-21\")(set! (-> *tar-plat-constants* player-weight) (meters -350)))(when (process-by-ename \"ogre-step-a-2\")(set! (-> *ogre-step-constants* player-weight) (meters -350)))(when (process-by-ename \"ogre-isle-c-1\")(set! (-> *ogre-isle-constants* player-weight) (meters -200)))")
                    
                elif command in ["setpoint", "setcheckpoint"] and enabled_check("setpoint") and cd_check("setpoint"):
                    sendForm("(vector-copy! (-> (-> *game-info* current-continue) trans) (target-pos 0))")
    
                elif command in ["tp"] and len(args) >= 4 and enabled_check("tp") and cd_check("tp"):
                    sendForm(f"(when (not (movie?))(set! (-> (target-pos 0) x) (meters {args[1]}))  (set! (-> (target-pos 0) y) (meters {args[2]})) (set! (-> (target-pos 0) z) (meters {args[3]})))")

                elif command in ["shift"] and len(args) >= 4 and enabled_check("shift") and range_check(args[1], SHIFTX_MIN, SHIFTX_MAX) and range_check(args[2], SHIFTY_MIN, SHIFTY_MAX) and range_check(args[3], SHIFTZ_MIN, SHIFTZ_MAX) and cd_check("tp"):
                    sendForm(f"(when (not (movie?))(set! (-> (target-pos 0) x) (+ (-> (target-pos 0) x)(meters {args[1]})))  (set! (-> (target-pos 0) y) (+ (-> (target-pos 0) y)(meters {args[2]}))) (set! (-> (target-pos 0) z) (+ (-> (target-pos 0) z)(meters {args[3]}))))")

                elif command in ["rocketman", "rocket"] and enabled_check("rocketman") and cd_check("rocketman"):
                    active_check("rocketman", 
                    "(set! (-> *standard-dynamics* gravity-normal y) -0.5)")

                elif command in ["movetojak", "summon"] and len(args) >= 2 and enabled_check("movetojak") and cd_check("movetojak"):
                    sendForm(f"(when (process-by-ename \"{args[1]}\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"{args[1]}\"))root)trans) (-> (target-pos 0) x) (-> (target-pos 0) y) (-> (target-pos 0) z) 1.0))")

                elif command in ["ouch"] and enabled_check("ouch") and cd_check("ouch"):
                    sendForm("(if (not (= *target* #f))(send-event *target* 'attack #t (new 'static 'attack-info)))")

                elif command in ["burn"] and enabled_check("burn") and cd_check("ouch"):
                    sendForm("(if (not (= *target* #f))(target-attack-up *target* 'attack 'burnup))")

                elif command in ["hp"] and len(args) >= 2 and enabled_check("hp") and cd_check("hp"):
                    sendForm(f"(set! (-> (the-as fact-info-target (-> *target* fact))health) (+ 0.0 {args[1]}))")

                elif command in ["melt"] and enabled_check("melt") and cd_check("die"):
                    sendForm("(when (not (movie?))(target-attack-up *target* 'attack 'melt))")

                elif command in ["endlessfall", "fall"] and enabled_check("endlessfall") and cd_check("die"):
                    sendForm("(when (not (movie?))(target-attack-up *target* 'attack 'endlessfall))")

                elif command in ["drown"] and enabled_check("drown") and cd_check("die"):
                    sendForm("(when (not (movie?))(target-attack-up *target* 'attack 'drown-death))")

                elif command in ["iframes"] and len(args) >= 2 and enabled_check("iframes") and cd_check("iframes"):
                    deactivate("iframes")
                    activate("iframes")
                    sendForm("(set! (-> *TARGET-bank* hit-invulnerable-timeout) (seconds " + str(args[1]) + "))")

                elif command in ["invertcam"] and len(args) >= 3 and enabled_check("invertcam") and cd_check("invertcam"):
                    if (args[1] == "third" or args[1] == "first") and (args[2] == "h" or args[2] == "v"):
                        deactivate("invertcam")
                        activate("invertcam")
                        sendForm(f"(set! (-> *pc-settings* {args[1]}-camera-{args[2]}-inverted?) (not (-> *pc-settings* {args[1]}-camera-{args[2]}-inverted?)))")

                elif command in ["cam"] and len(args) >= 2 and str(args[1]).lower() in cam_list and enabled_check("cam") and cd_check("cam"):
                    deactivate("stickycam")
                    deactivate("cam")
                    activate("cam")
                    sendForm(f"(send-event *camera* 'change-state cam-{args[1]} 0)(send-event *target* 'no-look-around (seconds {durations[command_names.index("cam")]}))")

                elif command in ["tiktok"] and enabled_check("tiktok") and cd_check("tiktok"):
                    active_check("tiktok",
                    f"(set! (-> *pc-settings* aspect-ratio) 0.5625)")

                elif command in ["stickycam"] and enabled_check("stickycam") and cd_check("stickycam"):
                    deactivate("cam")
                    active_check("stickycam",
                    f"(send-event *target* 'no-look-around (seconds {durations[command_names.index("stickycam")]}))(send-event *camera* 'change-state cam-circular 0)")

                elif command in ["askew", "tilt"] and enabled_check("askew") and cd_check("askew"):
                    active_check("askew", 
                    "(set! (-> *standard-dynamics* gravity x) 25000.0)")
                    
                elif command in ["deload"] and enabled_check("deload") and cd_check("deload"):
                    sendForm("(when (not (movie?))(set! (-> *load-state* want 0 display?) #f)(set! (-> *load-state* want 1 display?) #f))")

                elif command in ["quickcam", "frickstorage"] and enabled_check("quickcam") and cd_check("quickcam"):
                    sendForm("(stop 'debug)(start 'play (get-or-create-continue! *game-info*))")
                    time.sleep(0.1)
                    sendForm("(set! (-> *game-info* current-continue) (get-continue-by-name *game-info* \"training-start\"))")

                elif command in ["dark"] and enabled_check("dark") and cd_check("dark"):
                    active_check("dark", 
                    "(set! *dark-level* (level-get-target-inside *level*))(set! (-> *dark-level* mood-func)update-mood-finalboss)")

                elif command in ["blind"] and len(args) >= 2 and enabled_check("blind") and range_check(args[1], BLIND_MIN, BLIND_MAX) and cd_check("dark"):
                    sendForm(f"(set-blackout-frames (seconds {args[1]}))")

                elif command in ["nodax", "dax"] and enabled_check("nodax") and cd_check("nodax"):
                    active_check("nodax", 
                    "(send-event *target* 'sidekick #f)")

                elif command in ["smallnet"] and enabled_check("smallnet") and cd_check("smallnet"):
                    active_check("smallnet", 
                    "(when (process-by-ename \"fisher-1\")(set!(-> *FISHER-bank* net-radius)(meters 0.0)))")

                elif command in ["widefish"] and enabled_check("widefish") and cd_check("widefish"):
                    active_check("widefish", 
                    "(when (process-by-ename \"fisher-1\")(set! (-> *FISHER-bank* width)(meters 10.0)))")

                elif command in ["maxfish"] and len(args) >= 2 and enabled_check("maxfish") and range_check(args[1], MAXFISH_MIN, MAXFISH_MAX) and cd_check("maxfish"):
                    sendForm(f"(when (process-by-ename \"fisher-1\")(set! (-> *FISHER-bank* max-caught) {args[1]}))")

                elif command in ["hardfish"] and enabled_check("hardfish") and cd_check("hardfish"):
                    active_check("hardfish", 
                    "(when (process-by-ename \"fisher-1\")(set! (-> (the fisher (process-by-ename \"fisher-1\")) difficulty) 5)(set! (-> *FISHER-bank* max-caught) 400))")   
                    
                elif command in ["customfish"] and len(args) >= 5 and enabled_check("customfish") and args[3] in fish_list and range_check(args[1], 0, 5) and range_check(args[2], 1, 7) and range_check(args[4], 0, 100) and cd_check("customfish"):
                    phase = (2 * int(args[2])) - 1
                    difficulty = int(args[1])
                    if args[3] in ["swing-min", "swing-max", "period", "timeout"]:
                        value = f"(seconds {args[4]})"
                    else:
                        value = float(args[4])
                    sendForm(f"(when (process-by-ename \"fisher-1\")(set! (-> (-> (-> *fisher-params* {difficulty}) {phase}) {args[3]}) {value}))")

                elif command in ["lowpoly", "lod"] and enabled_check("lowpoly") and cd_check("lowpoly"):
                    active_check("lowpoly", 
                    "(set! (-> *pc-settings* lod-force-tfrag) 2)(set! (-> *pc-settings* lod-force-tie) 3)(set! (-> *pc-settings* lod-force-ocean) 2)(set! (-> *pc-settings* lod-force-actor) 3)")

                elif command in ["moveplantboss", "plantboss"] and enabled_check("moveplantboss") and cd_check("moveplantboss"):
                    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #f)")
                    time.sleep(0.05)
                    sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
                    sendForm("(set! (-> (the-as fact-info-target (-> *target* fact))health) 1.0)")
                    time.sleep(2)
                    sendForm("(set! (-> (target-pos 0) x) (meters 431.47))  (set! (-> (target-pos 0) y) (meters -44.00)) (set! (-> (target-pos 0) z) (meters -334.09))")
                    if not ALL_ACTORS:
                        time.sleep(0.05)
                        sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #t)")

                elif command in ["moveplantboss2", "plantboss2"] and enabled_check("moveplantboss2") and cd_check("moveplantboss2"):
                    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #f)")
                    time.sleep(0.050)
                    sendForm("(when (process-by-ename \"plant-boss-3\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"plant-boss-3\"))root)trans) (meters 436.97) (meters -43.99) (meters -347.09) 1.0))")
                    if not ALL_ACTORS:
                        time.sleep(0.05)
                        sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #t)")

                elif command in ["basincell"] and enabled_check("basincell") and cd_check("basincell"):
                    sendForm("(if (when (process-by-ename \"fuel-cell-45\") (= (-> (->(the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans x)  (meters -266.54)))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -248.92) (meters 52.11) (meters -1515.66) 1.0))(when (process-by-ename \"fuel-cell-45\")(set-vector!  (-> (-> (the process-drawable (process-by-ename \"fuel-cell-45\"))root)trans) (meters -266.54) (meters 52.11) (meters -1508.48) 1.0)))")

                elif command in ["resetactors"] and enabled_check("resetactors") and cd_check("resetactors"):
                    sendForm("(reset-actors 'debug)")

                elif command in ["noactors"] and enabled_check("noactors") and cd_check("resetactors"):
                    active_check("noactors",
                    "(set! *spawn-actors* #f) (reset-actors 'debug)")

                elif command in ["actors-on", "actorson"] and enabled_check("actors-on") and (user in COMMAND_ADMINS or user in COMMAND_MODS):
                    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #f)")

                elif command in ["actors-off", "actorsoff"] and enabled_check("actors-off") and (user in COMMAND_ADMINS or user in COMMAND_MODS):
                    sendForm("(set! (-> *pc-settings* ps2-actor-vis?) #t)")

                elif command in ["debug"] and enabled_check("debug") and (user in COMMAND_ADMINS or user in COMMAND_MODS):
                    sendForm("(set! *debug-segment* (not *debug-segment*))(set! *cheat-mode* (not *cheat-mode*))")

                elif command in ["fixoldsave"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):
                    sendForm("(set! (-> *game-info* current-continue) (get-continue-by-name *game-info* \"training-start\"))(auto-save-command 'auto-save 0 0 *default-pool*)")

                elif command in ["save"] and enabled_check("save") and (user in COMMAND_ADMINS or user in COMMAND_MODS):            
                    sendForm("(auto-save-command 'auto-save 0 0 *default-pool*)")

                elif command in ["resetcooldowns", "resetcds"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):           
                    for x in range(len(command_names)):
                        last_used[x]=0.0
                    sendMessage(irc, f"/me {TARGET_ID} -> All cooldowns reset.")

                elif command in ["active"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):           
                    sendMessage(irc, f"/me {TARGET_ID} -> {", ".join(active_list)}")

                elif command in ["cd", "cooldown"] and len(args) >= 3 and str(args[1]) in command_names and (user in COMMAND_ADMINS or user in COMMAND_MODS):          
                    cooldowns[command_names.index(str(args[1]))]=float(args[2])
                    sendMessage(irc, f"/me {TARGET_ID} -> '{args[1]}' cooldown set to {args[2]}s.")

                elif command in ["dur", "duration"] and len(args) >= 3 and str(args[1]) in command_names and (user in COMMAND_ADMINS or user in COMMAND_MODS):         
                    durations[command_names.index(str(args[1]))]=float(args[2])
                    sendMessage(irc, f"/me {TARGET_ID} -> '{args[1]}' duration set to {args[2]}s.")

                elif command in ["enable"] and len(args) >= 2 and str(args[1]) in command_names and (user in COMMAND_ADMINS or user in COMMAND_MODS):          
                    enabled[command_names.index(str(args[1]))] = True
                    sendMessage(irc, f"/me {TARGET_ID} -> '{args[1]}' enabled.")

                elif command in ["disable"] and len(args) >= 2 and str(args[1]) in command_names and (user in COMMAND_ADMINS or user in COMMAND_MODS):          
                    enabled[command_names.index(str(args[1]))] = False
                    sendMessage(irc, f"/me {TARGET_ID} -> '{args[1]}' disabled.")
                    
                elif command in ["mod"] and len(args) >= 2 and user in COMMAND_ADMINS:          
                    COMMAND_MODS.append(str(args[1]))
                    sendMessage(irc, f"/me {TARGET_ID} -> {args[1]} added to mod list.")

                elif command in ["widejak", "wide"] and enabled_check("widejak") and cd_check("scale"):
                    deactivate("bigjak")
                    deactivate("smalljak")
                    deactivate("scale")
                    deactivate("flatjak")
                    active_check("widejak", 
                    "(set! (-> (-> (the-as target *target* )root)scale x) 4.0)(set! (-> (-> (the-as target *target* )root)scale y) 1.0)(set! (-> (-> (the-as target *target* )root)scale z) 1.0)")

                elif command in ["flatjak", "flat"] and enabled_check("flatjak") and cd_check("scale"):
                    deactivate("bigjak")
                    deactivate("smalljak")
                    deactivate("widejak")
                    deactivate("scale")
                    active_check("flatjak", 
                    "(set! (-> (-> (the-as target *target* )root)scale x) 1.3)(set! (-> (-> (the-as target *target* )root)scale y) 0.2)(set! (-> (-> (the-as target *target* )root)scale z) 1.3)")

                elif command in ["smalljak", "small"] and enabled_check("smalljak") and cd_check("scale"):
                    deactivate("bigjak")
                    deactivate("scale")
                    deactivate("widejak")
                    deactivate("flatjak")
                    active_check("smalljak", 
                    "(set! (-> (-> (the-as target *target* )root)scale x) 0.4)(set! (-> (-> (the-as target *target* )root)scale y) 0.4)(set! (-> (-> (the-as target *target* )root)scale z) 0.4)(set! (-> *TARGET-bank* wheel-flip-dist) (meters 43.25))")

                elif command in ["bigjak", "big"] and enabled_check("bigjak") and cd_check("scale"):
                    deactivate("scale")
                    deactivate("smalljak")
                    deactivate("widejak")
                    deactivate("flatjak")
                    active_check("bigjak", 
                    "(set! (-> (-> (the-as target *target* )root)scale x) 2.7)(set! (-> (-> (the-as target *target* )root)scale y) 2.7)(set! (-> (-> (the-as target *target* )root)scale z) 2.7)")

                elif command in ["color", "colour"] and len(args) >= 4 and enabled_check("color") and cd_check("color"):
                    deactivate("color")
                    activate("color")
                    sendForm(f"(set! (-> *target* draw color-mult x) (+ 0.0 {args[1]}))(set! (-> *target* draw color-mult y) (+ 0.0 {args[2]}))(set! (-> *target* draw color-mult z) (+ 0.0 {args[3]}))")

                elif command in ["scale"] and len(args) >= 4 and enabled_check("scale") and range_check(str(args[1]), SCALE_MIN, SCALE_MAX) and range_check(str(args[2]), SCALE_MIN, SCALE_MAX) and range_check(str(args[3]), SCALE_MIN, SCALE_MAX) and cd_check("scale"):
                    deactivate("bigjak")
                    deactivate("smalljak")
                    deactivate("widejak")
                    deactivate("flatjak")
                    deactivate("scale")
                    activate("scale")
                    sendForm(f"(set! (-> (-> (the-as target *target* )root)scale x) (+ 0.0 {args[1]}))(set! (-> (-> (the-as target *target* )root)scale y) (+ 0.0 {args[2]}))(set! (-> (-> (the-as target *target* )root)scale z) (+ 0.0 {args[3]}))")

                elif command in ["slippery"] and enabled_check("slippery") and cd_check("slippery"):
                    deactivate("pinball")
                    active_check("slippery", 
                    "(set! (-> *stone-surface* slope-slip-angle) 16384.0)(set! (-> *stone-surface* slip-factor) 0.7)(set! (-> *stone-surface* transv-max) 1.5)(set! (-> *stone-surface* turnv) 0.5)(set! (-> *stone-surface* nonlin-fric-dist) 4091904.0)(set! (-> *stone-surface* fric) 23756.8)(set! (-> *grass-surface* slope-slip-angle) 16384.0)(set! (-> *grass-surface* slip-factor) 0.7)(set! (-> *grass-surface* transv-max) 1.5)(set! (-> *grass-surface* turnv) 0.5)(set! (-> *grass-surface* nonlin-fric-dist) 4091904.0)(set! (-> *grass-surface* fric) 23756.8)(set! (-> *ice-surface* slip-factor) 0.3)(set! (-> *ice-surface* nonlin-fric-dist) 8183808.0)(set! (-> *ice-surface* fric) 11878.4)")

                elif command in ["gravity", "grav"] and len(args) >= 2 and enabled_check("gravity") and args[1] in ["high", "low"] and cd_check("gravity"):
                    match args[1]:
                        case "high":
                            line = "(set! (-> *standard-dynamics* gravity-length) (* GRAVITY_AMOUNT 3.5))(set! (-> *standard-dynamics* gravity y) (* GRAVITY_AMOUNT 2.5))"
                        case "low":
                            line = "(set! (-> *standard-dynamics* gravity-length) (/ GRAVITY_AMOUNT 4.5))(set! (-> *standard-dynamics* gravity y) (/ GRAVITY_AMOUNT 2.5))"    
                    active_check("gravity", 
                    line)
                
                elif command in ["pinball"] and enabled_check("pinball") and cd_check("pinball"):
                    deactivate("slippery")
                    active_check("pinball", 
                    "(set! (-> *stone-surface* fric) -25000.0)")
    
                #elif command in ["heatmax"] and len(args) >= 2:
                #    sendForm("(set! (-> *RACER-bank* heat-max) " + str(args[1]) + ")")
                   
                #elif command in ["loadlevel"] and len(args) >= 2:
                #    sendForm("(set! (-> *load-state* want 1 name) '" + str(args[1]) + ")(set! (-> *load-state* want 1 display?) 'display)")
                   
                #elif command in ["setecotime", "ecotime"] and len(args) >= 2:
                #    sendForm("(set! (-> *FACT-bank* eco-full-timeout) (seconds " + str(args[1]) + "))")
    
                elif command in ["bighead"] and enabled_check("bighead") and cd_check("bighead"):
                    deactivate("smallhead")
                    deactivate("hugehead")
                    active_check("bighead",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats big-head)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats big-head)))")

                elif command in ["smallhead"] and enabled_check("smallhead") and cd_check("smallhead"):
                    deactivate("bighead")
                    deactivate("hugehead")
                    active_check("smallhead",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats small-head)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats small-head)))")

                elif command in ["bigfist","bigfists"] and enabled_check("bigfist") and cd_check("bigfist"):
                    active_check("bigfist",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats big-fist)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats big-fist)))")

                elif command in ["bigheadnpc"] and enabled_check("bigheadnpc") and cd_check("bigheadnpc"):
                    active_check("bigheadnpc",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats big-head-npc)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats big-head-npc)))")

                elif command in ["hugehead"] and enabled_check("hugehead") and cd_check("hugehead"):
                    deactivate("bighead")
                    deactivate("smallhead")
                    active_check("hugehead",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats huge-head)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats huge-head)))")

                elif command in ["mirror"] and enabled_check("mirror") and cd_check("mirror"):
                    active_check("mirror",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats mirror)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats mirror)))")

                elif command in ["notex", "notextures"] and enabled_check("notex") and cd_check("notex"):
                    active_check("notex",
                    "(set! (-> *pc-settings* speedrunner-mode?) #f)(begin (logior! (-> *pc-settings* cheats) (pc-cheats no-tex)) (logclear! (-> *pc-settings* cheats-known) (pc-cheats no-tex)))")

                elif command in ["spiderman"] and enabled_check("spiderman") and cd_check("spiderman"):
                    active_check("spiderman",
                    "(set! (-> *pat-mode-info* 1 wall-angle) 0.0) (set! (-> *pat-mode-info* 2 wall-angle) 0.0)")

                elif command in ["statue", "freeze"] and enabled_check("statue") and cd_check("statue"):
                    active_check("statue",
                    "(when (not (movie?))(logior! (-> *target* mask) (process-mask sleep)))")

                elif command in ["fakewarp", "fakewarp"] and enabled_check("fakewarp") and cd_check("fakewarp"):
                    active_check("fakewarp",
                    f"(set! (-> *setting-control* default music-volume) 0.0)(set! (-> *setting-control* default dialog-volume) 0.0)(set! (-> *setting-control* default sfx-volume) 0.0)(set! (-> *setting-control* default ambient-volume) 0.0)(set-blackout-frames (seconds {durations[command_names.index("fakewarp")]}))")

                elif command in ["press"] and len(args) >= 2 and str(args[1]).lower() in pad_list and enabled_check("press") and cd_check("press"):
                    sendForm(f"(logior! (cpad-pressed 0) (pad-buttons {args[1]}))")

                elif command in ["pause"] and enabled_check("pause") and cd_check("pause"):
                    sendForm(f"(activate-progress *dproc* (progress-screen fuel-cell))")

                elif command in ["lang", "language"] and len(args) >= 2 and str(args[1]).lower() in lang_list and enabled_check("lang") and cd_check("lang"):
                    sendForm(f"(set! (-> *setting-control* default language) (language-enum {str(args[1]).lower()}))")

                elif command in ["timeofday", "time"] and len(args) >= 2 and enabled_check("timeofday") and range_check(args[1], 0, 24) and cd_check("timeofday"):
                    sendForm(f"(set-time-of-day {float(args[1])})")

                elif command in ["turn-left"] and enabled_check("turn-left") and cd_check("turn-left"):
                    sendForm("(quaternion-rotate-local-y! (-> *target* root dir-targ) (-> *target* root dir-targ) (/ DEGREES_PER_ROT 8.0))")

                elif command in ["turn-right"] and enabled_check("turn-right") and cd_check("turn-right"):
                    sendForm("(quaternion-rotate-local-y! (-> *target* root dir-targ) (-> *target* root dir-targ) (/ DEGREES_PER_ROT -8.0))")

                elif command in ["turn-180"] and enabled_check("turn-180") and cd_check("turn-180"):
                    sendForm("(quaternion-rotate-local-y! (-> *target* root dir-targ) (-> *target* root dir-targ) (/ DEGREES_PER_ROT 2.0))")

                elif command in ["cam-right"] and enabled_check("cam-right") and cd_check("cam-right"):
                    sendForm("(set! (-> *cpad-list* cpads 0 rightx) (the-as uint 0))")

                elif command in ["cam-left"] and enabled_check("cam-left") and cd_check("cam-left"):
                    sendForm("(set! (-> *cpad-list* cpads 0 rightx) (the-as uint 255))")

                elif command in ["cam-in"] and enabled_check("collected") and cd_check("cam-in"):
                    sendForm("(set! (-> *cpad-list* cpads 0 righty) (the-as uint 0))")

                elif command in ["cam-out"] and enabled_check("cam-out") and cd_check("cam-out"):
                    sendForm("(set! (-> *cpad-list* cpads 0 righty) (the-as uint 255))")

                elif command in ["finalboss"] and (user in COMMAND_ADMINS or user in COMMAND_MODS):
                    global finalboss_mode
                    finalboss_cooldown_commands = [
                    "scale", "hp", "iframes", "ouch", "rocketman",
                    "noeco", "eco", "shortfall", "nuka", "slippery", "nojumps",
                    "gravity", "quickcam"]
                    finalboss_mode = not finalboss_mode
                    if finalboss_mode:
                        adjust_finalboss_cooldowns(finalboss_cooldown_commands, FINALBOSS_MUL)
                        sendMessage(irc, f"/me {TARGET_ID} -> Final Boss Mode activated! Cooldowns are longer and some commands are disabled.")
                    else:
                        adjust_finalboss_cooldowns(finalboss_cooldown_commands, FINALBOSS_MUL, divide=True)
                        sendMessage(irc, f"/me {TARGET_ID} -> Final Boss Mode deactivated.")
                    
                elif command in ["repl"] and len(args) >= 2 and enabled_check("repl") and cd_check("repl"):
                    if user in COMMAND_ADMINS:
                        args = message.split(" ", 1)
                        sendForm(str(args[1]))
                    else:
                        sendMessage(irc, f"/me @{user} Sorry, 'repl' is currently only accessable to the devs.")

        message = ""

        # check which commands have reached their duration, then deactivate
        active_sweep()
        
        #if GK_WIN.poll() is not None:
        #     code that closes goalc
        time.sleep(0.08)
            
            
# Dont touch
def twitch():

    global user, message

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