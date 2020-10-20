import pandas as pd
import numpy as np
import json
import pickle
from sklearn.preprocessing import MinMaxScaler


class WebModel:
    model_name = 'model_lgbm'
    predictions = []
    pred_brooklyn = []
    pred_bronx = []
    pred_queens = []


    def __init__(self, model_name):
        self.model_name = model_name
        model = pickle.load(open(f'../models/{self.model_name}.pkl','rb'))
        
        self.predictions = self.forecast_pickups(model)
        self.get_static_pred()
    
    def load_model(self):
        loaded_model = pickle.load(open(f'../models/{self.model_name}.pkl','rb'))
        return loaded_model

    def get_static_pred(self):
        if self.model_name == 'model_sarimax':
            self.pred_brooklyn = np.array(pd.read_csv('../models/pred_sarimax_brooklyn.csv')['0'])
            self.pred_bronx = np.array(pd.read_csv('../models/pred_sarimax_bronx.csv')['0'])
            self.pred_queens = np.array(pd.read_csv('../models/pred_sarimax_queens.csv')['0'])

        if self.model_name == 'model_lgbm':
            self.pred_brooklyn = np.array(pd.read_csv('../models/pred_lgbm_brooklyn.csv')['0'])
            self.pred_bronx = np.array(pd.read_csv('../models/pred_lgbm_bronx.csv')['0'])
            self.pred_queens = np.array(pd.read_csv('../models/pred_lgbm_queens.csv')['0'])

        if self.model_name == 'model_naive':
            self.pred_brooklyn = np.array(pd.read_csv('../models/pred_naive_brooklyn.csv')['0'])
            self.pred_bronx = np.array(pd.read_csv('../models/pred_naive_bronx.csv')['0'])
            self.pred_queens = np.array(pd.read_csv('../models/pred_naive_queens.csv')['0'])
        
        if self.model_name == 'model_prophet':
            self.pred_brooklyn = np.array(pd.read_csv('../models/pred_prophet_brooklyn.csv')['yhat'])
            self.pred_bronx = np.array(pd.read_csv('../models/pred_prophet_bronx.csv')['yhat'])
            self.pred_queens = np.array(pd.read_csv('../models/pred_prophet_queens.csv')['yhat'])

        


    def forecast_pickups(self, model):
        if self.model_name == 'model_sarimax':
            uber = pd.read_csv('../uber_data.csv').dropna()
            manhattan = uber[uber['borough']=='Manhattan']
            steps = -1
            manhattan['actual'] = manhattan['pickups'].shift(steps)
            sc_out = MinMaxScaler(feature_range=(0,1))
            scaler_ouput = sc_out.fit_transform(manhattan[['actual']])
            features = pd.read_csv('../X_test_sarimax.csv')
            predictions = model.forecast(steps=len(features), exog=features)
            predictions = pd.DataFrame(predictions, columns=['Forecast'])
            
            predictions = sc_out.inverse_transform(predictions)
            predictions = predictions
            return predictions

        elif self.model_name == 'model_lgbm':
            features = pd.read_csv('../X_test_lgbm.csv')
            predictions = model.predict(features)
            return predictions

        elif self.model_name == 'model_naive':
            features = pd.read_csv('../X_test_naive.csv')
            y_test = pd.read_csv('../y_test_naive.csv')
            fh = np.arange(1,len(y_test)+1)
            predictions = model.predict(fh)
            predictions = np.array(predictions)
            return predictions

        elif self.model_name == 'model_prophet':
            features = pd.read_csv('../X_test_prophet.csv')
            predictions = model.predict(features)
            predictions = np.array(predictions['yhat'][-720:])
            return predictions

        else:
            raise ValueError("Aucun des models ne correspond au model selectionné")


    def create_pickups_cluster(self,prediction_number=0, horizon=0):
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

        for i in range(0,int(self.pred_brooklyn[horizon])):
            feature = {"type": "Feature", "properties": {"id": "Brooklyn", "time": 1507425650894},
                    "geometry": {"type": "Point", "coordinates": [-73.944157, 40.678178, 0.0]}}
            populate_feature.append(feature)

        for i in range(0,int(self.pred_bronx[horizon])):
            feature = {"type": "Feature", "properties": {"id": "Bronx", "time": 1507425650895},
                    "geometry": {"type": "Point", "coordinates": [-73.865429, 40.837049, 0.0]}}
            populate_feature.append(feature)

        for i in range(0,int(self.pred_queens[horizon])):
            feature = {"type": "Feature", "properties": {"id": "Queens", "time": 1507425650896},
                    "geometry": {"type": "Point", "coordinates": [-73.741901, 40.715662, 0.0]}}
            populate_feature.append(feature)

        schema['features'] = populate_feature
        return schema

    def create_json(self, horizon=1):
        predictions = self.predictions
        cluster_value = int(predictions[horizon-1])
        json_to_pass = self.create_pickups_cluster(cluster_value, horizon=horizon-1)

        return json.dumps(json_to_pass)

    def get_y_test_pred(self):
        predictions = self.predictions
        if self.model_name == 'model_sarimax':
            y_test = pd.read_csv('../y_test_sarimax.csv')
            y_t = np.array(y_test['actual'])
            y_tt = pd.Series(y_t, index = y_test.index)
            #y_tt.index = pd.to_datetime(y_tt.index)

            y_pred = self.predictions
            y_pred = y_pred.reshape((720,))
            y_pred_df = pd.Series(y_pred[:-1], index = y_test.index)
            #y_pred_df.index = pd.to_datetime(y_pred_df.index)
            return y_tt, y_pred_df

        elif self.model_name == 'model_lgbm':
            y_test = pd.read_csv('../y_test_lgbm.csv', index_col=0)
            y_t = np.array(y_test['pickups'])
            y_tt = pd.Series(y_t, index = y_test.index)
            y_tt.index = pd.to_datetime(y_tt.index)

            y_pred = self.predictions
            y_pred_df = pd.Series(y_pred, index = y_test.index)
            y_pred_df.index = pd.to_datetime(y_pred_df.index)
            return y_tt, y_pred_df

        elif self.model_name == 'model_naive':
            y_test = pd.read_csv('../y_test_naive.csv')
            y_t = np.array(y_test['pickups'])
            y_tt = pd.Series(y_t, index = y_test.index)
            #y_tt.index = pd.to_datetime(y_tt.index)

            y_pred = self.predictions
            y_pred_df = pd.Series(y_pred, index = y_test.index)
            #y_pred_df.index = pd.to_datetime(y_pred_df.index)
            return y_tt, y_pred_df

        elif self.model_name == 'model_prophet':
            y_test = pd.read_csv('../y_test_prophet.csv', index_col=0)
            y_t = np.array(y_test['pickups'])
            y_tt = pd.Series(y_t, index = y_test.index)
            y_tt.index = pd.to_datetime(y_tt.index)

            y_pred = self.predictions
            y_pred_df = pd.Series(y_pred, index = y_test.index)
            y_pred_df.index = pd.to_datetime(y_pred_df.index)
            return y_tt, y_pred_df

        else:
            raise ValueError("Aucun des models ne correspond au model selectionné")


    def smape_perso(self,y_test, y_pred):
        return 100/len(y_test) * np.sum(2 * np.abs(y_pred - y_test) / (np.abs(y_test) + np.abs(y_pred)))
    
    def mape(self,y_test, y_pred): 
        return np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    def get_smape(self):
        predictions = self.predictions
        if self.model_name == 'model_sarimax':
            y_test = pd.read_csv('../y_test_sarimax.csv')
            predictions = predictions.reshape((720,))
            return round(self.smape_perso(y_test['actual'],predictions[:-1]),2)

        elif self.model_name == 'model_lgbm':
            y_test = pd.read_csv('../y_test_lgbm.csv')
            print(predictions.shape)
            return round(self.smape_perso(y_test['pickups'],predictions),2)

        elif self.model_name == 'model_naive':
            y_test = pd.read_csv('../y_test_naive.csv')
            return round(self.smape_perso(y_test['pickups'],predictions),2)

        elif self.model_name == 'model_prophet':
            y_test = pd.read_csv('../y_test_prophet.csv')
            return round(self.smape_perso(y_test['pickups'],predictions),2)

        else:
            raise ValueError("Aucun des models ne correspond au model selectionné")

    def get_mape(self):
        predictions = self.predictions
        if self.model_name == 'model_sarimax':
            y_test = pd.read_csv('../y_test_sarimax.csv')
            predictions = predictions.reshape((720,))
            return round(self.mape(y_test['actual'],predictions[:-1]),2)

        elif self.model_name == 'model_lgbm':
            y_test = pd.read_csv('../y_test_lgbm.csv')
            print(predictions.shape)
            return round(self.mape(y_test['pickups'],predictions),2)

        elif self.model_name == 'model_naive':
            y_test = pd.read_csv('../y_test_naive.csv')
            return round(self.mape(y_test['pickups'],predictions),2)

        elif self.model_name == 'model_prophet':
            y_test = pd.read_csv('../y_test_prophet.csv')
            return round(self.mape(y_test['pickups'],predictions),2)

        else:
            raise ValueError("Aucun des models ne correspond au model selectionné")
    

