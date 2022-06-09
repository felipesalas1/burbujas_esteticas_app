from django.db import models
''''
Modelos en la base de datos
Se guarda en la base de datos el token de autenticación de Spotify
Cuando expira, cuando se creo, los datos de la sesión del usuario 
'''

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)