# TABS-Harness
A harness for calling and automatically running TABS (totally accurate battle simulator) via configs and process communications.

* Adds an HTML frontend for orchestrating matches in TABS.
* Uses key/mouse inputs to puppet a game session.
* Reads in config files to determine game session's critieria.

This system operates on a basic loop of players setup a red or blue side, then when both parties are ready, a GO command is issued to the system to then paint those layouts in the game and then let it go.

NOTE: THIS IS A TRASHFIRE OF DEMONSTRATION CODE. HOPEFULLY SOMEONE ELSE FINISHES IT. BUT IT DOES DO PROOF OF CONCEPT. This may get work in the future, but I am open sourcing it as this may just be a flight of fancy for me.

## Setup
* Have TABS set to a windowed mode (see Troubleshooting for specific reasons and paras)

* Have a SEPERATE devices (phone, laptop, other computer, etc) for inputing to the website

* Ensure python 3+ with following libraries: pynput

## Running with Web Front End
* (Optional) Start streaming the desktop with Discord (for you and other to see game results)

* Ensure TABS is NOT RUNNING (Code will start it up)

* Run python3 01-run-input-server.py PORTNUMBER (like 8070)

* (Optional) On http://DEVICEIP:PORTNUMBER/ (from a seperate device), enter the Faction ID (0-9 for the 10 factions in order of default) and the Unit ID (0-6) as FID-UID (example: 0-0 is tribal-clubber) in any squares you want and the team (red or blue) then hit submit.

* On http://DEVICEIP:PORTNUMBER/ (from a seperate device), press the submit button at the bottom of the page to start the game.

## Running with Process Front End
* (Optional) Enter the Faction ID (0-9 for the 10 factions in order of default) and the Unit ID (0-6) as FID-UID (example: 0-0 is tribal-clubber) in any squares you want in either "blue-layout.csv" or "red-layout.csv".

* Ensure TABS is NOT RUNNING (Code will start it up)

* Run python3 01-run-orchestration.py

* Leave the mouse alone until it is on the sandbox mode screen

* Enter "NEW" into the process input prompt, then quickly click back on TABS (I am too lazy to figure out window focuses at present).

## Troubleshooting
* MOUSE CLICKING IN WRONG SPOTS :  The macros run on the resolution of the screen (assuming a middle set window of a total res of 1920 x 1080, with the game window at 1280 x 960) if there are errors where the mouse is clicking on the wrong stuff, try adjusting either the game window size or by manually finding the new coords they need with 00-find-mouse-coords.py

* UNITS PLACED IN WRONG SPOTS : There is some sensitivity to how the auto-placer works, it is possible it "jiggles" a bit when placing units, if this is bad try changing the timings of "UnitStep" or by adding more "leeway" to the layouts.

* NEED MORE SPOTS FOR PLACING UNITS (Web Front End) : To add more spots, run 00-generate-input-html.py with higher SizeX and SizeY values, then copy paste the html output into index.html's text inputs section.

