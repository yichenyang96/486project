import google_search
from flask import Flask, make_response, redirect, url_for, jsonify, render_template, request
import json



app = Flask(__name__)
cache = {}
with open('cache.json') as f:
    cache = json.load(f)


@app.route("/recursive")
def search_recur():
    status_code = 200
    query = request.args.get('query')
    info = {}
    if 'recursive' not in cache:
        cache['recursive'] = {}
    if  query in cache['recursive']: 
        info = cache['recursive'][query]
    else:
        info = google_search.recursive_model(query)
        cache['recursive'][query] = info
        with open('cache.json', 'w') as f:
            json.dump(cache, f, indent=4, sort_keys=True, default=str)
    is_left = True
    for data in info['results']:
        data['position'] = 'left' if is_left else 'right'
        is_left = not is_left
        
    return render_template("index.html", **info)
    # return jsonify(info), status_code


@app.route("/timespan")
def search():
    status_code = 200
    query = request.args.get('query')
    info = {}
    if 'timespan' not in cache: 
        cache['timespan'] = {}
    if 'timespan' in cache and query in cache['timespan']:
        info = cache['timespan'][query]
    else:
        info = google_search.google_search(query)
        cache['timespan'][query] = info
        with open('cache.json', 'w') as f:
            json.dump(cache, f, indent=4, sort_keys=True, default=str)
    is_left = True
    for data in info['results']:
        data['position'] = 'left' if is_left else 'right'
        is_left = not is_left
        
    return render_template("index.html", **info)
    # return jsonify(info), status_code

@app.route("/")
def index():
    info = {'results': []}
    return render_template("index.html", **info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
