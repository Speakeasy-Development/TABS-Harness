import http.server

# Take in Post requests from the server, setup the config files
# https://floatingoctothorpe.uk/2017/receiving-files-over-http-with-python.html
#

import os
import sys
import http.server
import json
import datetime
from http import cookies
from typing import Tuple
import random
import tabsAPI

# Input controllers
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html


class ApiRequestHandler(http.server.SimpleHTTPRequestHandler):


    def do_POST(self):

        # Parse out necessary parameters
        length = int(self.headers['content-length'])

        action = self.path

        if 'start' in action:
            # Start the game session
            if tabs.SessionActive:
                tabs.KillFlip = True

            # set HTTP headers
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.flush_headers()

            self.end_headers()

            # Finish web transaction
            self.wfile.write(''.encode())

            # Reread the layouts
            blueFP = open('./blue-layout.csv', 'r')
            blueLines = blueFP.readlines()
            blueFP.close()

            redFP = open('./red-layout.csv', 'r')
            redLines = redFP.readlines()
            redFP.close()

            tabs.SelectMap()

            tabs.StartSession(redLines, blueLines)

        else:
            # Load in the layouts and put them into files

            postDataRaw = self.rfile.read(length)

            postDataRaw = postDataRaw.decode()

            data = dict()

            # parse the paras
            paras = postDataRaw.split('&')

            for para in paras:

                paraAndValue = para.split('=')

                paraName = paraAndValue[0].replace('+','-')

                data[paraName] = paraAndValue[1]

            # write to layout
            unitLayouts = data.copy()
            # remove color from the copy
            del unitLayouts['color']

            if data['color'].lower() == 'red' or data['color'].lower() == 'blue':
                layoutFP = open('./{}-layout.csv'.format(data['color']), 'w')

                rows = list()

                rowNum = 0

                rowStr = ''

                for entry in unitLayouts.keys():
                    entryX = int(entry.split('-')[0])

                    if rowNum != entryX:
                        # new row
                        rowNum = entryX

                        rowStr += '\n'
                        rows.append(rowStr)
                        rowStr = ''

                    rowStr += '{},'.format(unitLayouts[entry])


                layoutFP.writelines(rows)
                layoutFP.flush()
                layoutFP.close()

                # set HTTP headers
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.flush_headers()

                self.end_headers()

                # Finish web transaction
                self.wfile.write(''.encode())

            else:
                print('Bad format')
                # set HTTP headers
                self.send_response(409)
                self.send_header("Content-type", "text/json")
                self.flush_headers()

                self.end_headers()

                # Finish web transaction
                self.wfile.write('Bad Format'.encode())


if __name__ == '__main__':
    port = int(sys.argv[1])
    address = ''

    gameServer = http.server.HTTPServer((address, port), ApiRequestHandler)

    # 0.0.0.0 means listen on any address, stating localhost breaks it for external connections
    print('Server up http://localhost:{}/'.format(port))

    try:
        mouse = Controller()
        keyboard = KeyboardController()

        # Read in settings
        gameDataFP = open('./game-config.json', 'r')
        gameData = json.load(gameDataFP)
        gameDataFP.close()

        sessionFP = open('./session-config.json', 'r')
        session = json.load(sessionFP)
        sessionFP.close()

        # Spin up TABS
        tabs = tabsAPI.TabsSession(gameData, mouse, keyboard, session)

        tabProc = tabs.StartUpTabs()

        gameServer.serve_forever()
    except KeyboardInterrupt:
        print()
    except Exception as ex:
        print(str(ex))
    finally:
        gameServer.shutdown()
        if tabProc is not None:
            tabProc.kill()
            tabProc.wait()
        print('Server cleaned up')
