import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Nastavenia doplnku
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def vytvor_polozku(nazov, akcia, ikona=None, je_priecinok=True, adresa_streamu=None):
    """Vytvorí položku v menu Kodi."""
    if adresa_streamu:
        # Ak ide o video, vytvoríme špeciálnu URL pre prehrávanie
        url = f"{BASE_URL}?action=play&url={urllib.parse.quote_plus(adresa_streamu)}&title={urllib.parse.quote_plus(nazov)}"
    else:
        url = f"{BASE_URL}?action={akcia}"
        
    list_item = xbmcgui.ListItem(label=nazov)
    if ikona:
        list_item.setArt({'icon': ikona, 'thumb': ikona})
    
    if not je_priecinok:
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': nazov})

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=je_priecinok)

def hlavne_menu():
    """Zobrazí základné kategórie."""
    vytvor_polozku("Slovenské TV", "list_sk", je_priecinok=True)
    vytvor_polozku("České TV", "list_cz", je_priecinok=False)
    xbmcplugin.endOfDirectory(HANDLE)

def zoznam_sk_tv():
    """Zoznam slovenských staníc."""
    # TV JOJ
    joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
    joj_logo = "https://upload.wikimedia.org/wikipedia/commons/e/ee/Logo_TV_JOJ_-_2020.svg"
    vytvor_polozku("TV JOJ", "play", ikona=joj_logo, je_priecinok=False, adresa_streamu=joj_url)

    # JOJ KRIMI
    krimi_url = "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8"
    krimi_logo = "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png"
    vytvor_polozku("JOJ Krimi", "play", ikona=krimi_logo, je_priecinok=False, adresa_streamu=krimi_url)

    xbmcplugin.endOfDirectory(HANDLE)

def prehraj_stream(url_streamu, nazov_tv):
    """Spustí samotné video s hlavičkami pre JOJ."""
    # Hlavičky sú kľúčové, aby server JOJ neodmietol Kodi
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Safari/537.36"
    finalna_url = f"{url_streamu}|User-Agent={urllib.parse.quote_plus(ua)}&Referer={urllib.parse.quote_plus('https://www.joj.sk/')}"
    
    list_item = xbmcgui.ListItem(path=finalna_url)
    list_item.setInfo('video', {'title': nazov_tv})
    
    # Aktivácia InputStream Adaptive (motor pre m3u8)
    list_item.setProperty('inputstream', 'inputstream.adaptive')
    list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

def oznam_cz():
    """Zobrazí okno pre České TV."""
    xbmcgui.Dialog().ok("TV Free", "Pripravujeme čoskoro!")

# --- ROUTER (Smerovač akcií) ---
parametre = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
akcia = parametre.get('action')

if akcia == 'list_sk':
    zoznam_sk_tv()
elif akcia == 'list_cz':
    oznam_cz()
elif akcia == 'play':
    prehraj_stream(parametre.get('url'), parametre.get('title'))
else:
    hlavne_menu()
    
