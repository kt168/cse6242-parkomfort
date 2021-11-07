import os
import json
import pandas as pd
import plotly

from flask import Flask
from flask import render_template, request

import plotly.express as px
from plotly.graph_objects import Choroplethmapbox


# create the Flask instance.
app = Flask(__name__)


# load data
dirname = os.path.dirname(__file__)
vehicle_larceny_filename = os.path.join(dirname, '../data/vehicle_larceny_loc.csv')
nyc_police_precincts_filename = os.path.join(dirname, '../data/nyc_police_precincts.geojson')

vehicle_larceny_loc_df = pd.read_csv(vehicle_larceny_filename)
nyc_precincts = json.load(open(nyc_police_precincts_filename))


# index webpage displays visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    # visualize data by precinct
    vehicle_larceny_by_pct = pd.DataFrame(vehicle_larceny_loc_df.groupby('ADDR_PCT_CD')['ADDR_PCT_CD'].count()).rename(columns={"ADDR_PCT_CD":"COUNT"}).reset_index()
    vehicle_larceny_by_pct = vehicle_larceny_by_pct.astype({"ADDR_PCT_CD":str})

    # create visuals
    graphs = [
        {
            'data': [
                Choroplethmapbox(
                    geojson=nyc_precincts,
                    locations=vehicle_larceny_by_pct["ADDR_PCT_CD"],
                    featureidkey="properties.precinct",
                    z=vehicle_larceny_by_pct["COUNT"],
                    hovertemplate = 'Policy Precinct=%{location}<br>Vehicle Larceny Count=%{z}<extra></extra>',
                    coloraxis= 'coloraxis'
                )
            ],

            'layout': {
                'title': 'vehicle_larceny_by_pct',
                'font': {
                    'family': 'arial'
                },
                'margin':{
                    "r":0,"t":0,"l":0,"b":0
                },
                'mapbox': {'center': {'lat': 40.7, 'lon': -73.9},
                           'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                           'style': 'carto-positron',
                           'zoom': 9},
               'coloraxis': {'colorbar': {'title': {'text': 'Vehicle Larceny Count'}}}
            }
        },
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays results
# feel free to create other routes
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query. this is an example of classification
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
