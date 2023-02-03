import time

import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import apikey

def main():
    ccm = SpotifyClientCredentials(client_id = apikey.my_id, client_secret = apikey.my_secret)
    scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
    token = spotipy.util.prompt_for_user_token(apikey.username, scope, apikey.my_id, apikey.my_secret, apikey.redirect_uri)

    spotify = spotipy.Spotify(client_credentials_manager = ccm, auth=token)

    anisong_playlists = ['https://open.spotify.com/playlist/1ANQ4WkjGggwVpILHZwWbV', 'https://open.spotify.com/playlist/3c9VYc2FoCQnOcchRuiUV6',
    'https://open.spotify.com/playlist/3PPXWtqZWEEJXNcz8Xtyop']

    set_tempo = 175
    set_tempo_range = 5

    all_feature_df = pd.DataFrame()
    for anisong_playlist in anisong_playlists:
        tmp_feature_df = fetch_track_feature(spotify, anisong_playlist)
        all_feature_df = pd.concat([all_feature_df, tmp_feature_df])

        # trackURLから重複削除
        all_feature_df.drop_duplicates(subset=['track_url'], inplace=True)

        all_feature_df.to_csv('01_result.csv')


def fetch_track_feature(spotify, original_play_list):
    list_data = spotify.playlist_tracks(original_play_list)
    track_num = list_data['total']

    all_feature_df = pd.DataFrame()

    for offset in np.arange(0, track_num, 100):
        print(offset, track_num)
        list_data = spotify.playlist_tracks(original_play_list, offset=offset)
        tmp_feature_df = featch_withoffset(spotify, list_data)
        all_feature_df = pd.concat([all_feature_df, tmp_feature_df])


    return all_feature_df


def featch_withoffset(spotify, list_data):
    urls_list =[]
    anisong_names = []
    for item in list_data['items']:
        track_url = item['track']['external_urls']['spotify']
        track_name = item['track']['name']

        urls_list.append(track_url)
        anisong_names.append(track_name)

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
    feature_df['track_url'] = urls_list

    return feature_df


if __name__=="__main__":
    main()