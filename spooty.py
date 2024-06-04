import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="3609e462524a462b84f3704feb653096",
                                               client_secret="a34648d3f68e4a29943d5c1b320b2c4e",
                                               redirect_uri="http://localhost/",
                                               scope="user-read-playback-state,user-modify-playback-state,user-library-read,playlist-read-collaborative,playlist-read-private"))

# +
if len(sys.argv) > 1:
    tid = sys.argv[1]
else:
    tid = 'spotify:track:4TTV7EcfroSLWzXRY6gLv6'

start = time.time()
analysis = sp.audio_analysis(tid)
delta = time.time() - start
print(json.dumps(analysis, indent=4))
print("analysis retrieved in %.2f seconds" % (delta,))


# +

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Whoops, need a username!")
#     print("usage: python user_playlists.py [username]")
#     sys.exit()

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
def play_MMM():
    
    avail_devices = sp.devices()
    
    if avail_devices["devices"] != []:
        phone_id = avail_devices["devices"][0]["id"]
        print("You are now listening on: " + avail_devices["devices"][0]["name"])
        wanted_song = int(input("Please enter song index: "))
    else:
        print("No one home!")
        return

    playlists = sp.user_playlists("08io0bu27xobjtf4ksqkm1vvg")

    for playlist in playlists['items']:
        if playlist["name"] == "Zane and Tommy Manipulator Mix":
            playlist_id = playlist["id"]
    songs = sp.playlist_items(playlist_id)
    
    
    song_id_list = []
    song_name_list = []
    for song in songs["items"]:
        song_id_list.append(song["track"]["id"])
        song_name_list.append(song["track"]["name"])
    
    song_id = song_id_list[wanted_song]
    if avail_devices["devices"][0]["is_active"] != True:
        sp.transfer_playback(phone_id)
        sp.start_playback(uris = [f"spotify:track:{song_id}"])
        print("Listening to: " + song_name_list[wanted_song])
    sp.start_playback(uris = [f"spotify:track:{song_id}"])
    print("Listening to: " + song_name_list[wanted_song])
# play_MMM()
# -


