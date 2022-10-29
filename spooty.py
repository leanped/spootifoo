from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy
import time
import sys
from pyduino import *


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="3609e462524a462b84f3704feb653096",
                                               client_secret="a34648d3f68e4a29943d5c1b320b2c4e",
                                               redirect_uri="http://localhost/",
                                               scope="user-read-playback-state,user-modify-playback-state,user-library-read,playlist-read-collaborative,playlist-read-private"))


# +
def get_devices():
    
    avail_devices = sp.devices()
    global phone_id
    if avail_devices["devices"] != []:
        phone_id = avail_devices["devices"][0]["id"]
        print("You are now listening on: " + avail_devices["devices"][0]["name"])
        return True
    else:
        print("No one home!")
        
        return False

    
def get_song_data(song_id):
#     playlists = sp.user_playlists("08io0bu27xobjtf4ksqkm1vvg")

#     for playlist in playlists['items']:
#         if playlist["name"] == wanted_playlist:
#             playlist_id = playlist["id"]
#     songs = sp.playlist_items(playlist_id)
    
#     global song_name_list
#     song_id_list = []
#     song_name_list = []
#     for song in songs["items"]:
#         song_id_list.append(song["track"]["id"])
#         song_name_list.append(song["track"]["name"])
#     global song_id
#     song_id = song_id_list[wanted_song]
    
    anal = sp.audio_analysis(f"spotify:track:{song_id}")
    bass_list = []
    segment_times = []
    segment_counter = 0
    for segment in anal["segments"]:
        segment_times.append(segment["start"])
    count_segments = len(segment_times)
    
    for segment in anal["segments"]:
        segment_counter += 1
        segment_dict = {"start_time": None, "timbre_bass": None, "pitch_bass": None, "diff": None}
        pitches = segment["pitches"]
        pitches.pop(pitches.index(max(pitches)))
        other_freq = sum(pitches)
        pitch_bass = False
        if other_freq < 1.5:
            pitch_bass = True
        segment_dict["pitch_bass"] = pitch_bass
        if segment["start"] < 0.00001:
            diff = 0
        elif segment_counter < count_segments: 
            diff = segment_times[segment_counter] - segment_times[segment_counter - 1]
            
        else:
            
            break
        
        timbre = segment["timbre"]
        for idx in range(len(timbre)):
            timbre[idx] = round(timbre[idx])
        segment_dict["timbre_bass"] = False
        if timbre[2] < -45:
            segment_dict["timbre_bass"] = True
        segment_dict["start_time"] = round(segment["start"], 2)
        segment_dict["diff"] = diff
        bass_list.append(segment_dict)
        
    
    return bass_list

def play_MMM_ard(bass_list):
    

   

    time_last = 0
    for segment_dict in bass_list:
        time_start = time.time()
        if segment_dict["timbre_bass"] or segment_dict["pitch_bass"]:
            print("@@@@@@")
            #a.digital_write(PIN,1)
            #a.digital_write(PIN,0)
        else:
            print("      ")
            #a.digital_write(PIN,1)
            #a.digital_write(PIN,0)
        time_end = time_start + segment_dict["diff"]
        while time.time() < time_end:
            continue
        #time.sleep(segment_dict["diff"])
        
        
        
            
#         pitches = segment["pitches"]
#         pitches.pop(pitches.index(max(pitches)))
#         other_freq = sum(pitches)
#         is_bass = " : ()"
#         if other_freq < 1.5:
#             is_bass = "BASSSSSSSS"
                
        
#         time_now = segment["start"]
#         diff = time_now - time_last
        
#         print(segment["start"], is_bass, diff)
#         if is_bass == "BASSSSSSSS":
#             a.digital_write(PIN,1)
#         else:
#             a.digital_write(PIN,0)
#         if diff > 0:
#             time.sleep(diff)
#             time_last = time_now
#             continue
#         time_last = time_now
       
    
def play_MMM(anal):
    

    time_last = 0
    for segment in anal["segments"]:
        
        pitches = segment["pitches"]
        pitches.pop(pitches.index(max(pitches)))
        other_freq = sum(pitches)
        is_bass = " : ()     "
        if other_freq < 1.5:
            is_bass = "BASSSSSSSS"
                
        
        time_now = segment["start"]
        diff = round(time_now - time_last , 3)
        
        print(segment["start"], is_bass, round(diff, 3))
        
        if diff > 0:
            time.sleep(diff)
            time_last = time_now
            continue
        time_last = time_now

        
def play_MMM_timb(anal):
    
    
    time_last = 0
    for segment in anal["segments"]:
        pitches = segment["pitches"]
        pitches.pop(pitches.index(max(pitches)))
        other_freq = sum(pitches)
        is_bass = False
        if other_freq < 1.5:
            is_bass = True
                
        
        timbre = segment["timbre"]
        for idx in range(len(timbre)):
            timbre[idx] = round(timbre[idx])
        bass = "-----------"
        
        if  isbass or timbre[2] < -50:
            bass = "BBBBBBBBBBB"
            a.digital_write(PIN,1)
            a.digital_write(PIN,0)
        else:
            a.digital_write(PIN,1)
            a.digital_write(PIN,0)
        time_now = segment["start"]
        diff = time_now - time_last
        
        print(round(segment["start"], 2), bass, round(diff, 2))
        
        if diff > 0:
            time.sleep(diff)
            time_last = time_now
            continue
        time_last = time_now
            



   
        
    

# -


def init_ard():
    if __name__ == '__main__':
        comPort = "COM3"
        global a
        global PIN
        a = Arduino(serial_port="//./" + comPort)
        # if your arduino was running on a serial port other than '/dev/ttyACM0/'
        # declare: a = Arduino(serial_port='/dev/ttyXXXX')

        time.sleep(3)
        # sleep to ensure ample time for computer to make serial connection 

        PIN = 6
        a.set_pin_mode(PIN,'O')
        # initialize the digital pin as output

        time.sleep(1)
        # allow time to make connection
        a.digital_write(PIN,1)
        time.sleep(1)
        a.digital_write(PIN,0)
        print("Arduino Success")


def get_song():  
    query = input("Please enter song: ")
    print()
    poss_songs = sp.search(query)
    returned = []
    for idx in range(len(poss_songs["tracks"]["items"])):

        song_name = poss_songs["tracks"]["items"][idx]["name"]
        artist_name = poss_songs["tracks"]["items"][idx]["album"]["artists"][0]["name"]


        return_tuple = (song_name, artist_name)

        returned.append(return_tuple)


    for idx in range(len(returned)):
        print( str(idx+1) + ".  " + returned[idx][0] + " by " + returned[idx][1] + "\n")
    song_idx = int(input("Enter song number: ")) - 1
    want_song_id = poss_songs["tracks"]["items"][song_idx]["id"]
    song_info = returned[song_idx][0] + " by " + returned[song_idx][1] + "\n"
    return (want_song_id, song_info)

# +
wanted_song = get_devices()

if wanted_song == True:
    #init_ard()
#     wanted_playlist = input("Please enter playlist or leave blank: ")
#     if wanted_playlist == '':
#         wanted_playlist = "Test songs"
    song_tuple = get_song()
    wanted_song_id = song_tuple[0]
    song_info = song_tuple[1]
    bass_list = get_song_data(wanted_song_id)
    
    play = input("Data loaded. Press y to play, n to cancel: ")
    if play == "y":
        avail_devices = sp.devices()
        if avail_devices["devices"][0]["is_active"] != True:
            sp.transfer_playback(phone_id)
            sp.start_playback(uris = [f"spotify:track:{wanted_song_id}"])
            print("Listening to: " + song_info)
        sp.start_playback(uris = [f"spotify:track:{wanted_song_id}"])
        print("Listening to: " + song_info)
        
        play_MMM_ard(bass_list)
    else:
        print("Cancelled!")


# -


