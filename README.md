## LCU Online Multiplayer Mod
This is a mod for LEGO City Undercover that adds online multiplayer functionality.
The mod is currently incomplete. The version available in this repo is a prototype, and was not originally intended for public release. However, it is functional, and can be used for simple games of hide + seek.

## Current State

 - The mod currently allows for 6 players to connect and explore the overworld together. The mod does not function in levels. Also, 6 players at once has not been fully tested, so it may not work properly. 
 
- Player disguises are partially synced, meaning that if a player wears an Astronaut disguise, for example, they will appear as an Astronaut to other players, but not necessarily the same exact model (a substitute astronaut costume will be used).

- Vehicles are synced in a similar way to disguises, although there are some vehicles synced correctly. All helicopters, Chase's Narym, taxi cabs, busses, and the Guardian, will all be synced correctly. All other vehicles will appear as the Hero to other players. On the subject of taxis and busses - other players can ride in the passenger seats while one player drives.

- Animations are partially synced. Similar situation to the two sections above, where some will sync correctly and others that haven't been added yet just use the idle animation.

- The mod only works on a PC copy of the game downloaded through Steam. It will not work with pirated/cracked copies. This isn't intentional, but simply a side effect of how the mod works. Steam versions of the game bought through key resellers will work fine. Switch/Xbox/PS4/Wii U versions of the game are not supported.

- The mod can be somewhat unstable. Playtesting sessions often had a much higher frequency of game crashes than you'd expect, though some sessions were worse than others. 

- Players who are geographically far from the server host may experience large amounts of lag/latency.

- Due to the design of the mod, Act 3 and Act 4 of the game's story may become non-functional after loading a save file with the mod active. Only play on 100% files, or on saves you do not wish to complete the story on.

- The code is an enormous mess. It is not well structured or designed. If you try reading the code, expect to find many badly labelled functions/variables, as well as plenty of redundant, unused, or poorly designed code. I was in the middle of rewriting it before I stopped working on the mod, however the rewritten version is currently non-functional.

## Usage
Be aware that the mod has had relatively little testing, and you are likely to experience plenty of bugs. I am not currently actively developing the mod, and will only be able to provide limited assistance with it.

- The mod requires Python 3.10 or later to be installed, along with the `websockets` module. You also need an old version of `pymeow`. This is included in the repo. The module may trigger a false positive anti-virus warning, but it's safe. The module is on Github somewhere if you want to find it yourself. The version I have seems to be last modified on 16/02/2022, so look for something around that old. You will also need to have extracted your LCU game files.

- Once all the requirements have been installed, copy `LEVEL99.SF` and `SCRIPT.TXT` to `LEVELS\LEGO_CITY\LEGO_CITY\AI` in your LCU game files. The player who is hosting the server should now launch `server.py`. Other players must enter the server's IP address into line 71 of `client.py`. The server host must configure port forwarding on port 8765 through their router's settings.

- When setup has been completed,  launch the game, load a save file, then launch `client.py`. If everything has worked, and the server is online, the message `Connected - PID: X` should appear in the client terminal window. At this point, other players connected to the server should be visible in-game.