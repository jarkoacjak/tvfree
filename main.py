import sys
import os
import urllib.parse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

# --- Nastavenia ---
# Jarko, toto sú základné premenné pre fungovanie doplnku
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

# Cesta k dátam doplnku, kam ukladáme vygenerovaný playlist
ADDON_DATA_PATH = xbmcvfs.translatePath("special://profile/addon_data/plugin.video.jarko_tv/")

if not xbmcvfs.exists(ADDON_DATA_PATH):
    xbmcvfs.mkdir(ADDON_DATA_PATH)

def add_directory_item(label, action, icon=None, is_folder=True, video_url=None, tvg_id=""):
    """Vytvorí položku v menu Kodi. tvg_id musí súhlasiť s ID v tvfeeepg.xml."""
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
        # ZMENA: setInfo sme nechali čisté, aby Kodi bralo informácie z tvojho XML
        list_item.setInfo('video', {'title': label})
        # DÔLEŽITÉ: Tieto riadky povedia Kodi, ktoré EPG patrí ku ktorému kanálu
        list_item.setProperty('tvg-id', tvg_id)
        list_item.setProperty('tvg-logo', icon)

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

# --- DEFINÍCIA KANÁLOV ---
# Jarko, tu si stráž, aby tvg-id bolo presne "JOJ.sk" (ako máš v XML)
CHANNELS_SK = [
    ("TV JOJ", "https://img.joj.sk/logo.png", "JOJ.sk", "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"),
    ("JOJ Plus", "https://i.ibb.co/21Xx2nnd/joj-plus.png", "JOJPlus.sk", "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8"),
    ("JOJ KRIMI", "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png", "JOJKrimi.sk", "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8"),
    ("JOJ 24", "https://img.joj.sk/38a52c95-84ce-4c04-b70a-2289a9fd1541", "JOJ24.sk", "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8"),
    ("JOJ Šport", "https://img.joj.sk/rx660n/662097da-11c1-434a-a923-3e00cdcb81e7", "JOJSport.sk", "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8"),
    ("Šport STVR", "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=1451376403675507", "STV4.sk", "https://n16.stv.livebox.sk/stv-tv/_definst_/stv4-lq.smil/playlist.m3u8?auth=b64:X2FueV98MTc3Nzk5NDQwMHwyZjhmMWJiMmZjN2JjNGYwNmQ4NTE0YmJkNjAwM2I4ZTQyMjg0MWFh"),
    ("Jojko", "https://i.ibb.co/TxFWhc1J/jojko.png", "Jojko.sk", "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8"),
    ("JOJ Family", "https://i.ibb.co/hJgjKqpF/joj-family.png", "JOJFamily.sk", "https://live.cdn.joj.sk/live/andromeda/family-1080.m3u8"),
    ("JOJ Cinema", "http://www.mediaguru.cz/wp-content/uploads/2016/06/Joj-Cinema_akt.png", "JOJCinema.sk", "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8"),
    ("CS History", "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836", "CSHistory.cz", "https://live.cdn.joj.sk/live/andromeda/cs_history-1080.m3u8"),
    ("CS Film", "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png", "CSFilm.cz", "https://live.cdn.joj.sk/live/andromeda/cs_film-1080.m3u8"),
    ("CS Mystery", "https://www.jojgroup.sk/wp-content/uploads/CS-mistery.png", "CSMystery.cz", "https://live.cdn.joj.sk/live/andromeda/cs_mystery-1080.m3u8"),
    ("Prima Love", "https://www.recenzer.cz/wp-content/uploads/2023/10/prima-love-logo.jpg", "PrimaLove.cz", "http://88.212.15.19/live/prima_love_avc_25p/playlist.m3u8"),
    ("TV LUX", "https://213.sk/wp-content/uploads/2020/11/tvlux.jpg", "TVLux.sk", "https://stream.tvlux.sk/luxtv/luxtv-livestream/playlist.m3u8"),
    ("TV Liptov", "https://yt3.googleusercontent.com/JJ6maA0dhvLU3z45Jhbgcc1brVZQswuPfYS6Da-Gli4MxXEPlhz5yuLkJlp7VL7mG7eSIxBORA=s900-c-k-c0x00ffffff-no-rj", "TVLiptov.sk", "http://95.105.255.137:1935/tvturiec/tvliptov.stream/playlist.m3u8"),
    ("TV Nitrička", "https://www.satelitnatv.sk/wp-content/uploads/2013/04/nitricka.jpg", "TVNitricka.sk", "https://dash4.antik.sk/live/test_nitricka/playlist.m3u8"),
    ("TV9", "https://www.fotelka.tv/image/cache/catalog/Regionalne/TV9-240x234.jpg", "TV9.sk", "https://dash4.antik.sk/live/test_tv9/playlist.m3u8"),
    ("TV 8", "https://www.digislovakia.sk/wp-content/uploads/2023/04/TV8-logo-2-300x231.png", "TV8.sk", "http://109.74.145.11:1935/tv8/ngrp:tv8.stream_all/playlist.m3u8"),
    ("Senzi TV", "https://static.wikia.nocookie.net/cstv/images/8/85/Senzi.png", "Senzi.sk", "https://lb.streaming.sk/senzi/stream/playlist.m3u8")
]

CHANNELS_CZ = [
    ("Minimax", "https://www.minimaxcz.tv/storage/images/cWiGhWyxj8fFnyWQZxEX.png", "Minimax.cz", "http://88.212.15.19/live/test_minimax/playlist.m3u8"),
    ("Óčko", "https://parasite.cz/wp-content/uploads/2013/02/ocko1.jpg", "Ocko.cz", "https://ocko-live-dash.ssl.cdn.cra.cz/cra_live2/ocko.stream.1.smil/playlist.m3u8"),
    ("ČT 24", "https://pecka.tv/wp-content/uploads/2025/12/studio-ct24-400x600.jpg", "CT24.cz", "https://dash2.antik.sk/live/ct24_avc_25p/playlist.m3u8")
]

# --- FUNKCIE PRE PLAYLIST ---

def setup_pvr_playlist():
    """Vygeneruje .m3u súbor, ktorý si Jarko vloží do IPTV Simple Clienta."""
    m3u_path = os.path.join(ADDON_DATA_PATH, "playlist.m3u")
    try:
        with open(m3u_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            all_channels = CHANNELS_SK + CHANNELS_CZ
            for name, logo, tid, url in all_channels:
                # Tu zapisujeme metaúdaje pre PVR klienta
                f.write(f'#EXTINF:-1 tvg-id="{tid}" tvg-logo="{logo}",{name}\n{url}\n')
        xbmcgui.Dialog().ok("Playlist Hotový", f"Súbor nájdeš tu:\n{m3u_path}")
    except Exception as e:
        xbmcgui.Dialog().error("Chyba", str(e))

# --- MENU ---

def show_main_menu():
    add_directory_item("Živé vysielanie", "live_menu", is_folder=True)
    add_directory_item("Vytvoriť Playlist pre PVR", "set_pvr_playlist", is_folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def show_live_menu():
    add_directory_item("Slovenské kanály", "list_sk", is_folder=True)
    add_directory_item("České kanály", "list_cz", is_folder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def list_channels(channel_list):
    for name, logo, tid, url in channel_list:
        add_directory_item(name, "play", icon=logo, is_folder=False, video_url=url, tvg_id=tid)
    xbmcplugin.endOfDirectory(HANDLE)

def play_video(stream_url, title):
    # Pridávame hlavičky, aby streamy (napr. JOJ) fungovali
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    referer = "https://www.joj.sk/"
    final_url = f"{stream_url}|User-Agent={urllib.parse.quote(user_agent)}&Referer={urllib.parse.quote(referer)}"
    
    list_item = xbmcgui.ListItem(path=final_url)
    list_item.setInfo('video', {'title': title})
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

# --- Spúšťač ---
if __name__ == '__main__':
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    action = params.get('action')
    
    if action == 'live_menu':
        show_live_menu()
    elif action == 'list_sk':
        list_channels(CHANNELS_SK)
    elif action == 'list_cz':
        list_channels(CHANNELS_CZ)
    elif action == 'set_pvr_playlist':
        setup_pvr_playlist()
    elif action == 'play':
        play_video(params.get('url'), params.get('title'))
    else:
        show_main_menu()

