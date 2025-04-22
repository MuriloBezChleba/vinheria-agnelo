from django.shortcuts import render
from django.http import JsonResponse
import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from django.http import HttpResponseRedirect
from collections import Counter


sp_oauth = SpotifyOAuth(
        client_id = settings.SPOTIFY_CLIENT_ID,
        client_secret = settings.SPOTIFY_SECRET_KEY,
        redirect_uri = 'http://127.0.0.1:8000/api/callback',
        scope="playlist-read-private playlist-read-collaborative",
        open_browser=False,  # (opcional, evita abrir navegador automaticamente)
        show_dialog=True,    # (opcional, força login mesmo se já tiver session salva)
        cache_path=".cache", # (opcional, define onde guardar o token)
)

def index(request):
    return JsonResponse({'message': 'API do Spotify funcionando!'})


def auth(request):
    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)


def analisarPlaylist(request):
    code = request.GET.get('code')
    playlist_url = request.GET.get('url')

    if not code or not playlist_url:
        return JsonResponse({'error' : 'É necessario fornecer o "code" ou a url da playlist'}, status = 400)
    match = re.search(r'playlist/([\w-]+)', playlist_url)
    if not match:
        return JsonResponse({'error': 'URL de playlist inválida'}, status=400)
    playlist_id = match.group(1).split('?')[0]  

    try:
        token_info = sp_oauth.get_access_token(code, as_dict=True, check_cache=True)
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)

        playlist_data = sp.playlist(playlist_id)
        generos_counter = Counter()

        for item in playlist_data['tracks']['items']:
            track = item.get('track')
            if not track:
                continue
            for artista in track.get('artists', []):
                artista_id = artista.get('id')
                if artista_id:
                    dados_artista = sp.artist(artista_id)
                    generos = dados_artista.get('genres',[])
                    generos_counter.update(generos)
        
        generos_agrupados = dict(generos_counter)

        if generos_counter:
            genero_top, valor_top = generos_counter.most_common(1)[0]
        else:
            genero_top, valor_top = None, 0

        return JsonResponse({
            'generos': generos_agrupados,
            'mais_comum':{
                'genero' : genero_top,
                'valor': valor_top
            }
        })
            


    except spotipy.exceptions.SpotifyException as e:
        return JsonResponse({'error': e.msg, 'status': e.http_status}, status=e.http_status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  