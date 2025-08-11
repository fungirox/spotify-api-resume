from dotenv import load_dotenv
import os 
from datetime import datetime
import base64
import requests
from requests import post,get
import json
from flask import Flask,redirect,request,jsonify,session,render_template
# this is for encode URL params like, hace la cadena de eso con un diccionario "value=1&string=hola"
import urllib.parse

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_URL = 'https://api.spotify.com/v1/'

# long_term medium_term short_term
# TIME_RANGE = 'short_term'
ITEMS_LIMIT = '3'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # here can we add different scopes for read more private/public info (o゜▽゜)o☆
    scope = 'user-read-private user-read-email user-top-read user-follow-read'
    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/spotify-cv')


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/spotify-cv')


@app.route('/spotify-cv', methods=['GET','POST'])
def get_spotify_data():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    if request.method == 'POST':
        TIME_RANGE = request.form.get("time-range")
    else:
        TIME_RANGE = 'short_term'

    try:
        
        playlists = get_playlists(headers)
        user_info = get_user_info(headers)
        artists = get_top_artists(headers, TIME_RANGE)
        tracks = get_top_tracks(headers, TIME_RANGE)

        data = {
            'user' : user_info,
            'playlists' : playlists,
            'artists' : artists,
            'tracks' : tracks,
            'range' : TIME_RANGE
        }
        return render_template('cv.html', data=data)
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        return None, "Token invalido o expirado"
    except Exception as e:
        print(f"Error general {e}")
        return None, "Error obteniendo datos de Spotify"

def get_playlists(headers):
    playlist_items = {}
    try:
        response = requests.get(API_URL + f'me/playlists?limit={ITEMS_LIMIT}', headers=headers)
        response.raise_for_status()  
        playlist_items = get_playlist_items(response.json().get('items', []))
    except Exception as e:
        print(f"Error obteniendo playlist: {e}")
    return playlist_items

def get_playlist_items(playlists):
    # este recibe una lista y envia una lista con un diccionario dentro
    if playlists:
        playlist_new = []
        for playlist in playlists:
            
            image = None
            if playlist.get('images') and len(playlist['images']) > 0:
                image = playlist['images'][0].get('url')
            
            tracks = 0
            if playlist.get('tracks') and len(playlist['tracks']) > 0:
                tracks = playlist['tracks'].get('total')
                
            item = {
                'name' : playlist.get('name','Sin nombre'),
                'image' : image or 'image_default.jpg',
                'tracks' : tracks
            }
            playlist_new.append(item)
        return playlist_new
    else: 
        return {}

def get_user_info(headers):
    user_info = {}
    try:
        response = requests.get(API_URL + 'me', headers=headers)
        response.raise_for_status()  
        user_info = get_user_item(response.json())
        following = get_user_following(headers)
        user_info.update({"following" : following})
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
    return user_info

def get_user_item(user):
    # este recibe un diccionario y regresa otro diccionario
    if user:
        image = None
        if 'images' in user and len(user['images']) > 0:
            image = user['images'][0].get('url')
        if 'followers' in user and user['followers']:
            followers = user['followers'].get('total',0)
        user_new = {
            'username': user['display_name'],
            'image': image or 'image_default_user.jpg',
            'followers': followers
        }
        return user_new
    else:
        return {}
    
def get_user_following(headers):
    following = 0
    try:
        response = requests.get(API_URL + 'me/following?type=artist', headers=headers)
        response.raise_for_status()  
        following = get_user_following_total(response.json())
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
    return following

def get_user_following_total(response):
    # este recibe un diccionario y regresa un numero
    if response:
        return response['artists']['total']
    else:
        return 0
    
def get_top_artists(headers, TIME_RANGE):
    top_artists = {}
    try:
        response = requests.get(API_URL + f"me/top/artists?time_range={TIME_RANGE}&limit={ITEMS_LIMIT}", headers=headers)
        response.raise_for_status()
        top_artists = get_artists_items(response.json().get('items', []))
    except Exception as e:
        print(f"Error obteniendo artistas: {e}")
    return top_artists

def get_artists_items(artists):
    # este recibe una lista y envia una lista con un diccionario dentro
    if artists:
        artist_new = []
        for artist in artists:
            image = None
            if artist.get('images') and len(artist['images']) > 0:
                image = artist['images'][0].get('url')
            item = {
                'name' : artist.get('name','Sin nombre'),
                'image' : image or 'image_default.jpg'
            }
            artist_new.append(item)
        return artist_new
    else: 
        return {}
    
def get_top_tracks(headers, TIME_RANGE):
    top_tracks = {}
    try:
        print(TIME_RANGE)
        response = requests.get(API_URL + f"me/top/tracks?time_range={TIME_RANGE}&limit={ITEMS_LIMIT}", headers=headers)
        response.raise_for_status()
        top_tracks = get_tracks_items(response.json().get('items', []))
    except Exception as e:
        print(f"Error obteniendo top tracks: {e}")
    return top_tracks

def get_tracks_items(tracks):
    # este recibe una lista y envia una lista con un diccionario dentro
    if tracks:
        track_new = []
        for track in tracks:
            image = None
            if 'album' in track:
                # es un objecto dentro de otro y asi, falta hacer esto 
                if 'images' in track['album']:
                    image = track['album']['images'][0].get('url')
                
            item = {
                'name' : track.get('name','Sin nombre'),
                'image' : image or 'image_default.jpg'
            }
            track_new.append(item)
        return track_new
    else: 
        return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


# canvas dimension : 1080 * 1920 
# i need to use Java script for the canvas design and generate
# ideas: u can select the period like: short-tem medium-term long-term
# also: u can add a little description about u or music
# i dont know