import tkinter as tk
from tkinter import messagebox, ttk
import os

class SettingsApp:
    def __init__(self, master):
        self.master = master
        master.title("Properties File Editor")

        # Set up the main container with a scrollbar
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.entries = {}
        self.check_vars = {}
        self.create_widgets()

        self.settings_file = '.env'
        self.load_settings()

    def create_widgets(self):
        # Sections for different settings
        self.add_section("User Settings", [
            "OAUTH", "TARGET_CHANNEL", "PREFIX", "CONNECT_MSG", "TARGET_ID"
        ], True)

        self.add_checkboxes_section("Camera Settings", [
            "first-camera-vertical-inverted", "first-camera-horizontal-inverted",
            "third-camera-vertical-inverted", "third-camera-horizontal-inverted"
        ], True)

        self.add_section("Command Limits", [
            "SHIFTX_MIN", "SHIFTX_MAX", "SHIFTY_MIN", "SHIFTY_MAX",
            "SHIFTZ_MIN", "SHIFTZ_MAX", "GIVE_MIN", "GIVE_MAX",
            "RJTO_MIN", "RJTO_MAX", "SCALE_MIN", "SCALE_MAX",
            "MINUSCELL_AMT", "PLUSCELL_AMT", "MINUSORBS_AMT", "PLUSORBS_AMT",
            "SUCK_MIN", "SUCK_MAX", "BLIND_MIN", "BLIND_MAX"
        ], True)

        self.add_checkboxes_section("Misc Settings", [
            "TOPOINT_PAST_CRATER"
        ], True)

        self.add_checkboxes_section("Command Enable/Disable", ["DISABLED_MSG", "TARGET_ID_MODE",
            "protect", "rjto", "superjump", "superboosted", "noboosteds",
            "nojumps", "noledge", "fastjak", "slowjak", "slippery", "pinball",
            "pacifist", "nuka", "invuln", "trip", "shortfall", "ghostjak",
            "getoff", "unzoom", "flutspeed", "freecam", "enemyspeed",
            "minuscell", "pluscell", "minusorbs", "plusorbs", "give",
            "collected", "eco", "rapidfire", "sucksuck", "noeco", "die",
            "topoint", "randompoint", "tp", "shift",
            "rocketman", "sfx", "movetojak", "ouch", "burn", "hp", "melt",
            "endlessfall", "drown", "iframes", "invertcam", "cam",
            "stickycam", "deload", "quickcam", "dark", "blind",
            "nodax", "smallnet", "widefish", "lowpoly", "color", "scale",
            "widejak", "flatjak", "smalljak", "bigjak", "moveplantboss",
            "moveplantboss2", "basincell", "resetactors", "noactors", "bighead",
            "smallhead", "bigfist", "bigheadnpc", "hugehead", "mirror",
            "notex", "spiderman", "press", "lang", "turn-left", "turn-right",
            "turn-180", "cam-left", "cam-right", "cam-in", "cam-out",
            "repl", "debug", "save", "actorson", "actorsoff",
            "fixoldsave", "finalboss"
        ], False)

        self.add_checkboxes_section("Command Cooldowns", [
            "COOLDOWN_MSG"
        ], True)

        self.add_section("", [
            "protect_cd", "rjto_cd", "superjump_cd", "superboosted_cd",
            "noboosteds_cd", "nojumps_cd", "noledge_cd", "fastjak_cd", "slowjak_cd", "slippery_cd",
            "pinball_cd", "pacifist_cd", "nuka_cd", "invuln_cd", "trip_cd",
            "shortfall_cd", "getoff_cd", "unzoom_cd", "flutspeed_cd", "freecam_cd",
            "enemyspeed_cd", "give_cd", "minuscell_cd", "pluscell_cd", "minusorbs_cd",
            "plusorbs_cd", "eco_cd", "rapidfire_cd", "sucksuck_cd", "noeco_cd",
            "die_cd", "topoint_cd", "tp_cd", "rocketman_cd", "sfx_cd",
            "movetojak_cd", "ouch_cd", "hp_cd", "iframes_cd", "invertcam_cd",
            "cam_cd", "stickycam_cd", "deload_cd", "quickcam_cd",
            "dark_cd", "nodax_cd", "smallnet_cd", "widefish_cd", "lowpoly_cd",
            "color_cd", "scale_cd", "moveplantboss_cd", "moveplantboss2_cd", 
            "basincell_cd", "bighead_cd", "smallhead_cd", "bigfist_cd", 
            "bigheadnpc_cd", "hugehead_cd", "mirror_cd", "notex_cd", "spiderman_cd", 
            "press_cd",
            "lang_cd", "resetactors_cd", "repl_cd", "turn-left_cd", "turn-right_cd",
            "turn-180_cd", "cam-left_cd", "cam-right_cd", "cam-in_cd", "cam-out_cd"
        ], False)

        self.add_checkboxes_section("Command Durations", [
            "ACTIVATION_MSG", "DEACTIVATION_MSG"
        ], True)

        self.add_section("", [
            "protect_dur", "rjto_dur", "superjump_dur",
            "superboosted_dur", "noboosteds_dur", "nojumps_dur", "noledge_dur", "fastjak_dur", 
            "slowjak_dur", "slippery_dur", "pinball_dur", "pacifist_dur",
            "shortfall_dur", "ghostjak_dur", "freecam_dur", "sucksuck_dur", 
            "noeco_dur", "rapidfire_dur", "iframes_dur", "rocketman_dur", 
            "invertcam_dur", "stickycam_dur", "cam_dur", "dark_dur",
            "nodax_dur", "spiderman_dur", "smallnet_dur", "widefish_dur", "lowpoly_dur", "color_dur",
            "scale_dur", "widejak_dur", "flatjak_dur", "smalljak_dur", "bigjak_dur",
            "bighead_dur", "smallhead_dur", "bigfist_dur", "bigheadnpc_dur", 
            "hugehead_dur", "mirror_dur", "notex_dur", "noactors_dur"
        ], False)

        # Buttons to save and load settings
        tk.Button(self.frame, text="Load Settings", command=self.load_settings).pack(pady=10)
        tk.Button(self.frame, text="Save Settings", command=self.save_settings).pack(pady=10)

    def format_key(self, key, format):
        if format:
            return key.replace('MSG', 'MESSAGE').replace(' MIN', ' MINIMUM').replace(' MAX', ' MAXIMUM').replace(' AMT', ' AMOUNT')
        else:
            return key.replace('_cd', '').replace('_dur', '')
        # return key

    def add_section(self, section_name, keys, format):
        tk.Label(self.frame, text=section_name, font=("Arial", 12, "bold")).pack(anchor="w", pady=3)
        container = tk.Frame(self.frame)
        container.pack(fill="x", padx=5, pady=2)

        left_frame = tk.Frame(container)
        left_frame.pack(side="left", fill="both", expand=True, padx=3)

        right_frame = tk.Frame(container)
        right_frame.pack(side="right", fill="both", expand=True, padx=3)

        half = len(keys) // 2
        left_keys = keys[:half]
        right_keys = keys[half:]

        for key in left_keys:
            frame = tk.Frame(left_frame)
            frame.pack(fill="x", pady=1)
            tk.Label(frame, text=self.format_key(key, format), width=20, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry

        for key in right_keys:
            frame = tk.Frame(right_frame)
            frame.pack(fill="x", pady=1)
            tk.Label(frame, text=self.format_key(key, format), width=20, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry



    def add_checkboxes_section(self, section_name, keys, format):
        tk.Label(self.frame, text=section_name, font=("Arial", 12, "bold")).pack(anchor="w", pady=3)
        container = tk.Frame(self.frame)
        container.pack(fill="x", padx=5)

        left_frame = tk.Frame(container)
        left_frame.pack(side="left", fill="both", expand=True, padx=3)

        right_frame = tk.Frame(container)
        right_frame.pack(side="right", fill="both", expand=True, padx=3)

        half = len(keys) // 2
        left_keys = keys[:half]
        right_keys = keys[half:]

        for key in left_keys:
            self.check_vars[key] = tk.BooleanVar()
            check = tk.Checkbutton(left_frame, text=self.format_key(key, format), variable=self.check_vars[key])
            check.pack(anchor="w")

        for key in right_keys:
            self.check_vars[key] = tk.BooleanVar()
            check = tk.Checkbutton(right_frame, text=self.format_key(key, format), variable=self.check_vars[key])
            check.pack(anchor="w")

    def load_settings(self):
        # Load settings from .env file
        if os.path.exists(self.settings_file):
            self.load_file(self.settings_file)
        else:
        #    # Ensure default settings are written if the file does not exist
        #    self.save_default_settings()
            messagebox.showwarning("Load Error", f"No settings file found at {self.settings_file}.")

    def load_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in self.entries:
                            self.entries[key].delete(0, tk.END)
                            self.entries[key].insert(0, value)
                        elif key in self.check_vars:
                            self.check_vars[key].set(value == "t")
            # messagebox.showinfo("Load Successful", f"Settings loaded from {filename}")
        except FileNotFoundError:
            messagebox.showwarning("Load Error", f"No settings file found at {filename}. Using default settings.")

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            for key, entry in self.entries.items():
                value = entry.get()
                f.write(f"{key}={value}\n")
            for key, var in self.check_vars.items():
                value = "t" if var.get() else "f"
                f.write(f"{key}={value}\n")
        
        # Append non-editable settings
        self.append_fixed_settings()

        messagebox.showinfo("Save Successful", f"Settings saved to {self.settings_file}")

    def append_fixed_settings(self):
        fixed_settings = """
PATHTOAHK=C:\\Program Files\\AutoHotkey\\AutoHotkey.exe
trip_dur=0
getoff_dur=0
flutspeed_dur=0
enemyspeed_dur=0
give_dur=0
collected_dur=0
eco_dur=0
die_dur=0
topoint_dur=0
randompoint_dur=0
tp_dur=0
shift_dur=0
movetojak_dur=0
ouch_dur=0
burn_dur=0
hp_dur=0
melt_dur=0
endlessfall_dur=0
deload_dur=0
blind_cd=0
blind_dur=0
quickcam_dur=0
moveplantboss_dur=0
moveplantboss2_dur=0
basincell_dur=0
resetactors_dur=0
noactors_cd
repl_dur=0
debug_dur=0
debug_cd=0
melt_cd=0
endlessfall_cd=0
burn_cd=0
shift_cd=0
randompoint_cd=0
sfx_dur=0
collected_cd=0
minuscell_dur=0
pluscell_dur=0
minusorbs_dur=0
plusorbs_dur=0
ghostjak_cd=0
save_cd=0
save_dur=0
resetcooldowns_cd=0
resetcooldowns_dur=0
cd_dur=0
cd_cd=0
dur_dur=0
dur_cd=0
enable_cd=0
disable_cd=0
disable_dur=0
enable_dur=0
flatjak_cd=0
smalljak_cd=0
bigjak_cd=0
widejak_cd=0
nuka_dur=0
invuln_dur=0
bigpound=f
bigpound_cd=0
bigpound_dur=0
actors-on_cd=0
actors-on_dur=0
actors-off_cd=0
actors-off_dur=0
unzoom_dur=0
drown_cd=0
drown_dur=0
press_dur=0
fixoldsave_dur=0
fixoldsave_cd=0
finalboss_dur=0
finalboss_cd=0
lang_dur=0
resetcooldowns=t
cd=t
dur=t
enable=t
disable=t
turn-left_dur=0
turn-right_dur=0
turn-180_dur=0
cam-left_dur=0
cam-right_dur=0
cam-in_dur=0
cam-out_dur=0
"""
        with open(self.settings_file, 'a') as f:
            f.write(fixed_settings.strip())
        # messagebox.showinfo("Fixed Settings Added", "Fixed settings appended to the .env file")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")  # Set the window size
    app = SettingsApp(root)
    root.mainloop()
