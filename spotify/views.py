from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import get_spotify_user, update_or_create_user_tokens, is_spotify_authenticated, get_spotify_user,search_popular_artist, create_playlist, get_related_artists
from api.models import Room

''''
Devuelve el id para que el usuario se autentique en Spotify
'''
class AuthURL(APIView):
    def get(self, request, fornat=None):
        scopes = 'user-read-recently-played user-read-playback-state user-modify-playback-state user-read-currently-playing user-top-read user-library-modify user-library-read playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative user-read-private user-follow-read user-follow-modify'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


''''
Función para recibir los datos de Spotify y guardar la autenticación en la base de datos
'''
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('http://app.felipesalas.com/')


''''
Comprueba que el usuario esté autenticado y tenga un token de 
'''

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


''''
Obtiene el session key del usuario
'''
class GetSessionid(APIView):
    def get(self, request, format=None):
        session_id = self.request.session.session_key
        auth = False
        if session_id != None:
            auth = True
            return Response({'status': auth}, status=status.HTTP_302_FOUND)
        return Response({'status': auth}, status=status.HTTP_404_NOT_FOUND)

''''
Llama las funciones para crear la recomendación
'''
class createplaylist(APIView):
    def get(self, format=None):
        print('Oli, llegué aquí') 
        getUser = get_spotify_user(self.request.session.session_key)
        artist = search_popular_artist(self.request.session.session_key)
        if artist == None:
            print('este usuarie no tiene música')
            return Response(status = status.HTTP_204_NO_CONTENT)
        idRelated = get_related_artists(self.request.session.session_key,artist)
        create_playlist(self.request.session.session_key, idRelated, getUser, artist)


        return Response(status = status.HTTP_200_OK)