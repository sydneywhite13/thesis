import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os

'''environment variables
- named value that cna affect behavior of process running on operating system
- accessed by various programs and scripts on the system 
- used to configure applications based on environment 
( often used in API keys, file paths, database connection strings...
- setting API keys and passwords as environment variables is more secure than hard coding them! 
How I Did This
* import os
* use key name pairs 
source: https://www.freecodecamp.org/news/python-env-vars-how-to-get-an-environment-variable-in-python/
'''

os.environ["CLIENT_ID"] = "79fecdecf6d244c0a34b1066e724abf7"
os.environ["CLIENT_SECRET"] = '3e97da230f1249869939e4adc8b6fa90'
username = 'sydw13'
scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')

# source: https://spotipy.readthedocs.io/en/2.11.1/

# old code that didn't work (but definitely should be used instead of my deprecated method)
''' 
scope = 'user-library-read'
auth_manager=SpotifyOAuth(scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist_id = 'spotify:playlist:7ExuuZdawPn7hlC02Az5u5'
results = sp.playlist(playlist_id)
print(json.dumps(results, indent=4))
'''
#print(token)

if token:
    sp = spotipy.Spotify(auth=token)
    playlist_id = 'spotify:playlist:7ExuuZdawPn7hlC02Az5u5'
    results = sp.playlist(playlist_id)
    #print(json.dumps(results, indent = 4))
    offset = 0
    response = sp.playlist_items(playlist_id, additional_types=['track'])
    #print(response['items'])
    for item in response['items']:
        print(item['track']['name'] + ' : ' + item['track']['artists'][0]['name'])

    ''' 
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
    # lots of code here
    '''
else:
    print('cannot get token for', username)