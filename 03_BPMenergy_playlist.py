import time
import json

import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import apikey

json_file = open('setting.json', 'r')
setting = json.load(json_file)

def main():
    set_tempo = setting['set_tempo']
    set_tempo_range = setting['set_tempo_range']
    result_csvs = setting['track_features']
    playlist_name = f"anisong_BPM{int(set_tempo-set_tempo_range)}-{int(set_tempo+set_tempo_range)}_energy"
    savecsv_name = f"03_result_{int(set_tempo-set_tempo_range)}-{int(set_tempo+set_tempo_range)}.csv"

    ccm = SpotifyClientCredentials(client_id = apikey.my_id, client_secret = apikey.my_secret)
    scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
    token = spotipy.util.prompt_for_user_token(apikey.username, scope, apikey.my_id, apikey.my_secret, apikey.redirect_uri)

    spotify = spotipy.Spotify(client_credentials_manager = ccm, auth=token)

    all_feature_df = pd.DataFrame()
    for result_csv in result_csvs:
        tmp_feature_df = pd.read_csv(result_csv)
        all_feature_df = pd.concat([all_feature_df, tmp_feature_df])

    # trackURLから重複削除
    # all_feature_df.drop_duplicates(subset=['track_url'], inplace=True)
    all_feature_df.drop_duplicates(subset=['name'], inplace=True)

    # BPMで絞り込みプレイリスト作成
    desired_tempo_df = all_feature_df[abs(all_feature_df['tempo']-set_tempo)<=set_tempo_range]
    print(f'{len(desired_tempo_df)}/{len(all_feature_df)} songs')

    # energyでも絞る
    desired_energy_df = desired_tempo_df.sort_values(by='energy', ascending=False)[:103]
    creat_playlist(spotify, playlist_name, list(desired_energy_df['track_url'].values))

    desired_energy_df.to_csv(savecsv_name)


def creat_playlist(spotify, playlist_name, urls):
    playlist = spotify.user_playlist_create(apikey.username, name = playlist_name)
    playlist_url = playlist['external_urls']['spotify']

    for offset in np.arange(0, len(urls), 100):
        spotify.user_playlist_add_tracks(apikey.username, playlist_url, urls[offset:offset+100])


if __name__=="__main__":
    main()