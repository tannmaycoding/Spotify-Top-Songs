"""
This is a command line app which can tell top songs of a given artist on Spotify.
"""

import json
import spotipy
import requests
import base64

clientId = "Your-ClientID"
clientSecret = "Your-Client-Secret"


def getToken():
    authStr = f"{clientId}:{clientSecret}"
    authBytes = authStr.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {authBase64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    jsonResult = json.loads(result.content)
    token = jsonResult["access_token"]
    return token


def getAuthHeader(token):
    return {"Authorization": f"Bearer {token}"}


def searchArtist(token, artistName):
    url = "https://api.spotify.com/v1/search"
    headers = getAuthHeader(token)
    query = f"?q={artistName}&type=artist&limit=1"
    queryUrl = f"{url}{query}"
    result = requests.get(queryUrl, headers=headers)
    jsonResult = json.loads(result.content)["artists"]["items"]
    if len(jsonResult) == 0:
        print("No Artist With This Name")
        return None

    return jsonResult[0]


def getSongs(token, artistId):
    url = f"https://api.spotify.com/v1/artists/{artistId}/top-tracks?country=US"
    headers = getAuthHeader(token)
    result = requests.get(url, headers=headers)
    jsonResult = json.loads(result.content)["tracks"]
    return jsonResult


while True:
    artistName = input("Enter Artist Name Or /quit to quit: ")
    if artistName == "/quit":
        break
    else:
        token = getToken()
        result = searchArtist(token, artistName)
        artistId = result["id"]
        songs = getSongs(token, artistId)
        print("Top Songs:")
        for i, song in enumerate(songs):
            print(f"{i + 1}. {song['name']}")
