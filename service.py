#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon


__settings__ = xbmcaddon.Addon(id='script.eunique.helper')
__cwd__ = __settings__.getAddonInfo('path')
__addonversion__ = __settings__.getAddonInfo('version')
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )
sys.path.append(BASE_RESOURCE_PATH)

from LibraryMonitor import LibraryMonitor
from LibraryMonitor import Kodi_Monitor

class Main:

    
    def __init__(self):

        KodiMonitor = Kodi_Monitor()

        #start the extra threads
        libraryMonitor = LibraryMonitor()
        libraryMonitor.start()

        while not (KodiMonitor.abortRequested() or xbmc.abortRequested):
            xbmc.sleep(150)
        else:
            # Abort was requested while waiting. We should exit
            xbmc.log('Eunique Helper Script --> shutdown requested !')
            #stop the extra threads
            libraryMonitor.stop()


xbmc.log('eunique helper version %s started' % __addonversion__)
Main()
xbmc.log('eunique helper version %s stopped' % __addonversion__)
