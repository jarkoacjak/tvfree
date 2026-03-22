import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Zakladne nastavenia (Kodi engine)
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def create_item(label, action, icon=None, is_folder=True, video_url=None):
    """Tato funkcia vytvori polozku v menu. Label je text, ktory uvidis v Kodi."""
    if video_url:
        url = f"{BASE_URL}?action=play&url={urllib.parse.quote_plus(video_url)}&title={urllib.parse.quote_plus(label)}"
    else:
        url = f"{BASE_URL}?action={action}"
        
    list_item = xbmcgui.ListItem(label=label)
    if icon:
        list_item.setArt({'icon': icon, 'thumb': icon})
    
    if not is_folder:
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': label})

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

def main_menu():
    """Hlavne menu - texty su po slovensky pre Jarka."""
    create_item("Slovenské TV", "list_sk", is_folder=True)
    create_item("České TV", "list_cz", is_folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_tv():
    """Zoznam stanic - M3U8 a loga su pridane podla tvojich poziadaviek."""
    # TV JOJ
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    joj_logo = "https://upload.wikimedia.org/wikipedia/commons/e/ee/Logo_TV_JOJ_-_2020.svg"
    create_item("TV JOJ", "play", icon=joj_logo, is_folder=False, video_url=joj_url)

    # JOJ KRIMI
    krimi_url = "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8"
    krimi_logo = "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png"
    create_item("JOJ Krimi", "play", icon=krimi_logo, is_folder=False, video_url=krimi_url)

    # SENZI TV
    senzi_url = "https://lb.streaming.sk/senzi/stream/playlist.m3u8"
    senzi_logo = "https://lookaside.fbsbx.com/lookaside/crawler/instagram/televiziasenzi/profile_pic.jpg"
    create_item("Senzi TV", "play", icon=senzi_logo, is_folder=False, video_url=senzi_url)

    xbmcplugin.endOfDirectory(HANDLE)

def play_video(stream_url, window_title):
    """Spustenie videa. Tu pridavame simulaciu prehliadaca Chrome, aby JOJ isla."""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    # Pre JOJ musime poslat 'Referer', inak nam video zamietnu
    if "joj.sk" in stream_url:
        final_url = f"{stream_url}|User-Agent={urllib.parse.quote_plus(user_agent)}&Referer={urllib.parse.quote_plus('https://www.joj.sk/')}"
    else:
        final_url = f"{stream_url}|User-Agent={urllib.parse.quote_plus(user_agent)}"
    
    list_item = xbmcgui.ListItem(path=final_url)
    list_item.setInfo('video', {'title': window_title})
    
    # InputStream Adaptive - toto je dolezite pre m3u8 streamy
    list_item.setProperty('inputstream', 'inputstream.adaptive')
    list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

def show_czech_message():
    """Oznam pre Ceske TV - presne podla tvojho zadania."""
    xbmcgui.Dialog().ok("TV Free", "Pripravujeme Čoskoro")

# --- SMEROVAC (ROUTER) ---
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if action == 'list_sk':
    list_slovak_tv()
elif action == 'list_cz':
    show_czech_message()
elif action == 'play':
    play_video(params.get('url'), params.get('title'))
else:
    main_menu()
    
