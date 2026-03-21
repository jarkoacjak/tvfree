import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Globálne premenné pre Kodi
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def create_item(label, url, is_folder=False, icon=None):
    """Vytvorí položku v zozname Kodi."""
    list_item = xbmcgui.ListItem(label=label)
    if icon:
        list_item.setArt({'icon': icon, 'thumb': icon})
    
    if not is_folder:
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': label})
        
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

def main_menu():
    """Zobrazí základný výber: Slovenské vs České."""
    create_item("Slovenské TV", f"{BASE_URL}?action=list_sk", is_folder=True)
    create_item("České TV", f"{BASE_URL}?action=list_cz", is_folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_tv():
    """Zoznam staníc pre Slovensko."""
    # Tvoj funkčný link na TV JOJ
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    
    # Pridanie User-Agenta (Kodi ho potrebuje, aby server JOJ neodmietol spojenie)
    user_agent = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    full_stream_url = joj_url + user_agent
    
    # Tvoje logo (priamy odkaz na obrázok)
    joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
    
    create_item("TV JOJ", full_stream_url, is_folder=False, icon=joj_logo)
    xbmcplugin.endOfDirectory(HANDLE)

def show_cz_msg():
    """Oznámenie pre české stanice."""
    xbmcgui.Dialog().notification('TV Free', 'Pripravujeme, pribudnú čoskoro!', xbmcgui.NOTIFICATION_INFO, 5000)

# --- JADRO DOPLNKU (ROUTER) ---
# Rozoberieme parametre, ktoré nám posiela Kodi pri kliknutí
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if not action:
    main_menu()
elif action == 'list_sk':
    list_slovak_tv()
elif action == 'list_cz':
    show_cz_msg()
    
