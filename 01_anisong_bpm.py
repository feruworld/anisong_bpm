import time

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import apikey

def main():
    ccm = SpotifyClientCredentials(client_id = apikey.my_id, client_secret = apikey.my_secret)
    spotify = spotipy.Spotify(client_credentials_manager = ccm)

    anisong_playlist = 'https://open.spotify.com/playlist/3pt1xO7l9OMpZ7ZWBj5KtT'

    set_tempo = 175
    set_tempo_range = 5
    fetch_track_feature(spotify, anisong_playlist)

def fetch_track_feature(spotify, original_play_list):
    list_data = spotify.playlist_tracks(original_play_list)
    track_num = list_data['total']

    urls_list =[]
    anisong_names = []
    print(track_num, len(list_data['items']))
    for i in range(track_num):
        track_url = list_data['items'][i]['track']['external_urls']['spotify']
        track_name = list_data['items'][i]['track']['name']
        print(track_name)

        urls_list.append(track_url)
        anisong_names.append(track_name)

    print(track_num, len(urls_list))
    time.sleep(1) #1sec stop
    tempo_urls_list =[]

    feature_dict = {}
    feature_keys = spotify.audio_features(urls_list[0])[0].keys()

    for i in range(len(urls_list)):
        track_url = urls_list[i]
        feature = spotify.audio_features(track_url)
        
        for key in feature_keys:
            if key in feature_dict:
                feature_dict[key].append(feature[0][key])
            else:
                feature_dict[key] = [feature[0][key]]
        
        time.sleep(1)

    feature_df = pd.DataFrame(feature_dict)
    feature_df['name'] = anisong_names
    feature_df.to_csv('01_result.csv')



if __name__=="__main__":
    main()