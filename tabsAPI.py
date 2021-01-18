import subprocess
import os
import json
import time

# Input controllers
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html


class TabsSession():

    def __init__(self, gameData:dict, mouseController, keyboardController, sessionData:dict):
        self.Mouse = mouseController
        self.Keyboard = keyboardController

        self.GameStartUpDelay = gameData['GameStartupDelay']
        self.InterInputDelay = gameData['InterInputDelay']
        self.UnitStep = gameData['UnitStep']
        self.ShortDelay = gameData['ShortDelay']

        self.InputFields = gameData['inputFields']

        self.SessionData = sessionData
        self.GameData = gameData

        self.TabsProc = None
        self.KillFlip = False
        self.SessionActive = False

    def StartUpTabs(self):
        """Start the game via the EXE and clicking to the map menu"""
        self.TabsProc = subprocess.Popen([self.GameData['pathToGameExe']])

        # Wait for the game itself to start up
        time.sleep(self.GameStartUpDelay)

        # Click the EULA Button
        self.Mouse.position = (self.InputFields['EULA OK'][0], self.InputFields['EULA OK'][1])
        self.Mouse.click(Button.left, 1)
        time.sleep(self.GameStartUpDelay)

        # Click the Sandbox Button
        self.Mouse.position = (self.InputFields['Sandbox Mode'][0], self.InputFields['Sandbox Mode'][1])
        self.Mouse.click(Button.left, 1)

        return self.TabsProc

    def SelectMap(self):
        """Select a map based on the session config requirements"""
        # Click on Map Type
        self.Mouse.position = (self.InputFields[self.SessionData['mapType']][0], self.InputFields[self.SessionData['mapType']][1])
        self.Mouse.click(Button.left, 1)
        time.sleep(self.InterInputDelay)

        # Click on Chosen map by index
        mapIndex = self.SessionData['mapIndex']
        mapButtonX = self.InputFields['Maps Start'][0] + (mapIndex * self.InputFields['Maps Start'][0])
        mapButtonY = self.InputFields['Maps Start'][1] + (mapIndex * self.InputFields['Maps Start'][1])

        self.Mouse.position = (mapButtonX, mapButtonY)
        self.Mouse.click(Button.left, 1)
        time.sleep(self.InterInputDelay)

    def PlaceUnits(self, layout:list, dirKey1:str, dirKey2:str):

        # reset mouse
        self.Mouse.position = (self.GameData['GameWindowSizes'][0] / 2, self.GameData['GameWindowSizes'][1] / 2)

        # Move to initial paint position (halfway of the layout height)
        layoutHeight = len(layout)

        # from center move up halfway of layout to start the paint
        for move in range(0, int(layoutHeight/2) + 1):
            self.Keyboard.press('w')
            time.sleep(self.UnitStep)
            self.Keyboard.release('w')
            time.sleep(self.UnitStep)

        # Paint alternate the direction for each row
        alternate = True

        rowLen = None

        print('Painting')
        for row in layout:
            row = row.replace('\n', '')

            rowPieces = row.split(',')

            if rowLen is None:
                rowLen = len(rowPieces)

            # if on an alternated row, reverse the entries
            if alternate == False:
                rowPieces.reverse()

            #print('Row {} - Len {}'.format(rowPieces, len(rowPieces)))

            for piece in rowPieces:

                if piece != '-1' and len(piece) > 0:
                    # Get faction index
                    #print('Placing {}'.format(piece))
                    unitPieces = piece.split('-')

                    factionIndex = unitPieces[0]

                    unitIndex = unitPieces[1]

                    # Select faction and unit
                    self.Mouse.position = (self.InputFields['Faction {}'.format(factionIndex)][0], self.InputFields['Faction {}'.format(factionIndex)][1])
                    time.sleep(self.UnitStep)
                    self.Mouse.click(Button.left, 1)
                    time.sleep(self.UnitStep)

                    self.Mouse.position = (self.InputFields['Unit {}'.format(unitIndex)][0], self.InputFields['Unit {}'.format(unitIndex)][1])
                    time.sleep(self.UnitStep)
                    self.Mouse.click(Button.left, 1)
                    time.sleep(self.UnitStep)

                    # reset mouse
                    self.Mouse.position = (self.GameData['GameWindowSizes'][0] / 2, self.GameData['GameWindowSizes'][1] / 2)

                    # place unit
                    time.sleep(self.UnitStep)
                    self.Mouse.click(Button.left, 1)
                    time.sleep(self.UnitStep)

                # move down the row
                if alternate:
                    self.Keyboard.press(dirKey1)
                    time.sleep(self.UnitStep)
                    self.Keyboard.release(dirKey1)
                else:
                    self.Keyboard.press(dirKey2)
                    time.sleep(self.UnitStep)
                    self.Keyboard.release(dirKey2)

                time.sleep(self.ShortDelay)

            # Move one row down
            self.Keyboard.press('s')
            time.sleep(self.UnitStep)
            self.Keyboard.release('s')
            time.sleep(self.ShortDelay)

            # Also, adjust by one on the ALTER case
            if alternate:
                alternate = False
                self.Keyboard.press(dirKey2)
                time.sleep(self.UnitStep)
                self.Keyboard.release(dirKey2)
                time.sleep(self.UnitStep)
            else:
                alternate = True
                self.Keyboard.press(dirKey1)
                time.sleep(self.UnitStep)
                self.Keyboard.release(dirKey1)
                time.sleep(self.UnitStep)

        # return to start, first go back up to middle
        for move in range(0, int(layoutHeight/2)):
            self.Keyboard.press('w')
            time.sleep(self.UnitStep)
            self.Keyboard.release('w')
            time.sleep(self.UnitStep)

        # adjust back to center
        for move in range(0, rowLen):

            if alternate:
                self.Keyboard.press(dirKey1)
            else:
                self.Keyboard.press(dirKey2)

            time.sleep(self.UnitStep)

            if alternate:
                self.Keyboard.release(dirKey1)
            else:
                self.Keyboard.release(dirKey2)

            time.sleep(self.UnitStep)

    def StartSession(self, redLayout:list, blueLayout:list):
        """Start a session of combat, prep, then execution"""

        if self.KillFlip and self.SessionActive:
            time.sleep(1)

        self.SessionActive = True
        self.KillFlip = False

        # Interupt the current run (if one is happening)
        self.Keyboard.press(Key.tab)
        time.sleep(self.UnitStep)
        self.Keyboard.release(Key.tab)
        time.sleep(self.UnitStep)

        # Select the map
        # Open the menu
        self.Keyboard.press(Key.esc)
        time.sleep(1)
        self.Keyboard.release(Key.esc)
        time.sleep(1)

        # Click on select map
        self.Mouse.position = (self.InputFields['Select Map'][0], self.InputFields['Select Map'][1])
        time.sleep(1)
        self.Mouse.click(Button.left, 1)
        time.sleep(1)

        self.SelectMap()

        # Repaint the layouts

        # Clear Red
        self.Mouse.position = (self.InputFields['Clear Red'][0], self.InputFields['Clear Red'][1])
        self.Mouse.click(Button.left, 1)
        time.sleep(self.UnitStep)

        # Clear Blue
        self.Mouse.position = (self.InputFields['Clear Blue'][0], self.InputFields['Clear Blue'][1])
        self.Mouse.click(Button.left, 1)
        time.sleep(self.UnitStep)

        # reset mouse
        self.Mouse.position = (self.GameData['GameWindowSizes'][0] / 2, self.GameData['GameWindowSizes'][1] / 2)

        self.PlaceUnits(redLayout, 'a', 'd')

        self.PlaceUnits(blueLayout, 'd', 'a')

        # Start
        print('Starting')
        self.Keyboard.press(Key.tab)
        time.sleep(self.UnitStep)
        self.Keyboard.release(Key.tab)

        # go though the cameras
        cameras = self.SessionData['Camera-Positions']

        for camera in cameras:
            if self.KillFlip:
                break
            else:
                # move camera to new position
                duration = camera["duration"]
                zoomLevel = camera["zoom"]
                relX = camera['relX']
                relY = camera['relY']

                # move
                # UNIMPLEMENTED THE MOVE

                # zoom
                # Unimplemented zoom, just do a few steps out

                for zoomDegree in range(0, 3):
                    self.Keyboard.press('s')
                    time.sleep(self.ShortDelay)
                    self.Keyboard.release('s')
                    time.sleep(self.ShortDelay)

                if duration == -1:
                    # no other camera position
                    break
                else:
                    # wait to move to new position
                    time.sleep(duration)


