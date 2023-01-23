 # Opengoal-Twitch-CrowdControl  

# Install Instructions
[Download latest](https://github.com/zedb0t/Opengoal-Twitch-CrowdControl/releases/latest/download/Opengoal-Twitch-CrowdControl.rar) [![Github All Releases](https://img.shields.io/github/downloads/zedb0t/Opengoal-Twitch-CrowdControl/total.svg)]()

You need the following in this order:  
Place `OpenGoalTwitchv.exe` and the `.env` file you downloaded inside of a folder next to `gk.exe` and `goalc.exe`  
Modify the contents of `.env` so that it listens for commands in your channel by opening it with notepad making changes and then saving, make sure to save as ALL FILE TYPES If you do not change this it will save it as `.env.txt` and not work. 
Open `OpenGoalTwitchv0.3` and it should automatically open `gk` and `goalc` and connect to twitch, now you are good to go!  

# Commands
### Controlling Jak
Right now there is NO way to directly move Jak (e.g. as if using the left stick), instead you'll need to punch and turn to move around. These don't currently work while the game is paused.
- `#square` `#x` `#triangle` `#circle` Pushes the corresponding button on the controller.
- `#turn-left` `#turn-right` Turns Jak 45 degrees
- `#cam-left` `#cam-right` Turns the camera slightly
- `#cam-in` Pushes the camera slightly in
- `#cam-out` Pulls the camera slightly out
- `#up` `#down` `#left` `#right` Pushes the corresponding D-Pad button on the controller (e.g. for warp gates)

### Altering Gameplay
- `#rjto amount` Sets rolljump distance. 
  - `amount` should be between [-200, 200], default is 17.3. 
  - Examples `#rjto 50` `#rjto -10`
- `#superjump` Gives Jak super high jumps.
- `#superboosted` Gives Jak super far boosteds.
- `#noboosteds` Makes boosteds impossible.
- `#fastjak` Sets Jak’s movement speeds very high.
- `#slowjak` Removes rolljumps and sets Jak’s movement speeds very low. Gives permanent yellow eco to remove punching.
- `#slippery` Makes the terrain slippery like ice.
- `#pacifist` Removes most of Jak’s attack options.
- `#trip` Trips Jak.
- `#shortfall` Sets the fall damage distance very low.
- `#ghostjak` Gets rid of Jak’s collision for a few seconds and causes him to fall through terrain.
- `#rocketman` Propels Jak into the air like a rocket.
- `#getoff` Boots Jak off the Zoomer and Flut Flut, as well as some minigames.
- `#unzoom` Exits the goggles if Jak is using them.
- `#flutspeed amount` Sets Flut Flut’s running speed. 
  - `amount` should be between [-200, 200], default is 20. 
  - Examples `#flutspeed 0` `#flutspeed 70` `#flutspeed 20`
- `#freecam` Puts the player into freecam for a few seconds.
- `#enemyspeed enemy-name amount` Sets the speed of the specified `enemy-name` (you need the proper name of the enemy for this to work)
  - `amount` should be between [-200, 200].
  - Examples `#enemyspeed babak 2` `#enemyspeed junglefish 5` `#enemyspeed lurkerpuppy 80` `#enemyspeed green-eco-lurker 0`

### Collectables & Powerups
- `#give type amount` Gives the player the specified 'amount' of cells or orbs. Use negative `amount` to take away cells or orbs.
  - For `type`, use `fuel` for Power Cells, and `money` for Precursor Orbs. 
  - Examples `#give fuel 1` `#give money 120` `#give money -200`
- `#collected type amount` Sets the cell or orb count to a specified value. 
  - For `type`, use `fuel` for Power Cells, and `money` for Precursor Orbs.
  - Examples `#collected fuel 20` `#collected fuel 0` `#collected money 99999`
- `#eco type` Gives Jak a full meter of a specified eco type.
  - `type` should be the eco color: `red` `blue` `yellow` or `green`
  - Examples `#eco blue` `#eco yellow` `#eco green`
- `#sucksuck amount` Sets the distance of the blue eco pull power. 
  - `amount` should be between [-200, 200], default is 12.
  - Examples `#sucksuck 0` `#sucksuck 100` `#sucksuck 12`
- `#noeco` Removes Jak’s ability to use eco powerups.

### Warping
- `#die` Resets Jak to the current checkpoint, as if he died.
- `#topoint checkpoint-name` Warps Jak to a specified checkpoint. You will need the [proper name of the checkpoint](https://github.com/Zedb0T/Opengoal-Twitch-CrowdControl/blob/9e9143a03352a57b3ae2a82ec03c709cdb222f06/resources/twitchcommands.py#L186-L200).
  - Examples `#topoint game-start` `#topoint jungle-tower` `#topoint snow-fort`
- `#randompoint` Warps Jak to a random checkpoint that isn’t after Volcanic Crater.
- `#tp x y z` Warps Jak to a specified coordinate point.
  - X and Z control horizontal position, Y controls vertical position.
  - Examples `#tp 0 0 0` `#tp -32 48 173` `#tp 901 -13 -1228`
- `#shift x y z` Warps Jak to a specified coordinate point relative to his current position, in meters.
  - Examples `#shift 0 -10 0` `#shift 10 10 10` `#shift 100 0 100`
- `#movetojak actor-name` Warps a specified actor to Jak’s position. You will need the proper name of the actor, not just the type (e.g. `farmer-3` not just `farmer`). An actor must be loaded in to be moved. Be careful of crashes.
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

### Misc
- `#protect` Protects the player by disabling all commands for a certain amount of time. If sacrifices are enabled, this will time out the user.
- `#invertcam pov axis` Inverts the current camera setting of a specified point of view and axis. 
  - `pov` should be `first` or `third`. 
  - `axis` should be `h` or `v`, refering to horizontal and vertical axes respectively.
  - Examples `#invertcam third h` `#invertcam first v` `#invertcam third v`
- `#stickycam` Freezes the camera in place and disables zooming for a few seconds.
- `#normalcam` Sets all the camera settings to normal.
- `#deload` Deloads the current level. Be careful of crashes.
- `#quickcam` Puts the player into freecam and immediately back out (stores levels).
- `#dark` Sets the current level’s mood to very dark.
- `#dax` Removes Daxter.
- `bighead` Enables big head cheat.
- `smallhead` Enables small head cheat.
- `bigfist` Enables big fist cheat.
- `bigheadnpc` Enables big head NPC cheat.
- `hugehead` Enables huge head cheat.
- `mirror` Enables mirror mode cheat.
- `notex` Enables no textures cheat.
- `#smalljak` Makes Jak small.
- `#bigjak` Makes Jak big.
- `#widejak` Makes Jak wide.
- `#flatjak` Makes Jak flat.
- `#scale x y z` Changes the scale of Jak based on axes. 
  - Values should be between [-15, 15].
  - Examples `#scale 10 1 1` `#scale 1 15 1` `#scale 1 1 1`
- `#color r g b` Changes Jak’s color based on RGB values.
  - Examples `#color 50 50 50` `#color 3.5 0 3.5` `#color 1 1 1`
- `#smallnet` Sets the fishing net width to very small.
- `#widefish` Sets the fishing river width to unfairly large.
- `#lowpoly` Sets the level of detail to low.
- `#resetactors` Resets all actors to their default states (enemies, crates, and other interactable aspects).
- `#moveplantboss` Moves the plant boss to a corner in the temple and eats Jak. Only use when actually in the temple.
- `#moveplantboss2` Moves the plant boss to a corner in the temple without eating Jak. Only use when actually in the temple.
- `#basincell` Swaps the spot of the jump cell in Precursor Basin.
