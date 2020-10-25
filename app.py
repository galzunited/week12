import base64
from flask import Flask, request, jsonify, render_template
from spotify_client import *
from secret import *
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
spotify = SpotifyAPI(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])

@app.route('/')
def index():
    return render_template(
      'index.html'
    )

@app.route('/new_releases')
def new_releases():
    results = spotify.get_new_releases()
    items = results['albums']['items']
    # print('items', items)
    return render_template(
      'new_releases.html',
      items=items
    )

@app.route('/artist/<artist_id>')
def artist_page(artist_id):
    print('id', artist_id)
    artist = spotify.get_artist(artist_id)
    result = spotify.get_top_tracks(artist_id)
    tracks = result['tracks']
    return render_template(
        'artist_page.html',
        artist=artist,
        tracks=tracks
    )

@app.route('/about')
def about():
    return render_template(
        'about.html'
    )

@app.route('/search')
def search():
    try:
      query = request.args['user_query']
      search_type = request.args['search_type']
      print('search type', search_type)
      results = spotify.search(query, search_type = search_type)[search_type + 's']['items']
      print(results)
      return render_template(
          'search.html',
          results=results,
          search_type=search_type
      )
    except Exception as e:
      print('blahh', e)
      return render_template('search.html')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)