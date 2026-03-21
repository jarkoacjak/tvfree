import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Premenné pre Kodi
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def create_item(label, url, icon=None, folder=False, playable=False):
    """Vytvorí položku v zozname."""
    list_item = xbmcgui.ListItem(label=label)
    if icon:
        list_item.setArt({'icon': icon, 'thumb': icon})
    
    if playable:
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': label})
        # Vynútenie prehrávača pre m3u8
        list_item.setProperty('inputstream', 'inputstream.adaptive')
        list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=folder)

def main_menu():
    """Hlavné menu."""
    create_item("Slovenské TV", f"{BASE_URL}?action=list_sk", folder=True)
    create_item("České TV", f"{BASE_URL}?action=list_cz", folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_tv():
    """Zoznam slovenských staníc."""
    # HLAVIČKA: Skúsime tento kratší User-Agent, ktorý funguje všade
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Safari/537.36"
    headers = f"|User-Agent={ua}"

    # 1. TV JOJ
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + headers
    joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
    create_item("TV JOJ", joj_url, icon=joj_logo, playable=True)

    # 2. JOJ KRIMI
    krimi_url = "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + headers
    krimi_logo = "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png"
    create_item("JOJ Krimi", krimi_url, icon=krimi_logo, playable=True)

    xbmcplugin.endOfDirectory(HANDLE)

def show_cz_msg():
    """Správa pre České TV."""
    xbmcgui.Dialog().ok("TV Free", "Pripravujeme čoskoro!")

# --- ROUTER ---
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if action == 'list_sk':
    list_slovak_tv()
elif action == 'list_cz':
    show_cz_msg()
else:
    main_menu()
    
