
import spotipy
import requests
from urllib.parse import urlencode
import base64
import webbrowser
# set up spotify authorization and access
''' will want to use an authorizaton code flow
- the security is not of utmost concern (this is generated data not personal) therefore no need for PKCE extension 
- this is a "long-running application" where we want to only grant access once

the flow
- application requests authorization to Spotify accounts service to user
- user grants acess and app requests access and refresh tokens
- Spotify account services supplies these
- app uses access token in web api request that Spotify web API returns
- this continues as a process of web API requests and JSON object returns
'''

client_id = "79fecdecf6d244c0a34b1066e724abf7"
client_secret = "3e97da230f1249869939e4adc8b6fa90"

# says with this id, we want the authorizaton code using the callback URI to read user library data
auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

# request to Spotify for the authorization code
webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
# code is displayed in the URL after user grants access (this would need to be changed if I didn't control every account)
code = "AQD4AlBHyiNrlMJkze_3Lq1dKyq5RT3pcIF6OU5Hj9zKQJaAPFxzoviW2bcuovEvlvPBfRvAtpIJM85URrQFSqL8kJqDHibw3R1U9VpAUXKdR1UrOuzz_pj3AiKtysuUcpTgOLzuyihX4bfcjmf2pP6-aeTd2ke6GyB-dmaJkZMApnpJZNEmDbnKMY1_9fNqjwWkjdg"

# giving Spotify the client id and client secret in encoded format
encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
# spotify required format
token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}
# we are passing in our authorization code we obtained before so that we can be authorized and make calls
token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:7777/callback"
}
# makes requests to endpoint with our credentials
r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

# the return object
token = r.json()["access_token"]
print(token)
# get the user's discover weekly playlist

# for each track in the playlist

# get all of the information about each song that you can

# save it to an excel sheet