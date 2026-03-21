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
        # Nastavenie informácií o videu pre prehrávač
        list_item.setInfo('video', {'title': label})
        
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

def main_menu():
    """Hlavná ponuka: Slovenské a České TV."""
    # Odkazy na podmenu
    sk_url = f"{BASE_URL}?action=list_sk"
    cz_url = f"{BASE_URL}?action=list_cz"
    
    create_item("Slovenské TV", sk_url, is_folder=True)
    create_item("České TV", cz_url, is_folder=False)
    
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_tv():
    """Zoznam slovenských staníc."""
    # TV JOJ Stream
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    
    # OPRAVA PRE M3U8: Pridanie User-Agenta, aby stream nezlyhal
    # Reťazec za '|' povie Kodi, ako sa má predstaviť serveru
    user_agent = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    full_url = joj_url + user_agent
    
    # Priame logo (YouTube profil JOJ)
    joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
    
    create_item("TV JOJ", full_url, is_folder=False, icon=joj_logo)
    
    xbmcplugin.endOfDirectory(HANDLE)

def show_cz_notice():
    """Zobrazenie správy pre České TV."""
    dialog = xbmcgui.Dialog()
    dialog.notification('TV Free', 'Pripravujeme, pribudnú čoskoro!', xbmcgui.NOTIFICATION_INFO, 5000)
    # Po oznámení zostaneme v hlavnom menu
    main_menu()

# --- SPRACOVANIE POŽIADAVIEK (ROUTER) ---
# Toto rozdelí URL a zistí, na čo používateľ klikol
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if not action:
    main_menu()
elif action == 'list_sk':
    list_slovak_tv()
elif action == 'list_cz':
    show_cz_notice()
    
