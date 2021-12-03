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

violation_by_pct_20_filename = os.path.join(dirname, '../data/violation_precinct_20.csv')
violation_by_pct_21_filename = os.path.join(dirname, '../data/violation_precinct_21.csv')

vehicle_larceny_loc_df = pd.read_csv(vehicle_larceny_filename)
nyc_precincts = json.load(open(nyc_police_precincts_filename))
violation_by_pct_20_df = pd.read_csv(violation_by_pct_20_filename)
violation_by_pct_21_df = pd.read_csv(violation_by_pct_21_filename)

# merge violation data
violation_by_pct_df = violation_by_pct_20_df.copy()
violation_by_pct_df.loc[:,'sum'] = violation_by_pct_df.loc[:,'sum'] + violation_by_pct_21_df.loc[:,'sum']


# index webpage displays visuals and receives user input text for model
@app.route('/', methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    request_type_str = request.method

    # visualize data by precinct

    # vehicle-related crimes
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
                'font': {
                    'family': 'arial'
                },
                'margin':{
                    "r":0,"t":0,"l":0,"b":0
                },
                'mapbox': {'center': {'lat': 40.7, 'lon': -74.0},
                           'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                           'style': 'carto-positron',
                           'zoom': 8.8},
               'coloraxis': {'colorbar': {'title': {'text': 'Vehicle Larceny Count'}}}
            }
        },
        {
            'data': [
                Choroplethmapbox(
                    geojson=nyc_precincts,
                    locations=violation_by_pct_20_df["Violation Precinct"],
                    featureidkey="properties.precinct",
                    z=violation_by_pct_20_df["sum"],
                    hovertemplate='Policy Precinct=%{location}<br>Parking Violation Count=%{z}<extra></extra>',
                    coloraxis='coloraxis'
                )
            ],

            'layout': {
                'font': {
                    'family': 'arial'
                },
                'margin': {
                    "r": 0, "t": 0, "l": 0, "b": 0
                },
                'mapbox': {'center': {'lat': 40.7, 'lon': -74.0},
                           'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                           'style': 'carto-positron',
                           'zoom': 8.8},
                'coloraxis': {'colorbar': {'title': {'text': 'Parking Violation Count'}}},
            }
        },

        {
            'data': [
                Choroplethmapbox(
                    geojson=nyc_precincts,
                    locations=violation_by_pct_21_df["Violation Precinct"],
                    featureidkey="properties.precinct",
                    z=violation_by_pct_21_df["sum"],
                    hovertemplate='Policy Precinct=%{location}<br>Parking Violation Count=%{z}<extra></extra>',
                    coloraxis='coloraxis'
                )
            ],

            'layout': {
                'font': {
                    'family': 'arial'
                },
                'margin': {
                    "r": 0, "t": 0, "l": 0, "b": 0
                },
                'mapbox': {'center': {'lat': 40.7, 'lon': -74.0},
                           'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                           'style': 'carto-positron',
                           'zoom': 8.8},
                'coloraxis': {'colorbar': {'title': {'text': 'Parking Violation Count'}}},
            }
        },

        {
            'data': [
                Choroplethmapbox(
                    geojson=nyc_precincts,
                    locations=violation_by_pct_df["Violation Precinct"],
                    featureidkey="properties.precinct",
                    z=violation_by_pct_df["sum"],
                    hovertemplate='Policy Precinct=%{location}<br>Parking Violation Count=%{z}<extra></extra>',
                    coloraxis='coloraxis'
                )
            ],

            'layout': {
                'font': {
                    'family': 'arial'
                },
                'margin': {
                    "r": 0, "t": 0, "l": 0, "b": 0
                },
                'mapbox': {'center': {'lat': 40.7, 'lon': -74.0},
                           'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                           'style': 'carto-positron',
                           'zoom': 8.8},
                'coloraxis': {'colorbar': {'title': {'text': 'Parking Violation Count'}}},
            }
        }
    ]

    fig_larceny = px.choropleth_mapbox(vehicle_larceny_by_pct,
                           geojson=nyc_precincts,
                           locations="ADDR_PCT_CD",
                           featureidkey="properties.precinct",
                           color="COUNT",
                           color_continuous_scale="balance",
                           mapbox_style="carto-positron",
                           zoom=8.5, center={"lat": 40.7, "lon": -74.0},
                           opacity=0.7
                            )

    fig_violations = px.choropleth_mapbox(violation_by_pct_df,
                                       geojson=nyc_precincts,
                                       locations="Violation Precinct",
                                       featureidkey="properties.precinct",
                                       color="sum",
                                       color_continuous_scale="amp",
                                       mapbox_style="carto-positron",
                                       zoom=8.5, center={"lat": 40.7, "lon": -74.0},
                                       opacity=0.7
                                       )

    fig_violations_20 = px.choropleth_mapbox(violation_by_pct_20_df,
                                          geojson=nyc_precincts,
                                          locations="Violation Precinct",
                                          featureidkey="properties.precinct",
                                          color="sum",
                                          color_continuous_scale="amp",
                                          mapbox_style="carto-positron",
                                          zoom=8.5, center={"lat": 40.7, "lon": -74.0},
                                          opacity=0.7
                                          )

    fig_violations_21 = px.choropleth_mapbox(violation_by_pct_21_df,
                                             geojson=nyc_precincts,
                                             locations="Violation Precinct",
                                             featureidkey="properties.precinct",
                                             color="sum",
                                             color_continuous_scale="amp",
                                             mapbox_style="carto-positron",
                                             zoom=8.5, center={"lat": 40.7, "lon": -74.0},
                                             opacity=0.7
                                             )
    # encode plotly graphs in JSON
    graphJSON_larceny = json.dumps(fig_larceny, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation_20 = json.dumps(fig_violations_20, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation_21 = json.dumps(fig_violations_21, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation = json.dumps(fig_violations, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    if request_type_str == 'GET':
        return render_template('master.html', graphJSON_larceny_pct=None, graphJSON_larceny=graphJSON_larceny, graphJSON_violation_20=graphJSON_violation_20, graphJSON_violation_21=graphJSON_violation_21, graphJSON_violation=graphJSON_violation)
    else:
        precinctcode_larceny = request.form['precinctcode_larceny']
        vehicle_larceny_loc_df['CMPLANT_DT'] = pd.to_datetime(vehicle_larceny_loc_df['CMPLANT_DT'])
        temp_df = vehicle_larceny_loc_df[vehicle_larceny_loc_df['ADDR_PCT_CD'] == int(precinctcode_larceny)]
        temp_df['Month'] = temp_df['CMPLANT_DT'].dt.month
        larceny_pct_df = pd.DataFrame(temp_df.groupby('Month').count().iloc[:, 1]).reset_index()
        larceny_pct_df.rename(columns={larceny_pct_df.columns[1]: 'Count'}, inplace=True)
        fig_precinct = px.bar(larceny_pct_df, x='Month', y='Count')

        graphJSON_larceny_pct = json.dumps(fig_precinct, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('master.html', precinctcode_larceny=precinctcode_larceny, graphJSON_larceny_pct=graphJSON_larceny_pct, graphJSON_larceny=graphJSON_larceny, graphJSON_violation_20=graphJSON_violation_20, graphJSON_violation_21=graphJSON_violation_21, graphJSON_violation=graphJSON_violation)

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
