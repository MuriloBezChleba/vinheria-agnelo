from django.shortcuts import render
from django.http import JsonResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings


def index(request):
    spotifyAuth = SpotifyOAuth(
        client_id = settings.SPOTIFY_CLIENT_ID,
        client_secret = settings.SPOTIFY_SECRET_KEY,
        redirect_uri = 'http://127.0.0.1:8000/api/index'
    )
    sp = spotipy.Spotify(auth_manager = spotifyAuth)
    novosLancamento = sp.new_releases(country="Brazil", limit=5)
    return JsonResponse(novosLancamento)

def auth(request):
    return JsonResponse({'Hello': 'world'})