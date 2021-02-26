from math import radians, cos, sin, asin, sqrt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import helper_functions as hf
from helper_functions import SPD_data
import dash_table
import geopy
import folium
import numpy as np
import scipy.stats as stats

from datetime import date, timedelta




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([ 
     dcc.Tabs(id='tabs-example', value='tab-crime', children=[
        dcc.Tab(label='Crime Dashboard', value='tab-crime'),
        dcc.Tab(label='Hypothesis Testing on Crime Data', value='tab-testing'),
    ]),
    html.Div(id = 'tab-content')
],style={
            'backgroundColor': '#ddd',
        })   

@app.callback(Output('tab-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-crime':
        return html.Div([    
        html.Div([ 
            html.H3(children='Seattle Interactive Crime Dashboard', style = {'font-size':'40px','textAlign':'center'}),

            html.Div([
                
                html.H5(children='Enter a Seattle Address to see Crime Incidences:'),

                dcc.Input(
                    id='address-input',
                    debounce = True,
                    size = '100',
                    type = 'search',
                    placeholder ='Input Street Address in Seattle, WA',
                    value = 'Pioneer Square, Seattle, WA',
                ),
        
                dcc.RadioItems(
                    id='radius-filter',
                    options=[{'label': j, 'value': i} 
                                for i,j in {2:'2 mile radius',
                                4:'4 mile radius', 6:'6 mile radius'}.items()],
                    value='1',
                    labelStyle={'display': 'inline-block'}
                ),

                html.H5(children='Date Range for Crimes Reported:'),
                
                dcc.RangeSlider(
                    id='my-datetime-slider',
                    updatemode = 'mouseup',
                    min =1,
                    max =25,
                    step = None,
                    value = [1,3],
                    marks = hf.slider_marks(25,date(2017, 1, 1))[0],
                )
            ], style={'width': '100%', 'display': 'inline-block',
             'textAlign': 'center'}),
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 30px',
            'height':'290px',
        }),
        html.Div([
            html.H3(children = 'Seattle Crime Map'),
            html.Iframe(id = 'crime-map', srcDoc = open('start_address.html','r').read(), width ='100%', height = '500')
        ],style = {'width':'28%', 'display': 'inline-block',
        'textAlign':'center','padding':'10px 5px'}),
        
        html.Div([
            html.H6(children = 'Types of Person Offenses'),
            dash_table.DataTable(
                id = "Person_Table",
                data = hf.crime_table(SPD_data,'PERSON', '2017-01-01','2017-01-02').to_dict('records'),
                columns = [{"name":i, 'id': i } for i in hf.crime_table(SPD_data,'PERSON', '2017-01-02','2017-01-05')],            
                style_cell = {'whiteSpace':'normal',
                                'height':'auto',},
                style_table = {'height': '300px','overflowY': 'auto'}
            ),
            html.H6(children = 'Person Offenses: Past 6 Month Trend'),
            dcc.Graph(id = 'Person_Graph',
            )
        ],style = {'width':'23%', 'float': 'right', 'display': 'inline-block','textAlign':'center', 'padding': '10px 5px'}),

        html.Div([
            html.H6(children = 'Types of Property Offenses'),
            dash_table.DataTable(
                id = "Property_Table",
                columns = [{"name":i, 'id': i } for i in hf.crime_table(SPD_data,'PROPERTY', '2017-01-02','2017-01-05')],
                data = hf.crime_table(SPD_data,'PROPERTY', '2017-01-01','2017-01-02').to_dict('records'),
                style_cell = {'whiteSpace':'normal',
                                'height':'auto',},
                style_table = {'height': '300px','overflowY': 'auto'}
            ),
            html.H6(children = 'Property Offenses: Past 6 Month Trend'),
            dcc.Graph(id = 'Property_Graph',
            )        
        ],style = {'width':'23%','float': 'right','display': 'inline-block', 'textAlign':'center','padding': '10px 5px'}),

        html.Div([
            html.H6(children = 'Types of Society Offenses'),
            dash_table.DataTable(
                id = "Society_Table",
                columns = [{"name":i, 'id': i } for i in hf.crime_table(SPD_data,'SOCIETY', '2017-01-02','2017-01-05')],
                data = hf.crime_table(SPD_data,'SOCIETY', '2017-01-01','2017-01-02').to_dict('records'),
                style_cell = {'whiteSpace':'normal',
                                'height':'auto',},
                style_table = {'height': '300px','overflowY': 'auto'}
            ),
            html.H6(children = 'Society Offenses: Past 6 Month Trend'),
            dcc.Graph(id = 'Society_Graph',
            )     
        ],style = {'width':'22%', 'float': 'right','display': 'inline-block', 'textAlign':'center', 'padding': '10px 5px'}),
    ], style={
            'backgroundColor': '#ddd',
            'height':'1200px'
        })
    elif tab == 'tab-testing':
        return html.Div([
            html.H3('''This page lets you test if a certain area/neighborhood in Seattle
            have a greater incident rate per month for various types of offenses compared to other 
            areas/neighborhoods.\n For example, does Pioneer Square have more average incidences per month of "Simple Assault" than Wallingford?'''),
        
            html.H3('Select an offense type:'),
            
            dcc.Dropdown(
                id = 'offense-dropdown',
                options=hf.site_names('Offense'),
                value = 'Simple Assault'
            ),


            html.H3('Select an area/neighborhood in Seattle:'),

            dcc.Dropdown(
                id = 'first-dropdown',
                options=hf.site_names('MCPP'),
                value = 'PIONEER SQUARE'
            ),

            html.H3('Select another area/neighborhood in Seattle to compare against:'),

            dcc.Dropdown(
                id = 'second-dropdown',
                options=hf.site_names('MCPP'),
                value = 'WALLINGFORD'
            ),

            html.H3('Conclusion:',style = {'font-size':'40px','textAlign':'center'} ),
            
            dcc.Textarea(
                id = 'result',
                placeholder = 'ipsum lorem',
                value = 'This is where the conclusion goes',
                style = {'width':'100%', 'height':'10%','font-size':'20px','textAlign':'center'}
            ),
            dcc.Graph(
                id = 'histogram-graph',
                style = {'width':'48%', 'height':'300px','font-size':'10px','display':'inline-block','textAlign':'center','padding': '10px 5px'}
            ),
            dcc.Graph(
                id = 'pdf-graph',
                style = {'width':'48%', 'height':'300px','font-size':'10px','display':'inline-block','textAlign':'center','padding': '10px 5px'}
            )
        ], style = {'height':'1000px', 'padding': '10px 5px'})




@app.callback(
    Output(component_id='result',component_property='value'),
    Output(component_id='histogram-graph',component_property='figure'),
    Output(component_id='pdf-graph',component_property='figure'),
    Input(component_id='offense-dropdown',component_property = 'value'),
    Input(component_id='first-dropdown',component_property = 'value'),
    Input(component_id='second-dropdown',component_property = 'value'),
)
def testing(offense_type, n1,n2):
    fig = go.Figure()
    if n1 ==n2:
        return ('Both groups are the same, no hypthesis test is needed',fig, fig)
    mask = (hf.SPD_data['Offense'] == offense_type) & ((hf.SPD_data['MCPP'].str.contains(n1)) | (hf.SPD_data['MCPP'].str.contains(n2)))
    #print(mask)
    df = hf.SPD_data[mask]
    #print(df)
    if df.empty:
        return ("Unable to compare these groups since one of the groups has no offenses of that type",fig,fig)
    
    df['test']=df.apply(lambda x: 1 if n2 in x['MCPP'] else 0,axis=1)
    df['Report DateTime'] = pd.to_datetime(df['Report DateTime'])
    dff = df[['Report DateTime','test']].sort_values('Report DateTime', ascending = True)
    dff_n1 = dff[dff['test'] == 0]
    dff_n2 = dff[dff['test'] == 1]
    #got the count of each group by month and then dropped the date column
    dff_n1 = dff_n1.resample('M', on='Report DateTime').count()['test'].reset_index()
    dff_n1 = dff_n1['test']
    dff_n2 = dff_n2.resample('M', on='Report DateTime').count()['test'].reset_index()
    dff_n2 = dff_n2['test']
    #mean of each group
    mean_n1 = np.mean(dff_n1)
    mean_n2 = np.mean(dff_n2)
    #variance of each group
    var_n1 = dff_n1.var(ddof=1)
    var_n2 = dff_n2.var(ddof=1)
    #std error of each group
    s_n1 = np.std(dff_n1)
    s_n2 = np.std(dff_n2)
    #t-statistic
    #histogram_plot(dff_n1,dff_n2,n1,n2)
    n1_dist = stats.norm(loc = mean_n1, scale = s_n1)
    n2_dist = stats.norm(loc = mean_n2, scale = s_n2)
    #print(mean_n1,mean_n2)
    
    x_range = np.linspace(0,10,100,endpoint = True)
    x_range_area = np.linspace(n1_dist.ppf(.95),10,100,endpoint = True) 
     
    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=x_range, y=n1_dist.pdf(x_range), name=n1,
                         line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=x_range, y=n2_dist.pdf(x_range), name=n2,
                         line=dict(color='royalblue', width=4)))

    fig.add_trace(go.Scatter(x=x_range_area, y=n1_dist.pdf(x_range_area),name=n1, line=dict(color='firebrick'),
    fill = 'tozeroy'))
                        
    
    fig.update_layout(title=f'Probability Density Graph with 5% Significance Threshold',
                   xaxis_title='Avg Monthly Incident Rate',
                   yaxis_title='Probability Density')
   
    result = stats.ttest_ind(dff_n1,dff_n2, axis=0,equal_var=False,alternative='greater') 
    

    if result[1]<.05:
        return ((f'{n1} average incidences per month: {mean_n1:.2f} and {n2} average incidences per month: {mean_n2:.2f}.\n\n'
         f'Under a Two Sample T-Test, the t-statistic was {result[0]} with a p-value of {result[1]}.\n'
         f'Thus, we can reject our null hypothesis (alpha of .05) that there is NO difference in incidences per month for {offense_type} between {n1} and {n2}.\n'
         f'We also have strong evidence to accept the alternative hypothesis which is that {n1} has more average incidences per month of {offense_type} than {n2}'),
         hf.histogram_plot(dff_n1,dff_n2,n1,n2), fig)

    else:
        return ((f'{n1} average incidences per month: {mean_n1:.2f} and {n2} average incidences per month: {mean_n2:.2f}.\n'
         f'Under a Two Sample T-Test, the t-statistic was {result[0]} with a p-value of {result[1]}.\n'
         f'Thus, we fail to reject our null hypothesis (alpha of .05) that there is NO difference in average incidences per monnth for {offense_type} between {n1} and {n2}.\n'),
         hf.histogram_plot(dff_n1,dff_n2,n1,n2), fig)


    
@app.callback(
    Output(component_id='crime-map',component_property='srcDoc'),
    Output(component_id = 'Person_Table',component_property = 'data'),
    Output(component_id = 'Property_Table',component_property = 'data'),
    Output(component_id = 'Society_Table',component_property = 'data'),
    Output(component_id = 'Person_Graph',component_property = 'figure'),
    Output(component_id = 'Property_Graph',component_property = 'figure'),
    Output(component_id = 'Society_Graph',component_property = 'figure'),
    Input(component_id='address-input',component_property = 'value'),
    Input(component_id='radius-filter',component_property = 'value'),
    Input(component_id ='my-datetime-slider', component_property = 'value'),
)
def address_to_coord(address_string,radius, range):
    geolocator = geopy.geocoders.MapQuest(api_key =	'E2jkOX2GsyC18ys4zRwZBAzY2nYd2MMR')
    location = geolocator.geocode(query = address_string, exactly_one = True)
    #convert range to datetime dates
    month_dict = {}
    for k,v in enumerate(hf.slider_marks(25,date(2017, 1, 1))[1]):
        month_dict[k+1]=v
    start_date = pd.to_datetime(month_dict[range[0]])
    end_date = pd.to_datetime(month_dict[range[1]])
    
    print(f'start date: {start_date}')
    print(f'end date: {end_date}')
    
    m = folium.Map(location=location[1], zoom_start = 14)
    folium.Marker(location = location[1], popup=location[1],
                    tooltip = '<i>Your Location</i>', icon=folium.Icon(color="orange")).add_to(m)
    map_data = hf.crimes_in_radius_dates(location[1],radius,start_date,end_date)
    hf.crime_marker(map_data['coordinates'],map_data['Crime Against Category'],m)
    folium.LayerControl(position='topright',collapsed='False').add_to(m)
    m.save("start_address.html")
    
    #created data for tables and line plots
    person_table = hf.crime_table(map_data,'PERSON', start_date,end_date).to_dict('records') 
    property_table = hf.crime_table(map_data,'PROPERTY', start_date,end_date).to_dict('records')
    society_table = hf.crime_table(map_data,'SOCIETY', start_date,end_date).to_dict('records')
    person_graph = hf.crime_trend_data(map_data,'PERSON',end_date)
    property_graph = hf.crime_trend_data(map_data,'PROPERTY',end_date)
    society_graph = hf.crime_trend_data(map_data,'SOCIETY',end_date)
    
    return open('start_address.html','r').read(), person_table, property_table, society_table,person_graph,property_graph,society_graph


if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)