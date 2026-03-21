import sys
import xbmcgui
import xbmcplugin
import urllib.parse

# Premenné pre Kodi
_handle = int(sys.argv[1])
_base_url = sys.argv[0]

def create_item(label, url, is_folder=False, icon=None):
    """Vytvorí položku v zozname."""
    list_item = xbmcgui.ListItem(label=label)
    if icon:
        list_item.setArt({'icon': icon, 'thumb': icon})
    
    if not is_folder:
        list_item.setProperty('IsPlayable', 'true')
        # Povieme Kodi, že ide o HLS stream (m3u8)
        list_item.setInfo('video', {'title': label, 'mediatype': 'video'})
        
    xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=list_item, isFolder=is_folder)

def main_menu():
    """Hlavná ponuka."""
    create_item("Slovenské TV", f"{_base_url}?action=list_sk", is_folder=True)
    create_item("České TV", f"{_base_url}?action=list_cz", is_folder=False)
    xbmcplugin.endOfDirectory(_handle)

def list_slovak_tv():
    """Zoznam SK staníc."""
    # TV JOJ - tvoj funkčný odkaz
    joj_m3u8 = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    
    # Pridanie hlavičiek pre Kodi (User-Agent a Content-Type)
    # Toto je kľúčové, aby server JOJ neodmietol požiadavku
    headers = "|User-Agent=Mozilla/5.0&Content-Type=application/vnd.apple.mpegurl"
    full_url = joj_m3u8 + headers
    
    # Logo JOJ
    joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
    
    create_item("TV JOJ", full_url, is_folder=False, icon=joj_logo)
    xbmcplugin.endOfDirectory(_handle)

def show_cz_info():
    """Oznam pre České TV."""
    xbmcgui.Dialog().notification('TV Free', 'Pripravujeme, pribudnú čoskoro!', xbmcgui.NOTIFICATION_INFO, 5000)

# --- JEDNODUCHÝ ROUTER (OPRAVA CHYBY MAIN.PY) ---
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if action == 'list_sk':
    list_slovak_tv()
elif action == 'list_cz':
    show_cz_info()
else:
    main_menu()
    
