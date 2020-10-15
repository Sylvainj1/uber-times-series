import numpy as np
import pickle
from flask import Flask, request, render_template


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

@app.route('/')
def mapbox_js():
    return render_template(
        'mapbox_js.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY
    )

if __name__ == '__main__':
    app.run()