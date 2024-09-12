 # Opengoal-Twitch-CrowdControl  

# Install Instructions
[Download latest](https://github.com/zedb0t/Opengoal-Twitch-CrowdControl/releases/latest) [![Github All Releases](https://img.shields.io/github/downloads/zedb0t/Opengoal-Twitch-CrowdControl/total.svg)]()

alternatively, read [installation here](https://docs.google.com/document/d/14O7a4fCDzkJnegX_u_cZmCaUm_UlTUOPt5Gnu3kZ65o/edit) or [command list here](https://docs.google.com/spreadsheets/d/1Dbt7bFN86zBA32e3zciOZCRqSIW0XR0Np7HfdypAOPE/edit?usp=sharing)

You need the following in this order:  
Place `Jak1Twitch.exe` and the `EXAMPLE.env` file you downloaded inside of `Your OpenGOAL folder > versions > official > [version you’re using])` with `gk.exe` and `goalc.exe`, then rename `EXAMPLE.env` to `.env` (make sure to save as ALL FILE TYPES -- If you do not change this it will save it as `.env.txt` and not work).
Modify the contents of `.env` by opening `J1T_GUI` ([generate ouath token here](https://twitchapps.com/tmi/)) and click Save Settings. 
Open `Jak1Twitch.exe` and it should automatically open `gk` and `goalc` and connect to Twitch. Now you are good to go!  

# Commands
### Controlling Jak
Right now there is NO way to directly move Jak (e.g. as if using the left stick), instead you'll need to punch and turn to move around. These don't currently work while the game is paused.
- `#press` `x` `triangle` `circle` `up` `down` `left` `right` `l1` `r1` Pushes the corresponding button on the controller.
- `#turn-left` `#turn-right` Turns Jak 45 degrees
- `#cam-left` `#cam-right` Turns the camera slightly
- `#cam-in` Pushes the camera slightly in
- `#cam-out` Pulls the camera slightly out

### Altering Gameplay
- `#rjto amount` Sets rolljump distance.  
  - Examples `#rjto 50` `#rjto -10`
- `#superjump` Gives Jak super high jumps.
- `nojumps` Removes Jak’s ability to jump.
- `noduck` Removes Jak's ability to duck, and consequently rolljump.
- `#superboosted` Gives Jak super far boosteds.
- `#noboosteds` Makes boosteds impossible.
- `#fastjak` Sets Jak’s movement speeds very high.
- `#slowjak` Reduces rolljumps and sets Jak’s movement speeds very low.
- `#slippery` Makes the terrain slippery like ice.
- `pinball` Makes Jak go crazy, bouncing all over the place.
- `#pacifist` Removes most of Jak’s attack options.
- `#trip` Trips Jak.
- `#shortfall` Sets the fall damage distance very low.
- `#ghostjak` Gets rid of Jak’s collision for a few seconds and causes him to fall through terrain.
- `#rocketman` Propels Jak into the air like a rocket.
- `#getoff` Boots Jak off the Zoomer and Flut Flut, as well as some minigames.
- `#unzoom` Exits the goggles if Jak is using them.
- `#flutspeed amount` Sets Flut Flut’s running speed.  
  - Examples `#flutspeed 0` `#flutspeed -70` `#flutspeed 20`
- `#freecam` Puts the player into freecam for a few seconds.

### Appearance
- `#dax` Removes Daxter.
- `#smalljak` Makes Jak small.
- `#bigjak` Makes Jak big.
- `#widejak`	Makes Jak wide.
- `#flatjak`	Makes Jak flat.
- `#bighead`	Makes Jak’s head big. (Cheat)
- `#smallhead`	Makes Jak’s head small. (Cheat)
- `#bigfist`	Makes Jak’s fists big. (Cheat)
- `#hugehead`	Makes Jak’s head huge. (Cheat)
- `#bigheadnpc`	Makes all NPCs’ heads big. (Cheat)
- `#scale x y z`	Changes the scale of Jak based on axes. Goes away after a respawn.
- `#color r g b`	Changes Jak’s color based on RGB values. Goes away after a respawn.

### Collectables & Powerups
- `#minuscell` Removes power cells from the player’s inventory.
- `#pluscell`	Adds power cells to the player’s inventory.
- `#minusorbs`	Removes precursor orbs from the player’s inventory. 
- `#plusorbs`	Adds precursor orbs to the player’s inventory.
- `#give type amount` Gives the player the specified 'amount' of cells or orbs. Use negative `amount` to take away cells or orbs. 
  - Examples `#give cell 1` `#give orbs 120` `#give money -200`
- `#collected type amount` Sets the cell or orb count to a specified value. 
  - Examples `#collected fuel 20` `#collected cells 0` `#collected orbs 99999`
- `#eco type` Gives Jak a full meter of a specified eco type.
  - `type` should be the eco color: `red` `blue` `yellow` or `green`
  - Examples `#eco blue` `#eco yellow` `#eco green`
- `#sucksuck amount` Sets the distance of the blue eco pull power. 
  - Examples `#sucksuck 0` `#sucksuck 100` `#sucksuck 12`
- `#noeco` Removes Jak’s ability to use eco powerups.
- `#invuln`	Makes Jak invulnerable to most things, until a respawn.
- `#nuka`	Activates “nuka glitch.” Enemies will ignore Jak, and he cannot interact with anything. Goes away after a respawn, bonk, or damage.
- `#spiderman`	Allows Jak to climb on walls like Spider-Man (infinite jumps everywhere).
- `#rapidfire`	Makes the fire rate for yellow eco really fast.

### Warping
- `#die` Resets Jak to the current checkpoint, as if he died.
- `#topoint checkpoint-name` Warps Jak to a specified checkpoint. You can either use the [internal name](https://github.com/Zedb0T/Opengoal-Twitch-CrowdControl/blob/9e9143a03352a57b3ae2a82ec03c709cdb222f06/resources/twitchcommands.py#L186-L200) of a checkpoint or use a level’s nickname (it will teleport to a random checkpoint in that level). 
  - Examples `#topoint game-start` `#topoint jungle-tower` `#topoint snow-fort`
- `#randompoint` Warps Jak to a random checkpoint that isn’t after Volcanic Crater (by default).
- `#tp x y z` Warps Jak to a specified coordinate point. Disabled by default.
  - X and Z control horizontal position, Y controls vertical position.
  - Examples `#tp 0 0 0` `#tp -32 48 173` `#tp 901 -13 -1228`
- `#shift x y z` Warps Jak to a specified coordinate point relative to his current position, in meters.
  - Examples `#shift 0 -10 0` `#shift 10 10 10` `#shift 100 0 100`
- `#movetojak actor-name` Warps a specified actor to Jak’s position. You will need the [proper name](https://docs.google.com/spreadsheets/d/1jIa7J_eWcoZYQbXlOOIrqdNb62m79Xhld1VnqOK5XwY/edit?gid=0#gid=0) of the actor (e.g. `farmer-3` not just `farmer`). An actor must be loaded in to be moved. Be careful of crashes.
  - Examples `#movetojak farmer-3` `#movetojak money-657` `#movetojak bird-lady-4`

### Health
- `#ouch` Simply damages Jak.
- `#burn` Burns Jak.
- `#hp amount` Sets Jak’s health to a specified amount. If set to 0, he won’t die until he gets hit or bonks.
  - Examples `#hp 1` `#hp 4` `#hp 500`
- `#melt` Melts Jak, as if he fell into lava.
- `#endlessfall` Kills Jak, as if he fell into an abyss.
- `#iframes amount` Sets the duration, in seconds, of the invulnerability state after Jak takes damage. Default is 3.
  - Examples `#iframes 0` `#iframes 30` `#iframes 3`

### World
- `#deload`	Deloads the current level.
- `#mirror`	Mirrors the world. (Cheat)
- `#notex`	Removes all textures. (Cheat)
- `#lowpoly`	Sets the level of detail to low.
- `#dark`	Sets the current level’s mood to very dark.
- `#grav mode`	Sets the gravity to low or high.
- `#timeofday time`	Sets the time of day, based on a 24-hour cycle.
  - Examples `#timeofday 12` `#timeofday 4` `#timeofday 23`
- `#noactors`		Removes all actors (enemies, crates, and other interactable aspects).
- `#resetactors`	Resets all actors to their default states.

### Misc
- `#protect`	Protects the player by disabling all commands for a certain amount of time.
- `#cam mode`	Changes the camera to a specified mode. Available modes are: endlessfall, eye, standoff, bike, and stick.
- `#invertcam pov axis`	Inverts the current camera setting of a specified point of view and axis. pov = first (goggles and freecam) or third, and axis = h or v, refering to horizontal and vertical.
  - Examples `#invertcam third h` `#invertcam first v` `#invertcam first h`
- `#stickycam`	Freezes the camera in place and disables zooming for a few seconds.
- `#quickcam`	Puts the player into freecam and immediately back out (stores levels).
- `#blind seconds`	Blackens the screen for a specified amount of time.
- `#sfx name`	Plays a sound effect.
  - Examples `#sfx shark` `#sfx explode` `#sfx fall`
- `#press button`	Inputs a button press. Currently, available buttons are: square, circle, x, triangle, up, down, left, and right.
- `#lang language`	Changes the voice lines to a specified language. Available languages are: english, french, german, italian, spanish, japanese, and uk-english.
- `#smallnet`	Makes the fishing net width very small.
- `#widefish`	Makes the fishing river width unfairly large.
- `#maxfish amount`	Sets the amount of pounds of fish needed to win the minigame.
  Examples `#maxfish 50` `#maxfish 150` `#maxfish 1`
- `#hardfish`	Sets the fish difficulty to the hidden hard mode.
- `#customfish difficulty phase field value`	Allows for a custom change to the fish minigame.
  - The minigame has 6 difficulties: 0-4 are the handicap tiers, and 5 is hard fish. The minigame starts on 0 and increases by one each time a handicap is applied. Each difficulty has 7 phases (eels are 6). Available fields are: timeout, vel, swing-min, swing-max, 
    period, fish-vel, bad-percent, and powerup-percent. Use `0.0`-`1.0` for percent fields.
  - Examples `#customfish 0 2 fish-vel 5` `#customfish 0 6 fish-vel 10` `#customfish 0 4 swing-min 7` `#customfish 5 6 bad-percent 0.85` `#customfish 0 3 period 0.1` `#customfish 5 7 powerup-percent 1.0`
- `#moveplantboss`	Moves the plant boss to a corner in the temple and eats Jak. Doesn't work outside of the temple.
- `#moveplantboss2`	Moves the plant boss to a corner in the temple without eating Jak. Doesn't work outside of the temple.
- `#basincell`	Swaps the spot of the jump cell in Precursor Basin.

### Streamer
- `#enable command`	Enables a command for use.
  - Example `#enable give`
- `#disable command`	Disables a command for use.
  - Example `#disable slowjak`
- `#cd command seconds` Sets the cooldown for a command.
  - Example `#cd die 600`
- `#dur command seconds`	Sets the duration of a command.
  - Example `#dur dark 20`
- `#resetcds`	Resets the cooldowns of all commands.
- `#fixoldsave`	Fixes the “Old Save Game” bug, if it happens.
- `#start`	Allow commands to come through.
- `#stop`	Stop allowing commands to come through.
- `#active`	See all active commands in chat.
- `#finalboss`	A special mode to make final boss easier. Doubles the cooldowns of harmful commands and disables some others.
