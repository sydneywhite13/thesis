'''
program to add selected songs to a user's queue every week as part of the experiment
this will allow me to change only the Spotify URIs of the songs for every type of user and otherwise
only username for consistency and to avoid mistakes

NOTE: this requires the user to have a Spotify premium account

this will be at mots $11 a month for three months for 30 users (11*3 = 33 * 30 = 990)
this will be at least $17 a month for three months for families of 6 (30/6 = 5) 17*3*5 = 255
'''

import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup




USERNAME = 'sydw13'

def access():
    # setting user and scope of access
    #username = 'sydw13'
    scope = 'streaming'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(USERNAME, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

def main():
    token = access()
    song_uri = ['spotify:track:6me7F0aaZjwDo6RJ5MrfBD', 'spotify:track:4oEf84vBYVftf6KmZexhVo', 'spotify:track:5SDIFVKRHCDEuJGD3TSRwV', 'spotify:track:7LlmSAqvcpjheDytACHfDu', 'spotify:track:3xtiXNDbSKxy20I7D6vFUg']
    # if we get a token
    if token:
        # use the token to make a request for the Discover Weekly playlist using its ID
        # note: to get the ID, go into Spotify, click Share- CRTL - Copy Playlist URI
        sp = spotipy.Spotify(auth=token)
        for i in range(len(song_uri)):
            sp.add_to_queue(song_uri[i])
main()