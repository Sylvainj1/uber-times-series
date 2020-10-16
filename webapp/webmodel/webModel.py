import pandas as pd
import numpy as np
import json
import pickle


class WebModel:
    def __init__(self, model):
        self.model = model
    
    def load_model(self):
        loaded_model = pickle.load(open(f'../models/{self.model}.pkl','rb'))
        return loaded_model

    def forecast_pickups(self):
        features = pd.read_csv('../X_test_csv.csv')
        model = self.load_model()
        predictions = model.predict(features)
        return predictions

    def create_pickups_cluster(self,prediction_number=0):
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

    def create_json(self):
        predictions = self.forecast_pickups()
        cluster_value = int(predictions[0])
        json_to_pass = self.create_pickups_cluster(cluster_value)

        return json.dumps(json_to_pass)
    

