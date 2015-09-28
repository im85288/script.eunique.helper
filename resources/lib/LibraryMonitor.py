#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import threading
import xbmcvfs
import random
import xml.etree.ElementTree as etree
import base64
import json
from datetime import datetime
import Utils as utils


class LibraryMonitor(threading.Thread):
    
    event = None
    exit = False
    liPath = None
    liPathLast = None
    delayedTaskInterval = 1800

    win = None
    addon = None
    addondir = None
    
    def __init__(self, *args):
        
        self.win = xbmcgui.Window( 10000 )
        self.addon = xbmcaddon.Addon(id='script.eunique.helper')
        self.addondir = xbmc.translatePath(self.addon.getAddonInfo('profile'))
        
        utils.logMsg("LibraryMonitor"," - started")
        self.event =  threading.Event()
        threading.Thread.__init__(self, *args)    
    
    def stop(self):
        utils.logMsg("LibraryMonitor"," - stop called")
        self.exit = True
        self.event.set()

    def run(self):

        lastListItemLabel = None
        self.previousitem = ""

        while (xbmc.abortRequested == False and self.exit != True):
            # monitor listitem props when videolibrary is active
            if (xbmc.getCondVisibility("[Window.IsActive(videolibrary) | Window.IsActive(movieinformation)] + !Window.IsActive(fullscreenvideo)")):
                
                self.liPath = xbmc.getInfoLabel("ListItem.Path")
                liLabel = xbmc.getInfoLabel("ListItem.Label")
                if ((liLabel != lastListItemLabel) and xbmc.getCondVisibility("!Container.Scrolling")):
                    
                    self.liPathLast = self.liPath
                    lastListItemLabel = liLabel
                    
                    # update the listitem stuff
                    try:
                        self.setGenreLabel()
                    except Exception as e:
                        utils.logMsg("Error", "ERROR in LibraryMonitor ! --> " + str(e), 0)

            xbmc.sleep(150)
            self.delayedTaskInterval += 0.15

    def setGenreLabel(self):
        #always clear the individual genre items first
        totalNodes = 10
        for i in range(totalNodes):
            if not self.win.getProperty('EuniqueSkinHelper.GenreListItem.' + str(i)):
                break
            self.win.clearProperty('EuniqueSkinHelper.GenreListItem.' + str(i))

        genre = xbmc.getInfoLabel('ListItem.Genre')
        if genre:
            if "/" in genre:
                genres = genre.split(" / ")
                count = 0
                for genre in genres:
                    self.win.setProperty("EuniqueSkinHelper.GenreListItem." + str(count),genre)
                    xbmc.log("Just set EuniqueSkinHelper.GenreListItem." + str(count) + "to genre " + str(genre))
                    count +=1
            else:
                self.win.setProperty("EuniqueSkinHelper.GenreListItem.0",genre)
                xbmc.log("Just set EuniqueSkinHelper.GenreListItem.0 to genre " + str(genre))


class Kodi_Monitor(xbmc.Monitor):
    
    WINDOW = xbmcgui.Window(10000)

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onDatabaseUpdated(self, database):
        pass                                         