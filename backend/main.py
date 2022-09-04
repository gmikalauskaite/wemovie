from imdb import Cinemagoer
from imdb.helpers import resizeImage
from flask import Flask, request
from flask_cors import CORS
from tmdbv3api import TMDb, Movie

tmdb = TMDb()
tmdb.api_key="PASTE YOUR KEY HERE"

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

movies = {}
mv = Movie()

@app.route("/room", methods=["POST"])
def create_room():
    js = request.json
    name = js["name"]

    movies[name] = {}

    return movies[name]

@app.route("/search", methods=["GET"])
def find_movies():
    args = request.args
    name = args["title"]

    results = mv.search(name)
    i = 0
    end_results = []
    for result in results:
        if i == 5:
            break
        if "release_date" not in result:
            continue
        if result["vote_average"] == 0:
            continue
        end_results.append({
            "title": result["title"],
            "cover": "https://image.tmdb.org/t/p/original/" + result["poster_path"],
            "release": result["release_date"][:4],
            "description": result["overview"],
            "rating": result["vote_average"]
        })
        i += 1

    return end_results

@app.route("/movies", methods=["GET"])
def fetch_movies():
    args = request.args
    room_name = args["room_name"]

    return movies[room_name]

@app.route("/movies", methods=["DELETE"])
def delete_movie():
    args = request.args
    room_name = args["room_name"]
    title = args["title"]

    del movies[room_name][title]

    return movies[room_name]

@app.route("/movies", methods=["POST"])
def add_movie():
    args = request.args
    room_name = args["room_name"]

    movie_from_client = request.json
    title = movie_from_client["title"]
    cover = movie_from_client["cover"]
    rating = movie_from_client["rating"]
    release = movie_from_client["release"]
    desc = movie_from_client["description"]

    movies[room_name][title] = {
            "cover": cover,
            "rating": rating,
            "release": release,
            "description": desc,
            "votes": 0
    }

    return movies[room_name]

@app.route("/vote", methods=["POST"])
def vote():
    args = request.args
    movie_title = args["title"]
    room_name = args["room_name"]
    movies[room_name][movie_title]["votes"] += 1

    return movies[room_name]

