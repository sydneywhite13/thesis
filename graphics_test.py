# program to get the title and artist of a user's 30 recommended Discover Weekly tracks on Spotify
import spotipy
import spotipy.util as util
import requests
import pandas as pd
from bs4 import BeautifulSoup
import tkinter

USERNAME = 'sydw13'

def access():
    # setting user and scope of access
    #username = 'sydw13'
    scope = 'user-library-read'
    # acquiring token to make requests to the API (deprecated method) (source:  https://spotipy.readthedocs.io/en/2.11.1/)
    token = util.prompt_for_user_token(USERNAME, scope, client_id = '79fecdecf6d244c0a34b1066e724abf7', client_secret = '3e97da230f1249869939e4adc8b6fa90', redirect_uri = 'http://localhost:7777/callback')
    return token

def main():
    filename = f"my_disc_weekly_tracks_wgender_{USERNAME}.csv"
    read_summary_stats(filename)

def read_summary_stats(filename):
    # open the file
    df = pd.read_csv(filename, encoding="windows-1252")
    dance = df.danceability.mean()
    energy = df.energy.mean()
    loudness = df.loudness.mean()
    acousticness = df.acoustiness.mean()
    tempo = df.tempo.mean()
    duration = df.duration_ms.mean()
    valence = df.valence.mean()
    #shapes(dance, energy, loudness)
    #colors(duration, valence)
    #pie_chart(df)
    print(dance, energy, loudness, acousticness, tempo, duration, valence)

def shapes(dance, energy, loudness):
    pass

def colors(duration, valence):
    # determie parameters of duration
    # based on how many colors there should be
    # determine colors by valence - can we get q1, mean, and q3
    pass

def pie_chart(df):
    pass

def graphics():
    m = tkinter.Tk()
    '''add widgets
    pack() method organizes widgets in blocks
    grid() organizes in grid
    place() specific positions 
    '''
    canvas_dim = 300
    w = tkinter.Canvas(m, bg='white', width=canvas_dim, height=canvas_dim)
    w.pack()
    l = tkinter.Label(m, text='your music was very...')
    l.pack()
    w.create_oval(10, 10, 23, 23, outline="orange", fill="orange")
    m.mainloop()
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