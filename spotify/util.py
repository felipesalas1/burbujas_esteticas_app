''''
Archivo con todos las funciones para crear las contra-recomendaciones
'''

import datetime
from requests.api import request
from requests.models import Request, Response
from rest_framework import status
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get
import random
import json
import string

# url base para las peticiones a Spotify

BASE_URL = "https://api.spotify.com/v1/"


# Toma el token del usuario 
def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    print(user_tokens)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


# Refresca o autentica el usuario de Spotify
def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

# verifica si el usuario ya tiene un token 
def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False

# Refresca el token
def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    print("el expires", expires_in)
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)

# Pide el nombre usuario de Spotify
def get_spotify_user(session_id):
    # print("llega acá al util")
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    response = get(BASE_URL + "me",{}, headers=headers).json()
    username = response.get('id')


    return username

""" 
Da un artista popular para el usuario
Usa un número pseudoaleatorio para escoger entre los 
20 artistas favoritos del usuario
"""


def search_popular_artist(session_id):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    print (BASE_URL + 'me/top/artists')
    responseOk = get(BASE_URL + 'me/top/artists',{}, headers=headers)
    response = responseOk.json()
    #print(response)
    artist = None
    print(responseOk.status_code)

    if responseOk.status_code == 401:
        refresh_spotify_token(session_id)
        responseOk = get(BASE_URL + 'me/top/artists',{}, headers=headers)
        response = responseOk.json()

    if responseOk.status_code == 200:

        total = response.get('total')
        print('El total ', total)
   
    
        if total == 0: #Cuando el usuario no ha usado spotify no hay forma de recomendarle música de forma algoritmica sin poner algún artista
            print('Llegué al IF')
            randomSearchQuery = random.choice(string.ascii_letters)
            print(session_id)
            artistId = randomSearch(session_id, randomSearchQuery)

        if total > 1:
            
            n = random.randint(0,19) # Solamente tomo los 20 items por defecto
            artists = response.get('items')
            artist = artists[n]
            artistId = artist.get('id')
            print(artist)

            print(artist, 'el artists')
            print(artistId, 'el artists ID')

        """ if total < 2 : 
            n = random.randint(0,1)
            artists = response.get('items')
            artist = artists[n]
            artistId = artist.get('id')
            print(artist)

            print(artist, 'el artists')
            print(artistId, 'el artists ID')  """

        
            
            

        

    return artistId

#Toma artistas relacionados al artista escogido en el método search_popular_artist

def get_related_artists(session_id ,artist):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    print(BASE_URL + 'artists/' + artist + '/related-artists')
    
    response = get(BASE_URL + 'artists/' + artist + '/related-artists',{}, headers=headers)

    if response.status_code == 200:

        response = response.json()
    
    else: print(response.status_code)

    #contador para el for y Lista de los artistas relacionados
    count = 0
    idRelated = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for artistNum in response['artists']:
        artistsNames = artistNum['name']
        artistsIds = artistNum['id']
        #Imprime cada artista relacionado que informa Spotify
        print(artistsNames)
        idRelated [count] = artistsIds
        count += 1  

    return idRelated

#Crea playlist en la cuenta del usuario, recibe los ids de los artistas relacionados, el artista base de la recomendación y el usuario

def create_playlist(session_id, idRelated, getUser, artist):
    now = datetime.datetime.now()
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    payload = json.dumps({
    "name": "Contrarecomendación " + now.strftime("%Y-%m-%d %H:%M:%S") + "Burbujas Estéticas",
    "public": False
    })
               

    response = post(BASE_URL + 'users/' + getUser + '/playlists',data=payload, headers=headers )

    response = response.json()

    elNombre = response['name']
    playlistId = response['id']

    #Toma los top tacks de las bandas relacionadas
    #Contadores para el For y los IF
    countb = 0
    counta = 0
    #Lista de los tracks relacionados, crea 90 y los llena con un dato Dummie
    idTracks = ["spotify:track:3ZLElfsFXSMmNCliIGhIb7"] * 90

    for band in idRelated:
      url = "https://api.spotify.com/v1/artists/" + idRelated[countb] + "/top-tracks?country=co"
      

      response = get(url, {} ,headers=headers)

    
      
      if response.status_code == 200:

        responseTracks = response.json()
      
      else: print(response.status_code)

      
     #contador para el for
      countd = 0
      for trackId in responseTracks['tracks']:
        

        #Toma datos del Json
        track_title = trackId['name']
        print(track_title)
        track_id = trackId['id']
        countc = 0
        for trackArt in trackId['artists']:
          
          if countc > 0:
            track_artist = track_artist + " - " + trackArt['name']
          else:
            track_artist = trackArt['name']
          countc += 1
          print(track_artist)
        track_pop = trackId['popularity']
        track_uri = trackId['uri']
        track_rDate = trackId['album']['release_date']


        print(countd)

        #toma solamente tres tracks para añadirlo a la playlist creada los otros datos son solamente para el CSV
        if countd <= 3:
        
          #trackIds = trackId['id']
          idTracks [counta] = trackId['uri']
          countd += 1
          counta += 1
        else: print("Artista número: " + str(countb))
        

      countb += 1 

    print(idTracks)

    #Añade las canciones del artista principal

    url = "https://api.spotify.com/v1/artists/" + artist +  "/top-tracks?country=co"
    payload={}
    

    response = get( url, {},headers=headers)

        
        
    if response.status_code == 200:

        responseTracks = response.json()

    else: print(response.status_code)

        
    #Añade las canciones del artista principal a la lista de tracks  
    for trackId in responseTracks['tracks']:
        #trackIds = trackId['id']
        idTracks [counta] = trackId['uri']
        counta += 1

    #Le hace un random al orden de las canciones dentro de la playlist
    random.shuffle(idTracks)

    print(idTracks)

    #Prepara los URIS para que Spotify lo acepte

    uris = ",".join(idTracks)

    print(uris)

    url = 'https://api.spotify.com/v1/users/' + getUser +'/playlists/' + playlistId + '/tracks?uris=' + uris


    response = post(url, {} ,headers=headers)

    
        
    if response.status_code == 200:

        responseTracks = response.json()
    else: print(response.status_code)

    print("se ha creado la playlist en la cuenta de: " + getUser)

    return status.HTTP_200_OK


""" 
Este método busca un artista con una letra generada al azar
Este método tiene un bias, Spotify devuelve los items con mayor popularidad, falta hacer uno que no busque hasta que la popularidad sea baja
 """

def randomSearch(session_id, letter):
    print(session_id)
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    payload = json.dumps({
    "q": letter,
    "type": 'artist'
    })
               

    
    response = get(BASE_URL + 'search?type=artist&q=' + letter , headers=headers ).json()

    artists = response.get('artists')
    #print(response.json())
    total = artists.get('total')


    n = random.randint(0,19)

    
    artist = artists.get('items')
    elArtist = artist[n]
    artistId = elArtist.get('id')


    return artistId
