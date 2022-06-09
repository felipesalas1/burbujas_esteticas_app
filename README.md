# BURBUJAS ESTÉTICAS Y SISTEMA DE RECOMENDACIÓN DE SPOTIFY COMO CURADOR, PORTERO E INFOMEDIARIO
## Prototipo digital, creador de contra-recomendaciones
# Proyecto de Grado de Felipe Salas-Noguera 
# Universidad de los Andes
## Facultadad de Artes y Humanidades
### Maestría en Humanidades Digitales
### Junio 2022
#### Versión 1.0.0

## Dirección de la aplicación 
http://app.felipesalas.com
## Sobre el proyecto    

Como parte de este proyecto de grado he desarrollado un prototipo que tiene como objetivo generar recomendaciones paralelas dentro de Spotify. Esta aplicación funciona usando la API de Spotify para obtener datos de los usuarios y generarle recomendaciones de canciones paralelas a las que da el SR. Este algoritmo de recomendación funciona de la siguiente forma: en primer lugar, selecciona un artista de forma aleatoria de los 20 artistas favoritos del usuario. En segundo lugar, se toman 20 artistas relacionados a este primer artista. Por último, se agregan 4 canciones del top de canciones de los artistas seleccionados. En caso de que el usuario no tenga ningún artista en su top de artistas se hace una búsqueda con una letra aleatoria y se selecciona un artista al azar de esa búsqueda. Este último paso tiene un sesgo, los artistas que recomienda hacen parte de los artistas más populares de la plataforma. Así mismo, este algoritmo puede llegar a funcionar mejor en los usuarios especialistas que en los generalistas. En los primeros usuarios es más probable que les llegue a gustar los artistas relacionados con los artistas que más escuchan, mientras que en los generalistas es probable que algunos artistas que escuchan estén relacionados con otros artistas que no hagan parte de la burbuja estética del usuario.  

Puede encontrar más información en el /proyecto_de_grado.pdf

## Desarrolado en 

- Python - Django 
- Javascript - React
- Django Restframework

## Para Comenzar 

Este proyecto se desarrollo en un solo projecto de Django con dos aplicaciones, una con el backend en python con Django restframework, y otra con ReactJS compliado por Webpack y Babel.

Para correr este proyecto es necesario instalar Django, node y react. 

Es necesario correr el siguiente código para instalar los paquetes necesarios para correr el proyecto 

''''sh
pip install -r /path/to/requirements.txt
'''

Tener en cuenta cambiar las credenciales en credentials.py para que funcione bien la autenticación de Spotifys

## Licencia 

Este proyecto está cubierto por las licencias MIT para el código y licencia Creative Commons Attribution-ShareAlike 4.0 International para la documentación y el texto.

Para más información leer LICENCE.md

## Contacto 

Felipe Salas-Noguera
Email: lf.salas10(at)uniandes.edu.co
Twitter: @felipelotas
Página web: https://felipesalas.com



