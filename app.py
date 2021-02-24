from math import radians, cos, sin, asin, sqrt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import helper_functions as hf
import dash_table
import geopy
import folium
from datetime import date, timedelta




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_Property = hf.crime_trend_data('PROPERTY','2017-01-01')
fig_property = px.line(df_Property, x ='date', y = 'Report Number', color = 'offense_type')

df_Person = hf.crime_trend_data('PERSON','2017-01-01')
fig_person = px.line(df_Person, x ='date', y = 'Report Number', color = 'offense_type')

df_Society = hf.crime_trend_data('PERSON','2017-01-01')
fig_society = px.line(df_Society, x ='date', y = 'Report Number', color = 'offense_type')


app.layout = html.Div([
    
    html.Div([
        html.H3(children='Seattle Interactive Crime Dashboard'),

        html.Div([
            

            dcc.Input(
                id='address-input',
                debounce = True,
                size = '100',
                type = 'search',
                placeholder ='Input Street Address in Seattle, WA',
                value = 'Seattle,WA',
            ),
            #html.Button('Submit', id = 'submit_button', n_clicks=0),
            dcc.RadioItems(
                id='radius-filter',
                options=[{'label': i, 'value': i} for i in ['2 mile radius', '5 mile radius', '10 mile radius']],
                value='Radius',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            html.H5(children='Specify Desired Date Range:'),
            dcc.RangeSlider(
            id='my-datetime-slider',
            updatemode = 'mouseup',
            min =1,
            max =25,
            step = None,
            value = [1,3],
            marks = hf.slider_marks(25,date(2017, 1, 1))[0],
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        html.H3(children = 'Seattle Crime Map'),
        html.Iframe(id = 'crime-map', srcDoc = open('start_address.html','r').read(), width ='90%', height = '800')
    ],style = {'width':'20%', 'display': 'inline-block', 'textAlign':'center'}),
    
    html.Div([
        html.H6(children = 'Types of Person Offenses'),
        dash_table.DataTable(
            id = "Person_Table",
            columns = [{"name":i, 'id': i } for i in hf.crime_table('PERSON', '2017-01-02','2017-01-05')],
            data = hf.crime_table('PERSON', '2017-01-01','2017-01-02').to_dict('records'),
            style_cell = {'whiteSpace':'normal',
                            'height':'auto',},
            style_table = {'height': '500px','overflowY': 'auto'}
        ),
        html.H6(children = 'Person Offenses: Past 6 Month Trend'),
        dcc.Graph(figure = fig_person),
    ],style = {'width':'25%', 'float': 'right', 'display': 'inline-block', 'textAlign':'center'}),

    html.Div([
        html.H6(children = 'Types of Property Offenses'),
        dash_table.DataTable(
            id = "Property_Table",
            columns = [{"name":i, 'id': i } for i in hf.crime_table('PROPERTY', '2017-01-02','2017-01-05')],
            data = hf.crime_table('PROPERTY', '2017-01-01','2017-01-02').to_dict('records'),
            style_cell = {'whiteSpace':'normal',
                            'height':'auto',},
            style_table = {'height': '500px','overflowY': 'auto'}
        ),
        html.H6(children = 'Property Offenses: Past 6 Month Trend'),
        dcc.Graph(figure = fig_property)        
    ],style = {'width':'30%','float': 'right', 'display': 'inline-block', 'textAlign':'center'}),

    html.Div([
        html.H6(children = 'Types of Society Offenses'),
        dash_table.DataTable(
            id = "Society_Table",
            columns = [{"name":i, 'id': i } for i in hf.crime_table('SOCIETY', '2017-01-02','2017-01-05')],
            data = hf.crime_table('SOCIETY', '2017-01-01','2017-01-02').to_dict('records'),
            style_cell = {'whiteSpace':'normal',
                            'height':'auto',},
            style_table = {'height': '500px','overflowY': 'auto'}
        ),
        html.H6(children = 'Society Offenses: Past 6 Month Trend'),
        dcc.Graph(figure = fig_society)     
    ],style = {'width':'25%', 'float': 'right', 'display': 'inline-block', 'textAlign':'center'}),
])

@app.callback(
    Output(component_id='crime-map',component_property='srcDoc'),
    Input(component_id='address-input',component_property = 'value'),
    Input(component_id='radius-filter',component_property = 'value'),
    Input(component_id ='my-datetime-slider', component_property = 'value')
    #State('address-input', 'value')
)
def address_to_coord(address_string,radius, range):
    #print(response.status_code)
    #print()
    geolocator = geopy.geocoders.MapQuest(api_key =	'E2jkOX2GsyC18ys4zRwZBAzY2nYd2MMR')
    location = geolocator.geocode(query = address_string, exactly_one = True)
    m = folium.Map(location=location[1], zoom_start = 15)
    folium.Marker(location = location[1], popup=location[1],
                    tooltip = '<i>Your Location</i>', icon=folium.Icon(color="green")).add_to(m)
    map_data = crimes_in_radius_dates(location[1],radius,range)
    crime_marker(map_data['coord'],map_data['Crime Against Category'])
    m.save("start_address.html")
    return open('start_address.html','r').read()

if __name__ == '__main__':
    app.run_server(debug=True)