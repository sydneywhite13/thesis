# program to get the title and artist of a user's 30 recommended Discover Weekly tracks on Spotify
import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup

# setting user and scope of access
# my username = sydw13
username = '3lemann'
scope = 'user-library-read'

# acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
token = util.prompt_for_user_token(username, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')

# if we get a token
if token:
    # use the token to make a request for the Discover Weekly playlist using its ID
    # note: to get the ID, go into Spotify, click Share- CRTL - Copy Playlist URI
    sp = spotipy.Spotify(auth=token)
    #spotify:playlist:6TerF51gqg9hnA0deqH2eX

    # my discover weekly: spotify:playlist:37i9dQZEVXcCETWli2sFrJ
    playlist_id = 'spotify:playlist:6TerF51gqg9hnA0deqH2eX'
    response = sp.playlist_items(playlist_id, additional_types=['track'])
    # open a file to write to
    f = open("my_disc_weekly_tracks.csv", "w")
    f.write('number, title, artist, danceability, energy, key, loudness, mode, speechiness, acoustiness, '
            'instrumentalness, liveness, valence, tempo, duration_ms, time_signature \n')
    track_ids = []
    artist_ids = []
    bios = []
    base = 'https://open.spotify.com/artist/'
    # for every track, print the title and artist (and write to file)
    for i in range(1, len(response['items'])):
        print(f"{i}. {response['items'][i]['track']['name']} : {response['items'][i]['track']['artists'][0]['name']}")
        f.write(f'{i}, {response["items"][i]["track"]["name"]}, {response["items"][i]["track"]["artists"][0]["name"]}, ')
        # save the track id to an array
        features = sp.audio_features([response['items'][i]['track']['id']])
        f.write(f'{features[0]["danceability"]}, {features[0]["energy"]}, {features[0]["key"]}, {features[0]["loudness"]},{features[0]["mode"]}, '
                f'{features[0]["speechiness"]}, {features[0]["acousticness"]}, {features[0]["instrumentalness"]}, {features[0]["liveness"]}, '
                f'{features[0]["valence"]}, {features[0]["tempo"]}, {features[0]["duration_ms"]}, {features[0]["time_signature"]}')
        artist_ids.append(response['items'][i]['track']['artists'][0]['id'])
        f.write('\n')
    for j in range(0, len(artist_ids)):
        url = base + artist_ids[j]
        #print(url)
        # use this url to scrape for information and text
        # source: https://realpython.com/beautiful-soup-web-scraper-python/
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        bios.append(soup.find_all("span", class_="Type__TypeElement-sc-goli3j-0 gLgnHU G_f5DJd2sgHWeto5cwbi"))
        #if not soup.find_all("span", class_="Type__TypeElement-sc-goli3j-0 gLgnHU G_f5DJd2sgHWeto5cwbi"):
         #   bios.append([])
else:
    print('cannot get token for', username)

# now, for every bios
she_her = 0
he_him = 0
they_them = 0

# bios is a double nested array
for i in range(0, len(bios)):
    she_her = 0
    he_him = 0
    they_them = 0
    flag = False
    for j in range(0, len(bios[i])):
        # clean the data (get rid of html speak)
        bio = bios[i][j].text
        # for every word in the string
        words = bio.split(' ')
        for word in words:
            if word == 'she' or word == 'her' or word == 'hers' or word == 'herself':
                she_her += 1
            # if the he, him, his
            if word == 'he' or word == 'him' or word == 'his' or word == 'himself':
                he_him += 1
            # if the word is they, them, theirs
            if word == 'they' or word == 'their' or word == 'theirs' or word == 'them' or word == 'themselves':
                they_them += 1
    #print(bio)
    print(f'pronouns she : {she_her} he: {he_him} they: {they_them}')
    # if she_her > 0 and he_him = 0 and they_them = 0, conclude W
    if she_her > 0 and he_him == 0 and they_them == 0:
        print('W')
    # if he_him > 0, and she_her = 0 and they_them = 0, conclude M
    elif he_him > 0 and she_her == 0 and they_them == 0:
        print('H')
    # the rest will get complicated, and you should set flags to be chekced by a human
    elif they_them > 0 and she_her == 0 and he_him == 0:
        print('T')
    elif she_her == he_him == they_them == 0:
        print('U')
    else:
        flag = True
        if she_her > he_him and she_her > they_them:
            if they_them > 0:
                if he_him == 0:
                    print('GW')
                else:
                    print('GM')
        elif he_him > she_her and he_him > they_them:
            if they_them > 0:
                if she_her == 0:
                    print('GH')
                else:
                    print('GM')
        elif they_them > she_her and they_them > he_him:
            if she_her == 0:
                print('GH')
            elif he_him == 0:
                print('GW')
            else:
                print('GM')
        elif she_her == 0 and they_them > 0 and he_him > 0:
            print('GH')
        elif he_him == 0 and they_them > 0 and she_her > 0:
            print('GW')
        elif they_them != 0:
            print('GM')
        else:
            print('U')
'''

Next Steps:
- get artist's biographies for pronoun scanning (or do this by hand?)

- preliminary analysis and data cleaning in R 
- experimental design

'''