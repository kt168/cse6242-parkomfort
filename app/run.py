import os
import json
import pandas as pd
import plotly
import math

from flask import Flask
from flask import render_template, request

import plotly.express as px
from plotly.graph_objects import Choroplethmapbox
import plotly.graph_objects as go

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
violation_by_pct_df.loc[:, 'sum'] = violation_by_pct_df.loc[:, 'sum'] + violation_by_pct_21_df.loc[:, 'sum']

# index webpage displays visuals and receives user input text for model
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    request_type_str = request.method

    # visualize data by precinct

    # vehicle-related crimes
    vehicle_larceny_by_pct = pd.DataFrame(vehicle_larceny_loc_df.groupby('ADDR_PCT_CD')['ADDR_PCT_CD'].count()).rename(
        columns={"ADDR_PCT_CD": "COUNT"}).reset_index()
    vehicle_larceny_by_pct = vehicle_larceny_by_pct.astype({"ADDR_PCT_CD": str})

    # create visuals
    graphs = [
        {
            'data': [
                Choroplethmapbox(
                    geojson=nyc_precincts,
                    locations=vehicle_larceny_by_pct["ADDR_PCT_CD"],
                    featureidkey="properties.precinct",
                    z=vehicle_larceny_by_pct["COUNT"],
                    hovertemplate='Policy Precinct=%{location}<br>Vehicle Larceny Count=%{z}<extra></extra>',
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
                                       zoom=8.2, center={"lat": 40.7, "lon": -74.0},
                                       opacity=0.7,
                                       title="Vehicle larceny by precinct (YTD)"
                                       )

    fig_violations = px.choropleth_mapbox(violation_by_pct_df,
                                          geojson=nyc_precincts,
                                          locations="Violation Precinct",
                                          featureidkey="properties.precinct",
                                          color="sum",
                                          color_continuous_scale="amp",
                                          mapbox_style="carto-positron",
                                          zoom=8.2, center={"lat": 40.7, "lon": -74.0},
                                          opacity=0.7
                                          )

    fig_violations_20 = px.choropleth_mapbox(violation_by_pct_20_df,
                                             geojson=nyc_precincts,
                                             locations="Violation Precinct",
                                             featureidkey="properties.precinct",
                                             color="sum",
                                             color_continuous_scale="amp",
                                             mapbox_style="carto-positron",
                                             zoom=8.2, center={"lat": 40.7, "lon": -74.0},
                                             opacity=0.7,
                                             title="Parking violations by precinct (FY-2020)"
                                             )

    fig_violations_21 = px.choropleth_mapbox(violation_by_pct_21_df,
                                             geojson=nyc_precincts,
                                             locations="Violation Precinct",
                                             featureidkey="properties.precinct",
                                             color="sum",
                                             color_continuous_scale="amp",
                                             mapbox_style="carto-positron",
                                             zoom=8.2, center={"lat": 40.7, "lon": -74.0},
                                             opacity=0.7,
                                             title="Parking violations by precinct (FY-2021)"
                                             )
    # encode plotly graphs in JSON
    graphJSON_larceny = json.dumps(fig_larceny, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation_20 = json.dumps(fig_violations_20, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation_21 = json.dumps(fig_violations_21, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_violation = json.dumps(fig_violations, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    if request_type_str == 'GET':
        return render_template('master.html', graphJSON_larceny_pct='null', graphJSON_violation_pct='null',
                               graphJSON_larceny=graphJSON_larceny,
                               graphJSON_violation_20=graphJSON_violation_20,
                               graphJSON_violation_21=graphJSON_violation_21, graphJSON_violation=graphJSON_violation)
    else:
        graphJSON_larceny_pct = 'null'
        graphJSON_violation_pct = 'null'

        if 'precinctcode_larceny' in request.form.keys():
            precinctcode_larceny = request.form['precinctcode_larceny']
            vehicle_larceny_loc_df['CMPLANT_DT'] = pd.to_datetime(vehicle_larceny_loc_df['CMPLANT_DT'])
            temp_df = vehicle_larceny_loc_df[vehicle_larceny_loc_df['ADDR_PCT_CD'] == int(precinctcode_larceny)]
            temp_df['Month'] = temp_df['CMPLANT_DT'].dt.month
            larceny_pct_df = pd.DataFrame(temp_df.groupby('Month').count().iloc[:, 1]).reset_index()
            larceny_pct_df.rename(columns={larceny_pct_df.columns[1]: 'Count'}, inplace=True)
            title = "Vehicle larceny for Precinct " + precinctcode_larceny
            fig_precinct = px.bar(larceny_pct_df, x='Month', y='Count', title=title)
            fig_precinct.update_xaxes(dtick="M1")
            graphJSON_larceny_pct = json.dumps(fig_precinct, cls=plotly.utils.PlotlyJSONEncoder)

        if 'precinctcode_violation' in request.form.keys():
            precinctcode_violation = request.form['precinctcode_violation']
            violation_yr = [2020, 2021]
            violation_2020 = \
            violation_by_pct_20_df[violation_by_pct_20_df["Violation Precinct"] == int(precinctcode_violation)][
                'sum'].values[0]
            violation_2021 = \
            violation_by_pct_21_df[violation_by_pct_21_df["Violation Precinct"] == int(precinctcode_violation)][
                'sum'].values[0]
            violation_ct = [violation_2020, violation_2021]
            violation_df = pd.DataFrame(list(zip(violation_yr, violation_ct)), columns=['Fiscal Year', 'Count'])

            title = "Parking violations for Precinct " + precinctcode_violation
            fig_precinct = px.bar(violation_df, x='Fiscal Year', y='Count', title=title, width=300)
            fig_precinct.update_xaxes(type='category')
            graphJSON_violation_pct = json.dumps(fig_precinct, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('master.html',
                               graphJSON_larceny_pct=graphJSON_larceny_pct,
                               graphJSON_violation_pct=graphJSON_violation_pct, graphJSON_larceny=graphJSON_larceny,
                               graphJSON_violation_20=graphJSON_violation_20,
                               graphJSON_violation_21=graphJSON_violation_21, graphJSON_violation=graphJSON_violation)


# web page that handles user query and displays results
# feel free to create other routes
@app.route('/search', methods=['GET', 'POST'])
def go():
    request_type_str = request.method

    # read token
    script_dir = os.path.dirname(__file__)  # Script directory
    token_path = os.path.join(script_dir, '../data/.mapbox_token')

    mapbox_access_token = open(token_path).read()
    px.set_mapbox_access_token(open(token_path).read())

    full_path = os.path.join(script_dir, '../data/meter_pct_risk.csv')
    df = load_meters(full_path)

    if request_type_str == 'GET':
        fig_onload = px.scatter_mapbox(lat=[40.7],
                                       lon=[-74.0],
                                       zoom=9,
                                       opacity=0)
        graph_onload = json.dumps(fig_onload, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template(
            'search.html',
            graph_onload=graph_onload
        )

    if request_type_str == 'POST':

        import plotly.graph_objects as go
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="parkomfort-search")

        search_addr = request.form['search_addr']
        title = 'Parking meters near ' + search_addr
        # search_addr = "175 5th Avenue NYC"
        location = geolocator.geocode(search_addr)

        lat, lon = (location.latitude, location.longitude)
        # lat, lon = floats_string_to_arr(lat_lon)
        # lat, lon = 40.730948, -73.993291

        nearby = find_nearby(df, lat, lon, convert_radius(100000))
        closest = find_closest(nearby, lat, lon)


        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
            lat=closest.LAT,
            lon=closest.LONG,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(255, 0, 0)',
                opacity=0.7
            ),
            text=closest.Addr,
            hoverinfo='text'
        ))

        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            hoverinfo='none'
        ))

        fig.update_layout(
            title=title,
            autosize=True,
            hovermode='closest',
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=lat,
                    lon=lon
                ),
                pitch=0,
                zoom=15,
                style='light'
            ),
        )

        graph_closest = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template(
            'search.html',
            graph_closest=graph_closest
        )


# meter calc
def load_meters(path: str) -> pd.DataFrame:
    meters = pd.read_csv(path)
    return meters


def convert_radius(meters):
    return meters * 0.00001 / 1.11


def reverse_convert_radius(radians):
    return radians * 1.11 / 0.00001


def calculate_distance(row, lat, lon):
    lat = max(row["LAT"], lat) - min(row["LAT"], lat)
    lon = max(row["LONG"], lon) - min(row["LONG"], lon)
    return math.sqrt(lat ** 2 + lon ** 2)


def find_nearby(df, lat, lon, radius, exclude=1):
    left = lon - radius
    right = lon + radius
    down = lat - radius
    up = lat + radius
    df = df[(df.LONG > left) & (df.LONG < right) & (df.LAT < up) & (df.LAT > down) & (df.risk_factor<=exclude)]
    return df


def find_closest(df, lat, lon, n=10):
    df['Distance'] = df.apply(lambda row: calculate_distance(row, lat, lon), axis=1)
    df = df.sort_values('Distance', ascending=True)
    return df.head(n)


def floats_string_to_arr(floats_str):
    def is_float(s):
        try:
            float(s)
            return True
        except:
            return False

    floats = [float(x) for x in floats_str.split(',') if is_float(x)]
    return floats


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
