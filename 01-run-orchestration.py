import subprocess
import os
import json
import time
import tabsAPI

# Input controllers
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html


if __name__ == '__main__':

    gameDataFP = open('./game-config.json', 'r')
    gameData = json.load(gameDataFP)
    gameDataFP.close()

    gamePath = gameData['pathToGameExe']
    gameActionDelay = gameData['InterInputDelay']

    if os.path.exists(gamePath):

        tabs = None

        try:

            mouse = Controller()
            keyboard = KeyboardController()

            gameLoop = True

            # Reread session details
            sessionFP = open('./session-config.json', 'r')
            session = json.load(sessionFP)
            sessionFP.close()

            tabs = tabsAPI.TabsSession(gameData, mouse, keyboard, session)

            tabProc = tabs.StartUpTabs()

            while(gameLoop):

                # Tabs input loop, wait for external input to guide next action
                nextAction = input('Next action:')

                if 'STOP' in nextAction.upper():
                    # Stop all
                    gameLoop = False
                    raise Exception("Stopping")
                elif 'NEW' in nextAction.upper():
                    time.sleep(5)

                    # Reread the layouts
                    blueFP = open('./blu-layout.csv', 'r')
                    blueLines = blueFP.readlines()
                    blueFP.close()

                    redFP = open('./red-layout.csv', 'r')
                    redLines = redFP.readlines()
                    redFP.close()

                    tabs.SelectMap()

                    tabs.StartSession(redLines, blueLines)

        except Exception as ex:
            print(str(ex))

        finally:

            if tabProc is not None:
                tabProc.kill()
                tabProc.wait()

    else:
        print('TABS not installed!')
