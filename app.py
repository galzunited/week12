import base64
from flask import Flask, request, jsonify, render_template
from spotify_client import *
from secret import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
      'index.html'
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
      spotify = SpotifyAPI(client_id, client_secret)
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