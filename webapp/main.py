import numpy as np
import pickle
from flask import Flask, request, render_template
import json


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']


pickup_json = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
    "features": [
    { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": None, "tsunami": 1 }, "geometry": { "type": "Point", "coordinates": [ -73.968565, 40.779897, 0.0 ] } },
    { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": None, "tsunami": 1 }, "geometry": { "type": "Point", "coordinates": [ -73.968565, 40.779897, 0.0 ] } },
    { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": None, "tsunami": 1 }, "geometry": { "type": "Point", "coordinates": [ -73.865429, 40.837049, 0.0 ] } },
    { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": None, "tsunami": 1 }, "geometry": { "type": "Point", "coordinates": [ -73.865429, 40.837049, 0.0 ] } },
    ]}

@app.route('/')
def mapbox_js():
    return render_template(
        'mapbox_js.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        pickup_data=json.dumps(pickup_json)
    )

if __name__ == '__main__':
    app.run()