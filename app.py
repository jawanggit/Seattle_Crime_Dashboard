from math import radians, cos, sin, asin, sqrt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import helper_functions as hf
import dash_table
from datetime import date


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
            

            dcc.Textarea(
                id='address-input',
                value='Input Street Address in Seattle, WA'
            ),
            dcc.RadioItems(
                id='radius-filter',
                options=[{'label': i, 'value': i} for i in ['2 mile radius', '5 mile radius', '10 mile radius']],
                value='Radius',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2017, 1, 1),
            max_date_allowed=date(2019, 12, 31),
            initial_visible_month=date(2017, 1, 4),
            end_date=date(2017, 1, 10)
            ),
            dcc.RadioItems(
                id='date-range',
                options=[{'label': i, 'value': i} for i in ['1 month', '3 month', '1 year']],
                value='range',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        html.H3(children = 'Crime Map'),
        html.Iframe(id = 'map', srcDoc = open('test.html','r').read(), width ='90%', height = '800')
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

# @app.callback(
# )

if __name__ == '__main__':
    app.run_server(debug=True)