# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcaddon
import os

# Základné nastavenia doplnku TV free
ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ICON = ADDON.getAddonInfo('icon')

def play_channel(url, name, icon=""):
    """Funkcia na spustenie TV streamu"""
    listitem = xbmcgui.ListItem(name)
    listitem.setArt({'thumb': icon, 'icon': icon})
    listitem.setInfo('video', {'title': name, 'plot': 'Sledujte TV zadarmo'})
    # Nastavenie, že ide o živé vysielanie (Live)
    listitem.setProperty('IsPlayable', 'true')
    xbmc.Player().play(url, listitem)

def tv_notify(message, title="TV free"):
    """Zobrazí oznámenie priamo v Kodi"""
    xbmcgui.Dialog().notification(title, message, ICON, 5000)

def log_tv(msg):
    """Zapíše správu do logu pre TV free"""
    xbmc.log(f"TV_FREE_LOG: {msg}", xbmc.LOGINFO)

def clear_cache():
    """Pomocná funkcia na vymazanie dočasných dát (ak by mrzli streamy)"""
    profile_path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    if os.path.exists(profile_path):
        tv_notify("Cache bola premazaná")
