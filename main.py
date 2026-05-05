import sys
import os
import urllib.parse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

# --- Nastavenia ---
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
ADDON_DATA_PATH = xbmcvfs.translatePath("special://profile/addon_data/plugin.video.jarko_tv/")

if not xbmcvfs.exists(ADDON_DATA_PATH):
    xbmcvfs.mkdir(ADDON_DATA_PATH)

def add_directory_item(label, action, icon=None, is_folder=True, video_url=None, tvg_id=""):
    """Vytvorí položku. tvg_id je kľúčové pre tvoj tvfreeepg.xml."""
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
        # TU JE ZMENA: Vymazali sme 'plot', aby Kodi bralo dáta z tvojho XML
        list_item.setInfo('video', {'title': label})
        # Priradenie ID stanice, aby ho PVR klient vedel spárovať
        list_item.setProperties({'tvg-id': tvg_id, 'tvg-logo': icon})

    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=is_folder)

# --- ZOZNAM STANÍC ---
# Upravené tak, aby sedeli s tvojím XML
CHANNELS_SK = [
    ("TV JOJ", "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "JOJ.sk", "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"),
    ("JOJ Plus", "https://i.ibb.co/21Xx2nnd/joj-plus.png", "JOJPlus.sk", "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8"),
    ("JOJ KRIMI", "https://img.telkac.zoznam.sk/data/images/channel/2026/03/04/image_new_137.thumb.png", "JOJKrimi.sk", "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8"),
    ("JOJ 24", "https://img.joj.sk/38a52c95-84ce-4c04-b70a-2289a9fd1541", "JOJ24.sk", "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8"),
    ("JOJ Šport", "https://img.joj.sk/rx660n/662097da-11c1-434a-a923-3e00cdcb81e7", "JOJSport.sk", "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8"),
    ("Šport STVR", "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=1451376403675507", "STV4.sk", "https://n16.stv.livebox.sk/stv-tv/_definst_/stv4-lq.smil/playlist.m3u8?auth=b64:X2FueV98MTc3Nzk5NDQwMHwyZjhmMWJiMmZjN2JjNGYwNmQ4NTE0YmJkNjAwM2I4ZTQyMjg0MWFh")
]

CHANNELS_CZ = [
    ("ČT Sport", "https://www.itelka.sk/wp-content/uploads/2023/04/ct-sport.png", "CTSport.cz", "http://88.212.15.19/live/test_ctsport_25p/playlist.m3u8"),
    ("ČT 24", "https://pecka.tv/wp-content/uploads/2025/12/studio-ct24-400x600.jpg", "CT24.cz", "https://dash2.antik.sk/live/ct24_avc_25p/playlist.m3u8")
]

# --- FUNKCIE PRE PVR ---

def setup_pvr_playlist():
    """Vytvorí playlist.m3u, ktorý si pridáš do PVR klienta."""
    m3u_path = os.path.join(ADDON_DATA_PATH, "playlist.m3u")
    try:
        with open(m3u_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            all_channels = CHANNELS_SK + CHANNELS_CZ
            for name, logo, tid, url in all_channels:
                f.write(f'#EXTINF:-1 tvg-id="{tid}" tvg-logo="{logo}",{name}\n{url}\n')
        xbmcgui.Dialog().ok("Jarko TV", f"Playlist vygenerovaný!\nNezabudni ho pridať do PVR klienta.")
    except Exception as e:
        xbmcgui.Dialog().error("Chyba", str(e))

def setup_pvr_epg():
    """Návod pre teba."""
    xbmcgui.Dialog().ok("EPG", "V PVR klientovi nastav ako zdroj EPG tvoj súbor: tvfreeepg.xml")

# --- MENU STRUKTÚRA ---

def show_main_menu():
    add_directory_item("Živé vysielania", "live_menu", is_folder=True)
    add_directory_item("Generovať playlist pre PVR", "set_pvr_playlist", is_folder=False)
    add_directory_item("Info o EPG", "set_pvr_epg", is_folder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def show_live_menu():
    add_directory_item("Slovenské TV", "list_sk", is_folder=True)
    add_directory_item("České TV", "list_cz", is_folder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def list_slovak_channels():
    for name, logo, tid, url in CHANNELS_SK:
        add_directory_item(name, "play", icon=logo, is_folder=False, video_url=url, tvg_id=tid)
    xbmcplugin.endOfDirectory(HANDLE)

def list_czech_channels():
    for name, logo, tid, url in CHANNELS_CZ:
        add_directory_item(name, "play", icon=logo, is_folder=False, video_url=url, tvg_id=tid)
    xbmcplugin.endOfDirectory(HANDLE)

def play_video(stream_url, title):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    referer = "https://www.joj.sk/"
    final_url = f"{stream_url}|User-Agent={urllib.parse.quote(user_agent)}&Referer={urllib.parse.quote(referer)}"
    list_item = xbmcgui.ListItem(path=final_url)
    list_item.setInfo('video', {'title': title})
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

# --- Router ---
if __name__ == '__main__':
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    action = params.get('action')
    if action == 'live_menu':
        show_live_menu()
    elif action == 'list_sk':
        list_slovak_channels()
    elif action == 'list_cz':
        list_czech_channels()
    elif action == 'set_pvr_playlist':
        setup_pvr_playlist()
    elif action == 'set_pvr_epg':
        setup_pvr_epg()
    elif action == 'play':
        play_video(params.get('url'), params.get('title'))
    else:
        show_main_menu()

