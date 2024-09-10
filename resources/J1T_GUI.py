import tkinter as tk
from tkinter import messagebox, ttk
import os

class SettingsApp:
    def __init__(self, master):
        self.master = master
        master.title("Properties File Editor")
        master.configure(bg="#E9E9E9")

        # Set up the main container with a scrollbar
        main_frame = tk.Frame(master, bg="#E9E9E9")
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame, bg="#E9E9E9")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.frame = tk.Frame(canvas, bg="#E9E9E9")
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.entries = {}
        self.check_vars = {}
        self.create_widgets()

        self.settings_file = '.env'
        self.load_settings()

        # Mouse wheel scrolling functionality
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mouse_wheel(e, canvas))

    def _on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_widgets(self):
        # Sections for different settings
        self.add_section("User Settings", [
            "OAUTH", "TARGET_CHANNEL", "PREFIX", "CONNECT_MSG", "TARGET_ID", "COMMAND_MODS"
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
            "SUCK_MIN", "SUCK_MAX", "BLIND_MIN", "BLIND_MAX", "MAXFISH_MIN", "MAXFISH_MAX"
        ], True)

        self.add_checkboxes_section("Misc Settings", [
            "DISABLED_MSG", "TARGET_MODE", "TOPOINT_PAST_CRATER", "COOLDOWN_MSG", "ACTIVATION_MSG", "DEACTIVATION_MSG", "COST_MODE", "LOAD_STARTED"
        ], True)

        self.add_checkboxes_section("Command Enable/Disable", [
            "actors-off", "actors-on", "askew", "basincell", "bigfist", "bighead", 
            "bigheadnpc", "bigjak", "blind", "burn", "cam", 
            "cam-in", "cam-left", "cam-out", "cam-right", "collected", 
            "color", "customfish", "dark", "debug", "deload", 
            "die", "drown", "eco", "earthquake", "endlessfall", 
            "fakewarp", "fastjak", "freecam", 
            "getoff", "ghostjak", "give", "gravity", "hardfish", 
            "hp", "hugehead", "iframes", "invertcam", "invuln", 
            "lang", "leapfrog", "lowpoly", "maxfish", "melt", "mirror", 
            "minuscell", "minusorbs", "moveplantboss", "moveplantboss2", "movetojak", 
            "noboosteds", "nodax", "nodive", "noduck", "noeco", "noactors", 
            "nojumps", "noledge", "notex", "nuka", "ouch", 
            "pacifist", "pinball", "playhint", "pluscell", "plusorbs", "press", 
            "protect", "quickcam", "randompoint", "rapidfire", "repl", 
            "resetactors", "rjto", "rocketman", "save", "scale", 
             "sfx", "shift", "shortfall", "slippery", "slowjak", "smallhead", "smalljak", 
            "smallnet", "spiderman", "statue", "stickycam", "superboosted", "superjump", 
            "sucksuck", "tiktok", "timeofday", "topoint", "tp", 
            "trip", "turn-180", "turn-left", "turn-right", "unzoom", 
            "widefish", "widejak"
        ], False)

        self.add_section("Command Cooldowns", [
            "askew_cd", "basincell_cd", "bigfist_cd", "bighead_cd", "bigheadnpc_cd", "cam_cd", 
            "cam-in_cd", "cam-left_cd", "cam-out_cd", "cam-right_cd", "color_cd", 
            "customfish_cd", "dark_cd", "deload_cd", "die_cd", "eco_cd", 
            "earthquake_cd", "fakewarp_cd", "fastjak_cd",
            "freecam_cd", "getoff_cd", "give_cd", "gravity_cd", "hardfish_cd", 
            "hp_cd", "hugehead_cd", "iframes_cd", "invertcam_cd", "invuln_cd", 
            "lang_cd", "leapfrog_cd", "lowpoly_cd", "maxfish_cd", "mirror_cd", "minuscell_cd", 
            "minusorbs_cd", "moveplantboss_cd", "moveplantboss2_cd", "movetojak_cd", 
            "noboosteds_cd", "nodax_cd", "nodive_cd", "noduck_cd", "noeco_cd", "noactors_cd", 
            "nojumps_cd", "noledge_cd", "notex_cd", "nuka_cd", "ouch_cd", 
            "pacifist_cd", "pinball_cd", "playhint_cd", "pluscell_cd", "plusorbs_cd", "press_cd", 
            "protect_cd", "quickcam_cd", "rapidfire_cd", "repl_cd", "resetactors_cd", 
            "rjto_cd", "rocketman_cd", "scale_cd", "sfx_cd", "shortfall_cd", 
            "slippery_cd", "slowjak_cd", "smallhead_cd", "smallnet_cd", "spiderman_cd", "statue_cd",
            "stickycam_cd", "superboosted_cd", "superjump_cd", "sucksuck_cd", "tiktok_cd", 
            "timeofday_cd", "topoint_cd", "tp_cd", "trip_cd", "turn-180_cd", 
            "turn-left_cd", "turn-right_cd", "unzoom_cd", "widefish_cd"
        ], False)

        self.add_section("Command Costs", [
            "askew_cost", "basincell_cost", "bigfist_cost", "bighead_cost", "bigheadnpc_cost", 
            "bigjak_cost", "blind_cost", "burn_cost", "cam_cost", "cam-in_cost", 
            "cam-left_cost", "cam-out_cost", "cam-right_cost", "collected_cost", 
            "color_cost", "customfish_cost", "dark_cost", "deload_cost", "die_cost", 
            "drown_cost", "earthquake_cost", "eco_cost", "endlessfall_cost", 
            "fakewarp_cost", "fastjak_cost", "flatjak_cost", 
            "freecam_cost", "getoff_cost", "ghostjak_cost", "give_cost", "gravity_cost", 
            "hardfish_cost", "hp_cost", "hugehead_cost", "iframes_cost", 
            "invertcam_cost", "invuln_cost", "lang_cost", "leapfrog_cost", "lowpoly_cost", "maxfish_cost", "melt_cost", 
            "mirror_cost", "minuscell_cost", "minusorbs_cost", "moveplantboss_cost", 
            "moveplantboss2_cost", "movetojak_cost", "noboosteds_cost", "nodax_cost", "nodive_cost", 
            "noduck_cost", "noeco_cost", "noactors_cost", "nojumps_cost", "noledge_cost", 
            "notex_cost", "nuka_cost", "ouch_cost", "pacifist_cost", "pinball_cost", "playhint_cost", 
            "pluscell_cost", "plusorbs_cost", "press_cost", "protect_cost", 
            "quickcam_cost", "randompoint_cost", "rapidfire_cost", "repl_cost", 
            "resetactors_cost", "rjto_cost", "rocketman_cost", "scale_cost", 
            "shift_cost", "shortfall_cost", "slippery_cost", "slowjak_cost", "smallhead_cost", 
            "smalljak_cost", "smallnet_cost", "spiderman_cost", "statue_cost", "stickycam_cost", 
            "superboosted_cost", "superjump_cost", "sucksuck_cost", "sfx_cost", 
            "tiktok_cost", "timeofday_cost", "topoint_cost", "tp_cost", "trip_cost", "turn-180_cost", 
            "turn-left_cost", "turn-right_cost", "unzoom_cost", "widefish_cost", 
            "widejak_cost"
        ], False)

        self.add_section("Command Durations", [
            "askew_dur", "bigfist_dur", "bighead_dur", "bigheadnpc_dur", "bigjak_dur",
            "color_dur", "cam_dur", "dark_dur", "fakewarp_dur", "fastjak_dur", "flatjak_dur",
            "freecam_dur", "ghostjak_dur", "gravity_dur", "hardfish_dur",
            "hugehead_dur", "iframes_dur", "invertcam_dur", "invuln_dur", "leapfrog_dur", "lowpoly_dur",
            "mirror_dur", "noactors_dur", "noeco_dur", "nodax_dur", "nodive_dur", "noduck_dur",
            "nojump_dur", "noledge_dur", "noboosteds_dur", "nojumps_dur", "notex_dur",
            "pacifist_dur", "pinball_dur", "protect_dur", "rapidfire_dur",
            "rjto_dur", "rocketman_dur", "scale_dur", "shortfall_dur", 
            "slippery_dur", "slowjak_dur", "smallhead_dur", "smalljak_dur",
            "smallnet_dur", "spiderman_dur", "statue_dur", "stickycam_dur", "sucksuck_dur",
            "superboosted_dur", "superjump_dur", "tiktok_dur", "widefish_dur", "widejak_dur"
        ], False)

        # Buttons to save and load settings
        tk.Button(self.frame, text="Load Settings", command=self.load_settings).pack(pady=10)
        tk.Button(self.frame, text="Save Settings", command=self.save_settings).pack(pady=10)
        
                # Add Save and Quit button
        save_quit_button = tk.Button(self.frame, text="Save and Exit", command=self.save_and_quit, bg="#2C9774", fg="white")
        save_quit_button.pack(pady=10)
        

    def format_key(self, key, format):
        if format:
            return key.replace('MSG', 'MESSAGE').replace(' MIN', ' MINIMUM').replace(' MAX', ' MAXIMUM').replace(' AMT', ' AMOUNT')
        else:
            return key.replace('_cd', '').replace('_dur', '').replace('_cost', '')
        # return key

    def add_section(self, section_name, keys, format):
        tk.Label(self.frame, text=section_name, font=("Arial", 12, "bold"), bg="#E9E9E9").pack(anchor="w", pady=2)
        container = tk.Frame(self.frame, bg="#E9E9E9")
        container.pack(fill="x", padx=2, pady=1)

        left_frame = tk.Frame(container, bg="#E9E9E9")
        left_frame.pack(side="left", fill="both", expand=True, padx=2)

        center_frame = tk.Frame(container, bg="#E9E9E9")
        center_frame.pack(side="left", fill="both", expand=True, padx=2)

        right_frame = tk.Frame(container, bg="#E9E9E9")
        right_frame.pack(side="right", fill="both", expand=True, padx=2)

        third = len(keys) // 3
        left_keys = keys[:third]
        center_keys = keys[third:2*third]
        right_keys = keys[2*third:]

        for key in left_keys:
            frame = tk.Frame(left_frame, bg="#E9E9E9")
            frame.pack(fill="x", pady=1)
            tk.Label(frame, text=self.format_key(key, format), width=17, anchor="w", bg="#E9E9E9").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry

        for key in center_keys:
            frame = tk.Frame(center_frame, bg="#E9E9E9")
            frame.pack(fill="x", pady=1)
            tk.Label(frame, text=self.format_key(key, format), width=17, anchor="w", bg="#E9E9E9").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry

        for key in right_keys:
            frame = tk.Frame(right_frame, bg="#E9E9E9")
            frame.pack(fill="x", pady=1)
            tk.Label(frame, text=self.format_key(key, format), width=17, anchor="w", bg="#E9E9E9").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry

    def add_checkboxes_section(self, section_name, keys, format, bg_color="#E9E9E9"):
        tk.Label(self.frame, text=section_name, font=("Arial", 12, "bold"), bg=bg_color).pack(anchor="w", pady=1, fill="x")
        container = tk.Frame(self.frame, bg=bg_color)
        container.pack(fill="x", padx=1)

        left_frame = tk.Frame(container, bg=bg_color)
        left_frame.pack(side="left", fill="both", expand=True, padx=1)

        center_frame = tk.Frame(container, bg=bg_color)
        center_frame.pack(side="left", fill="both", expand=True, padx=1)

        right_frame = tk.Frame(container, bg=bg_color)
        right_frame.pack(side="right", fill="both", expand=True, padx=1)

        third = len(keys) // 3
        left_keys = keys[:third]
        center_keys = keys[third:2*third]
        right_keys = keys[2*third:]

        for key in left_keys:
            self.check_vars[key] = tk.BooleanVar()
            check = tk.Checkbutton(left_frame, text=self.format_key(key, format), variable=self.check_vars[key], bg=bg_color)
            check.pack(anchor="w")

        for key in center_keys:
            self.check_vars[key] = tk.BooleanVar()
            check = tk.Checkbutton(center_frame, text=self.format_key(key, format), variable=self.check_vars[key], bg=bg_color)
            check.pack(anchor="w")

        for key in right_keys:
            self.check_vars[key] = tk.BooleanVar()
            check = tk.Checkbutton(right_frame, text=self.format_key(key, format), variable=self.check_vars[key], bg=bg_color)
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
        #messagebox.showinfo("Save Successful", f"Settings saved to {self.settings_file}")
    
    def save_and_quit(self):
        self.save_settings()
        self.master.quit()
        
        # Append non-editable settings
        self.append_fixed_settings()

    def append_fixed_settings(self):
        fixed_settings = """
PATHTOAHK=C:\\Program Files\\AutoHotkey\\AutoHotkey.exe
trip_dur=0
getoff_dur=0
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
earthquake_dur=0
repl_dur=0
debug_dur=0
debug_cd=0
save_cd=0
save_dur=0
actors-on_dur=0
actors-off_dur=0
actors-on_cd=0
actors-off_cd=0
melt_cd=0
endlessfall_cd=0
burn_cd=0
shift_cd=0
randompoint_cd=0
sfx_dur=0
playhint_dur=0
collected_cd=0
minuscell_dur=0
pluscell_dur=0
minusorbs_dur=0
plusorbs_dur=0
ghostjak_cd=0
flatjak_cd=0
smalljak_cd=0
bigjak_cd=0
widejak_cd=0
nuka_dur=0
unzoom_dur=0
drown_cd=0
drown_dur=0
press_dur=0
lang_dur=0
maxfish_dur=0
customfish_dur=0
timeofday_dur=0
turn-left_dur=0
turn-right_dur=0
turn-180_dur=0
cam-left_dur=0
cam-right_dur=0
cam-in_dur=0
cam-out_dur=0
save_cost=0
actors-on_cost=0
actors-off_cost=0
debug_cost=0
"""
        with open(self.settings_file, 'a') as f:
            f.write(fixed_settings.strip())
        # messagebox.showinfo("Fixed Settings Added", "Fixed settings appended to the .env file")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set the window size
    root.configure(bg="#E9E9E9")  # Change background color of the main window
    app = SettingsApp(root)
    root.mainloop()
