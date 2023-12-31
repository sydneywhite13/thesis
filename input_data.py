'''
program to record input data (top 10 songs in each genre by individual artists)
and add the songs to appropriate experimental user's queue in order to feed their recommendation algorithm
'''


''' TO DO:
- feed input! 
- put in calendars
'''

import spotipy
import spotipy.util as util
from datetime import date
from spotipy.oauth2 import SpotifyClientCredentials

USERNAME = 'sydw13'
EXP_USERS = ['alt_user_w_1', 'alt_user_w_2', 'alt_user_w_3', 'alt_user_m_1', 'alt_user_m_2', 'alt_user_m_3',
             'country_user_w_1', 'country_user_w_2', 'country_user_w_3', 'country_user_m_1', 'country_user_m_2', 'country_user_m_3',
             'dance_user_w_1', 'dance_user_2_w', 'dance_user_3_w', 'dance_user_m_1', 'dance_user_m_2', 'dance_user_m_3']
EXP_USERS_2 = ['hip_user_w_1', 'hip_user_w_2', 'hip_user_w_3', 'hip_user_m_1', 'hip_user_m_2', 'hip_user_m_3',
             'pop_user_w_1', 'pop_user_w_2', 'pop_user_w_3', 'pop_user_m_1', 'pop_user_m_2', 'pop_user_m_3',
             'rock_user_w_1', 'rock_user_w_2', 'rock_user_w_3', 'rock_user_m_1', 'rock_user_m_2', 'rock_user_m_3']
GENRES = ['alt', 'country', 'dance', 'hip', 'pop', 'rock']

def access(username):
    # setting user and scope of access
    scope = 'streaming'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

# separate access method for modifying public playlists (as opposed to readint them)
def access_playlist(username):
    # setting user and scope of access
    scope = 'playlist-modify-public playlist-modify-private'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

# TODO: make another access with another app for half of the experimental users (since there is a 25 user limit)

#e45a193003f745298175e924b6ba45f2
def access2(username):
    scope = 'playlist-modify-public playlist-modify-private playlist-read-private user-library-modify'
    token = util.prompt_for_user_token(username, scope, client_id= 'e45a193003f745298175e924b6ba45f2', client_secret= '793b35f55e3a4b02abfb61499b14aeed', redirect_uri = 'thesis://callback')
    return token

# part one: record input data (Spotify URIs) from the six playlists (my account)
def get_uris():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e45a193003f745298175e924b6ba45f2",
                                                               client_secret="793b35f55e3a4b02abfb61499b14aeed"))

    ids = ['spotify:playlist:2ajnJnTJcJn9nm5mBBiebY', 'spotify:playlist:3v41x6tCu7oozI0IuueUq8', 'spotify:playlist:7gDppZo1zLU1lUqlh94Tib',
           'spotify:playlist:6EEDSSXgnc52ywL3Z4K4RQ', 'spotify:playlist:0V6z0mD0MZNwjmvofOGV02', 'spotify:playlist:4tGiqqaPr2C4ClytYyUshu']

    uris = []
    for j in range(len(ids)):
        response = sp.playlist_items(ids[j], additional_types=['track'])
        filename = f'{GENRES[j]}_input_{date.today()}.csv'
        f = open(filename, 'w')
        f.write('number,title,artist,danceability,energy,key,loudness,mode,speechiness,acoustiness,'
            'instrumentalness,liveness,valence,tempo,duration_ms,time_signature,pronoun \n')
        # for every track, write the attributes to a file
        # write the track uri to an array
        uris.append([])

        for i in range(0, len(response['items'])):
            f.write(
                f'{i + 1}, {response["items"][i]["track"]["name"]}, {response["items"][i]["track"]["artists"][0]["name"]} , ')
            # save the track id to an array
            uris[j].append(response['items'][i]['track']['uri'])
            features = sp.audio_features([response['items'][i]['track']['id']])
            f.write(
                f'{features[0]["danceability"]}, {features[0]["energy"]}, {features[0]["key"]}, {features[0]["loudness"]},{features[0]["mode"]}, '
                f'{features[0]["speechiness"]}, {features[0]["acousticness"]}, {features[0]["instrumentalness"]}, {features[0]["liveness"]}, '
                f'{features[0]["valence"]}, {features[0]["tempo"]}, {features[0]["duration_ms"]}, {features[0]["time_signature"]}, ')
        f.close()
    return uris

# part two: add appropriate list of URIs to appropriate experimental user groups
# (different script for scrapping their discover weekly after the fact)
def add_to_queues(uris):
    # for each genre (of which there are 6)
    for i in range(len(GENRES)):
        # for the next six users, add to queue
        for j in range(len(GENRES)):
            user = EXP_USERS[(i*6) + j]
            token = access(user)
            if token:
                sp = spotipy.Spotify(auth=token)
                for k in range(10):
                    sp.add_to_queue(uris[i][k])

# instead of adding to queue, create a playlist for each user and add the URIs to it
# then also try to add the songs to their liked songs
def user_playlists(uris):
    # for each genre (of which there are 6)
    for i in range(len(GENRES)):
        # for the next 6 users, create the playlist and add the songs
        for j in range(len(GENRES)):
            u = EXP_USERS[(i*6) + j]
            token = access_playlist(u)
            if token:
                sp = spotipy.Spotify(auth=token)
                created_playlist = sp.user_playlist_create(user=u, name=f'{GENRES[i]} of {date.today()}', public=True,
                                                           collaborative=False,
                                                           description=f'all of my favorite {GENRES[i]} songs this week')
                pl_id = created_playlist["id"]
                sp.playlist_add_items(pl_id, uris[i], position=None)

GENRES = ['alt', 'country', 'dance', 'hip', 'pop', 'rock']

# method to like the playlist created by me for each of the 6 users of each genre (if we cannot make them on free accounts)
def like_playlists():
    ids = ['2ajnJnTJcJn9nm5mBBiebY', '3v41x6tCu7oozI0IuueUq8',
           '7gDppZo1zLU1lUqlh94Tib',
           '6EEDSSXgnc52ywL3Z4K4RQ', '0V6z0mD0MZNwjmvofOGV02',
           '4tGiqqaPr2C4ClytYyUshu']
    for i in range(len(GENRES)):
        for j in range(6):
            u = EXP_USERS[(i * 6) + j]
            token = access_playlist(u)
            if token:
                sp = spotipy.Spotify(auth=token)
                sp.current_user_follow_playlist(ids[i])
                print(f'{u}')

# function not to create a playlist but to add the songs to them
def add_to_playlist(uris):
    username = '31b5e5p6b4xzqmv2btuzfekiqdfq'
    #https://open.spotify.com/playlist/4GJTDpmIjmfmZedB8ox3kO?si=e35be8429b2c4dc8
    plid = '4GJTDpmIjmfmZedB8ox3kO'
    token = access_playlist(username)
    if token:
    #sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e45a193003f745298175e924b6ba45f2",
    #                                                           client_secret="793b35f55e3a4b02abfb61499b14aeed"))
        sp = spotipy.Spotify(auth=token)
        print('authorized')
        #print(uris[1])
        sp.playlist_add_items(plid, uris[1])

def main():
    #uris = get_uris()
    #print(uris)
    uris = [['spotify:track:1odExI7RdWc4BT515LTAwj', 'spotify:track:1pJk9Ai1GNT0HPWdRpgbBx', 'spotify:track:28cm9uWSKVAfZ0HDBlq4rS', 'spotify:track:4Akq61SpQYUE8IuE7hHNH8', 'spotify:track:2SXx7Ofa79CeJfio98aJcG', 'spotify:track:2Iv1yhxAH7m9SpohnJMs9B', 'spotify:track:3IX0yuEVvDbnqUwMBB3ouC', 'spotify:track:1g8becOwXRFEkYukY94L99', 'spotify:track:1rju0XLSgmtqpjrrCJxsp4', 'spotify:track:4pchG0mOBAJoXXu1vmwyTY'], ['spotify:track:65M92JpTbAdHmTQm4jGaDa', 'spotify:track:0eBFgRxyVSeuT4iyrbukdn', 'spotify:track:6UoKX6uLJwhsnyTp5k5StP', 'spotify:track:7qaMlLPdwNiiU1Uiy1oAdO', 'spotify:track:6d3QUBsiAw3aZI6F2mMhzk', 'spotify:track:41cv1emXVm5Su4DWvltXa6', 'spotify:track:4bARASJEokNacSYtEhoNBp', 'spotify:track:2ePiBvKtQOCBHq9uOlwiiU', 'spotify:track:2z5t8IRRtt5vwkSzP9umJo', 'spotify:track:3vKAQFXRh0lkJdPuS5pclq'], ['spotify:track:787Y2idwCU2Rk60Prv4wpr', 'spotify:track:0rK3a7tLRVgJBoc2DP3tIX', 'spotify:track:4heve4ydl1u6V3AD4moZq9', 'spotify:track:74HBdKMibHlpW312HTFReN', 'spotify:track:4tPHsS7lFxBCe6zRAOWMSR', 'spotify:track:31nfdEooLEq7dn3UMcIeB5', 'spotify:track:3oOvEw1pgxMtrQMNgPWQHL', 'spotify:track:5CaUUACiQFEf4zR5WoeIrp', 'spotify:track:5mjYQaktjmjcMKcUIcqz4s', 'spotify:track:79Ojf7CxxJw04NP4d8hrf8'], ['spotify:track:4xhsWYTOGcal8zt0J161CU', 'spotify:track:6iiCzEd1ULpq7nXbZVQ4pi', 'spotify:track:1nQaTUDJ7Rc4yOvZmg9Ozr', 'spotify:track:1a73gcEg6h6Re6hHXoVltJ', 'spotify:track:5Se32hEA9raeboZerywxka', 'spotify:track:6uTPdRrEDeH8Fyg5L5qmeU', 'spotify:track:73f5rpLgydSRIvHzRLcJFF', 'spotify:track:2IGMVunIBsBLtEQyoI1Mu7', 'spotify:track:3Kh8X9lHztqVBTgw30HbXn', 'spotify:track:351CSUM0YDA0GCbHCSKoL1'], ['spotify:track:1BxfuPKGuaTgP7aM0Bbdwr', 'spotify:track:4xhsWYTOGcal8zt0J161CU', 'spotify:track:2IGMVunIBsBLtEQyoI1Mu7', 'spotify:track:3rUGC1vUpkDG9CZFHMur1t', 'spotify:track:4iZ4pt7kvcaH6Yo8UoZ4s2', 'spotify:track:5mjYQaktjmjcMKcUIcqz4s', 'spotify:track:2KslE17cAJNHTsI2MI0jb2', 'spotify:track:4MjDJD8cW7iVeWInc2Bdyj', 'spotify:track:0mflMxspEfB0VbI1kyLiAv', 'spotify:track:17phhZDn6oGtzMe56NuWvj'], ['spotify:track:4Akq61SpQYUE8IuE7hHNH8', 'spotify:track:1pJk9Ai1GNT0HPWdRpgbBx', 'spotify:track:1BO9znQb8BbJ5W8KPAqgWE', 'spotify:track:0Ef2EJ0YndF0GZMQHsrOvt', 'spotify:track:5sp71CUt0jXRNqHblPGp7b', 'spotify:track:1g8becOwXRFEkYukY94L99', 'spotify:track:3p84R45PM75ngq8XRoe45o', 'spotify:track:1ja4311zfLHqUL96poSXfP', 'spotify:track:7Az7rVogNu6XpLnykVI5fA', 'spotify:track:6vWu5uWlox5TVDPl3LvoG3']]
    #add_to_queues(uris)
    #user_playlists(uris)
    #like_playlists()
    add_to_playlist(uris)
    print('done')

main()