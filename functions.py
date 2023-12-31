# program to get the title and artist of a user's 30 recommended Discover Weekly tracks on Spotify
import spotipy
import spotipy.util as util
import requests
import pandas as pd
from bs4 import BeautifulSoup


USERNAME = 'sydw13'

def access():
    # setting user and scope of access
    #username = 'sydw13'
    scope = 'user-library-read'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(USERNAME, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

def main():
    token = access()
    # if we get a token
    if token:
        # use the token to make a request for the Discover Weekly playlist using its ID
        # note: to get the ID, go into Spotify, click Share- CRTL - Copy Playlist URI
        sp = spotipy.Spotify(auth=token)
        playlist_id = 'spotify:playlist:37i9dQZEVXcCETWli2sFrJ'
        response = sp.playlist_items(playlist_id, additional_types=['track'])
        # open a file to write to
        filename = f"my_disc_weekly_tracks_wgender_{USERNAME}.csv"
        f = open(filename, "w")
        f.write('number,title,artist,danceability,energy,key,loudness,mode,speechiness,acoustiness,'
                'instrumentalness,liveness,valence,tempo,duration_ms,time_signature,pronoun,flag \n')
        base = 'https://open.spotify.com/artist/'
        # for every track, print the title and artist (and write to file)
        for i in range(0, len(response['items'])):
            print(f"{i + 1}. {response['items'][i]['track']['name']} : {response['items'][i]['track']['artists'][0]['name']}")
            f.write(f'{i + 1}, {response["items"][i]["track"]["name"]}, {response["items"][i]["track"]["artists"][0]["name"]} , ')
            # save the track id to an array
            features = sp.audio_features([response['items'][i]['track']['id']])
            f.write(f'{features[0]["danceability"]}, {features[0]["energy"]}, {features[0]["key"]}, {features[0]["loudness"]},{features[0]["mode"]}, '
                    f'{features[0]["speechiness"]}, {features[0]["acousticness"]}, {features[0]["instrumentalness"]}, {features[0]["liveness"]}, '
                    f'{features[0]["valence"]}, {features[0]["tempo"]}, {features[0]["duration_ms"]}, {features[0]["time_signature"]}, ')
            #artist_ids.append(response['items'][i]['track']['artists'][0]['id'])
            url = base + response['items'][i]['track']['artists'][0]['id']
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            bio = soup.find_all("span", class_="Type__TypeElement-sc-goli3j-0 gLgnHU G_f5DJd2sgHWeto5cwbi")
            instagram = soup.find_all("a", class_="njTqo2LYbrg0pH171b_U")
            pronouns, flag = get_pronouns(bio)
            insta_link = get_pronoun_social(instagram)
            # write the insta_link to the file as well (for pronoun checking)
            # and then write the other socials as well
            if flag:
                flag = 1
            else:
                flag = 0
            f.write(f'{pronouns}, {flag} \n')
        f.close()
        read_summary_stats(filename)
    else:
        print('cannot get token')

def get_pronoun_social(socials):
    links = []
    instagram = ''
    for j in range(0, len(socials)):
        link = socials[j]['href']
        links.append(link)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        if 'instagram' in link:
            instagram = link
            #trying to find a way to scrape pronouns from instagram (since on profile and user selected) but cannot find it in the html
            #print(link)
            page = requests.get(instagram)
            soup = BeautifulSoup(page.content, "html.parser")
            pro = soup.find_all("div", class_='x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do')
    return instagram


def get_pronouns(bios):
    # now, for every bios
    # bios is a double nested array
    she_her = 0
    he_him = 0
    they_them = 0
    pronoun = ''
    flag = False
    for j in range(0, len(bios)):
        # clean the data (get rid of html speak)
        bio = bios[j].text
        # for every word in the string
        words = bio.split(' ')
        for word in words:
            if word == 'she' or word == 'her' or word == 'hers' or word == 'herself':
                she_her += 1
            # if he, him, his
            if word == 'he' or word == 'him' or word == 'his' or word == 'himself':
                he_him += 1
            # if the word is they, them, theirs
            if word == 'they' or word == 'their' or word == 'theirs' or word == 'them' or word == 'themselves':
                they_them += 1
    # if she_her > 0 and he_him = 0 and they_them = 0, conclude W
    if she_her > 0 and he_him == 0 and they_them == 0:
        pronoun = 'W'
    # if he_him > 0, and she_her = 0 and they_them = 0, conclude M
    elif he_him > 0 and she_her == 0 and they_them == 0:
        pronoun = 'H'
    # the rest will get complicated, and you should set flags to be chekced by a human
    elif they_them > 0 and she_her == 0 and he_him == 0:
        pronoun = 'T'
    elif she_her == he_him == they_them == 0:
        pronoun = 'U'
    else:
        flag = True
        if she_her > he_him and she_her > they_them:
            if they_them > 0:
                if he_him == 0:
                    pronoun = 'GW'
                else:
                    pronoun = 'GM'
        elif he_him > she_her and he_him > they_them:
            if they_them > 0:
                if she_her == 0:
                    pronoun = 'GH'
                else:
                    pronoun = 'GM'
        elif they_them > she_her and they_them > he_him:
            if she_her == 0:
                pronoun = 'GH'
            elif he_him == 0:
                pronoun = 'GW'
            else:
                pronoun = 'GM'
        elif she_her == 0 and they_them > 0 and he_him > 0:
            pronoun = 'GH'
        elif he_him == 0 and they_them > 0 and she_her > 0:
            pronoun = 'GW'
        elif they_them != 0:
            pronoun = 'GM'
        else:
            pronoun = 'U'
    return pronoun, flag


def read_summary_stats(filename):
    # open the file
    df = pd.read_csv(filename, encoding="windows-1252")
    print(df)
    print(df.columns)
    dance = df.danceability.mean()
    energy = df.energy.mean()
    loudness = df.loudness.mean()
    acousticness = df.acousticness.mean()
    tempo = df.tempo.mean()
    duration = df.duration.mean()
    valence = df.valence.mean()
    shapes(dance, energy, loudness)
    colors(duration, valence)
    pie_chart(df)
    print(df, dance, energy, loudness, acousticness, tempo, duration, valence)

def shapes(dance, energy, loudness):
    pass

def colors(duration, valence):
    pass

def pie_chart(df):
    pass
main()

'''
fun user output stuff:
- danceability : the shape itself 
- energy : shape movement speed 
- loudness : the size of the shapes 
- acousticness : how the things move? 
- instrumentalness : ? 
- tempo : color changing speed 
- duration : how many colors there are in the background 
- valece (hapiness) : colors of background 


something happy should have a happy color 
a fast tempo should make things move faster colors change quickly 
energy could make shapes move faster 
'''