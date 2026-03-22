import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# --- Základné nastavenia ---
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def add_directory_item(label, action, icon=None, is_folder=True, video_url=None):
    """Vytvorí položku v menu Kodi."""
    query = {'action': action}
    if video_url:
        query['url'] = video_url
        query['title'] = label
        
    url = f"{BASE_URL}?{urllib.parse.urlencode(query)}"
    list_item = xbmcgui.ListItem(label=label)
    
    if icon:
        list_item.setArt({'icon': icon, 'thumb': icon})
    
    if not is_folder:
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': label})

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

def show_main_menu():
    """Hlavné menu."""
    add_directory_item("Slovenské TV", "list_sk", is_folder=True)
    add_directory_item("České TV", "list_cz", is_folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_channels():
    """Zoznam slovenských staníc."""
    # TV JOJ
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    joj_logo = "https://upload.wikimedia.org/wikipedia/commons/e/ee/Logo_TV_JOJ_-_2020.svg"
    add_directory_item("TV JOJ", "play", icon=joj_logo, is_folder=False, video_url=joj_url)

    # JOJ KRIMI
    krimi_url = "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8"
    krimi_logo = "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png"
    add_directory_item("JOJ Krimi", "play", icon=krimi_logo, is_folder=False, video_url=krimi_url)

    # SENZI TV
    senzi_url = "https://lb.streaming.sk/senzi/stream/playlist.m3u8"
    senzi_logo = "https://static.wikia.nocookie.net/cstv/images/8/85/Senzi.png"
    add_directory_item("Senzi TV", "play", icon=senzi_logo, is_folder=False, video_url=senzi_url)

    xbmcplugin.endOfDirectory(HANDLE)

def play_video(stream_url, title):
    """Spustí video s čistým nastavením hlavičiek."""
    # User-Agent simulujúci Chrome
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    # Skúsime poslať hlavičky oddelene pre vyššiu stabilitu
    final_url = stream_url + f"|User-Agent={ua}&Referer=https://www.joj.sk/"
    
    list_item = xbmcgui.ListItem(path=final_url)
    list_item.setInfo('video', {'title': title})
    
    # Nutné pre m3u8 streamy
    list_item.setProperty('inputstream', 'inputstream.adaptive')
    list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

def show_czech_notice():
    """Zobrazí tvoj text pre České TV."""
    xbmcgui.Dialog().ok("TV Free", "Pripravujeme Čoskoro")

# --- Smerovač (Router) ---
if __name__ == '__main__':
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    action = params.get('action')

    if action == 'list_sk':
        list_slovak_channels()
    elif action == 'list_cz':
        show_czech_notice()
    elif action == 'play':
        play_video(params.get('url'), params.get('title'))
    else:
        show_main_menu()
        
