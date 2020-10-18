import numpy as np
import pickle
from flask import Flask, request, render_template
from jinja2 import Template
import json
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.embed import json_item
from bokeh.resources import CDN
from bokeh.resources import INLINE

from webmodel.webModel import WebModel


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

model = WebModel('model_lgbm')


@app.route('/')
def mapbox_js():
    return render_template(
        'html/index.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        pickup_data=[]
    )

@app.route('/predict', methods = ['POST'])
def predict():
    #en fait ce qu'il faudra faire, c'est laisser à l'utilisateur choisir l'horizon, ou bien la date
    # genre 1h, 2h etc...
    # recuperer cet input ici 
    #et choper la valeur en conséquence
    # par exemple ici au lieu d'avoir predictions[0] pour 1h apres,
    # #si l'utilisateur veut 2h apres ca sera predictions[1] etc...

    selected_model = request.form.get('model_select')
    horizon = int(request.form.get('horizon'))
    print(str(selected_model))
    print(str(horizon))
    model_name = selected_model.split('_')[1].capitalize()

    model = WebModel(selected_model)
    cluster_data = model.create_json(horizon)
    smape_score = model.get_smape()
    mape_score = model.get_mape()

    return render_template(
        'html/index.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        pickup_data=cluster_data,
        smape_score = smape_score,
        mape_score = mape_score,
        pred_horizon = horizon,
        model_name = model_name
    )


@app.route('/myplot')
def myplot():
    plot = figure()
    y_test, y_pred = model.get_y_test_pred()

    plot.line(x=y_pred.index, y=y_pred.values, line_color='red')
    plot.line(x=y_test.index, y=y_test.values, line_color='blue')

    return json.dumps(json_item(plot, "myplot"))


if __name__ == '__main__':
    app.run()
