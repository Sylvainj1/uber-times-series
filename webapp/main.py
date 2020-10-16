import numpy as np
import pickle
from flask import Flask, request, render_template
import json
import pandas as pd


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']


def create_pickups_cluster(prediction_number=0):
    schema = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "pickups_json"}},
        "features": []
    }

    populate_feature = []

    for i in range(0, prediction_number):
        feature = {"type": "Feature", "properties": {"id": "Manhattan", "time": 1507425650893},
                   "geometry": {"type": "Point", "coordinates": [-73.968565, 40.779897, 0.0]}}
        populate_feature.append(feature)

    schema['features'] = populate_feature
    return schema

pickup_json = create_pickups_cluster()

model_test = pickle.load(open('../models/model_lgbm.pkl','rb'))


@app.route('/')
def mapbox_js():
    return render_template(
        'html/index.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        pickup_data=json.dumps(pickup_json)
    )

@app.route('/predict', methods = ['POST'])
def predict():
    #en fait ce qu'il faudra faire, c'est laisser à l'utilisateur choisir l'horizon, ou bien la date
    # genre 1h, 2h etc...
    # recuperer cet input ici 
    #et choper la valeur en conséquence
    # par exemple ici au lieu d'avoir predictions[0] pour 1h apres,
    # #si l'utilisateur veut 2h apres ca sera predictions[1] etc...

    features = pd.read_csv('../X_test_csv.csv')
    predictions = model_test.predict(features)

    cluster_value = int(predictions[0])
    json_to_pass = create_pickups_cluster(cluster_value)

    return render_template(
        'html/index.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        pickup_data=json.dumps(json_to_pass)
    )


if __name__ == '__main__':
    app.run()
