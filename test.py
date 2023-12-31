'''
program to record input data (top 10 songs in each genre by individual artists)
and add the songs to appropriate experimental user's queue in order to feed their recommendation algorithm
'''


''' TO DO:
- change the file outputs and actual queues to printing to double check
- check on the discover weekly functions
- make new input data
- upgrade all accounts to premium 
- feed input! 
- put in calendars
'''

import spotipy
import spotipy.util as util
from datetime import date

USERNAME = 'sydw13'
EXP_USERS = ['alt_user_w_1', 'alt_user_w_2', 'alt_user_w_3', 'alt_user_m_1', 'alt_user_m_2', 'alt_user_m_3',
             'country_user_w_1', 'country_user_w_2', 'country_user_w_3', 'country_user_m_1', 'country_user_m_2', 'country_user_m_3',
             'dance_user_w_1', 'dance_user_2_w', 'dance_user_3_w', 'dance_user_m_1', 'dance_user_m_2', 'dance_user_m_3',
             'hip_user_w_1', 'hip_user_w_2', 'hip_user_w_3', 'hip_user_m_1', 'hip_user_m_2', 'hip_user_m_3',
             'pop_user_w_1', 'pop_user_w_2', 'pop_user_w_3', 'pop_user_m_1', 'pop_user_m_2', 'pop_user_m_3',
             'rock_user_w_1', 'rock_user_w_2', 'rock_user_w_3', 'rock_user_m_1', 'rock_user_m_2', 'rock_user_m_3']
GENRES = ['alt', 'country', 'dance', 'hip', 'pop', 'rock']

def access(username):
    # setting user and scope of access
    scope = 'streaming'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token


def access_playlist(username):
    # setting user and scope of access
    scope = 'playlist-modify-public'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

# part one: record input data (Spotify URIs) from the six playlists (my account)
def get_uris():
    token = access(USERNAME)
    # if we get a token
    if token:
        # use the token to make a request for the input playlist by using the ID
        sp = spotipy.Spotify(auth=token)

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
                    f'{features[0]["valence"]}, {features[0]["tempo"]}, {features[0]["duration_ms"]}, {features[0]["time_signature"]}, \n')
            f.close()
        return uris

# part two: add appropriate list of URIs to appropriate experimental user groups
# (different script for scrapping their discover weeky after the fact)
def add_to_queues(uris):
    # for each genre (of which there are 6)
    # 6
    for i in range(len(GENRES)):
        # for the next six users, add to queue
        # 6
        for j in range(len(GENRES)):
            # 36
            #user = EXP_USERS[(i*6) + j]
            token = access(USERNAME)
            if token:
                sp = spotipy.Spotify(auth=token)
                for k in range(10):
                    sp.add_to_queue(uris[i][k])

def user_playlists(uris):
    # for each genre (of which there are 6)
    for i in range(len(GENRES)):
        # for the next 6 users, create the playlist and add the songs
        for j in range(len(GENRES)):
            #user = EXP_USERS[(i*6) + j]
            token = access_playlist(USERNAME)
            if token:
                sp = spotipy.Spotify(auth=token)
                #print(f"playlist: {user}'s {GENRES[i]} of {date.today()}")
                created_playlist = sp.user_playlist_create(user=USERNAME, name= f'{GENRES[i]} of {date.today()}', public=True, collaborative=False,
                                                           description=f'all of my favorite {GENRES[i]} songs this week')
                pl_id = created_playlist["id"]
                sp.playlist_add_items(pl_id, uris[i], position=None)
                #print(f'{uris[i]}')

def main():
    uris = get_uris()
    #print(get_uris())
    add_to_queues(uris)
    #add_to_queues(uris)
    #token = access('alt_user_w_1')
    #if token:
    #    print('one worked')
    #user_playlists(uris)

main()