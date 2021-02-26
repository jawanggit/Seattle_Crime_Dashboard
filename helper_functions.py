from math import radians, cos, sin, asin, sqrt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date, timedelta
from pandas.tseries.offsets import DateOffset
from math import radians, cos, sin, asin, sqrt
import folium
import plotly.graph_objects as go


import json

SPD_data = pd.read_csv('sample_2018_2019.csv',delimiter = ',')
SPD_data.sort_values(by='Report DateTime', ascending = True, inplace = True)
SPD_data['coordinates'] = SPD_data[['Latitude', 'Longitude']].values.tolist()
SPD_data = SPD_data.iloc[:100000,:]


def crimes_in_radius_dates(coord, radius, start_date, end_date):
    df = SPD_data
    df['Report DateTime']=pd.to_datetime(df['Report DateTime']).dt.date
    date_mask = (pd.to_datetime(df['Report DateTime']) >= start_date) & (pd.to_datetime(df['Report DateTime']) <= end_date)
    dff = df[date_mask]

    result = [point_in_radius(value[0],value[1],coord[0],coord[1],radius)
                for value in dff['coordinates']]
         
    return dff[result]

    
def point_in_radius(lat1, lon1, lat2, lon2, radius):
    # """
    # Calculate the great circle distance between two points 
    # on the earth (specified in decimal degrees)
    # """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    if c*r<=int(radius):
        return True
    else:
        return False

def address_to_coord(address_string):
    #print(response.status_code)
    #print()
    result = address_string.replace(' ','+')
    query = f'https://nominatim.openstreetmap.org/search?q={result}&format=geojson'
    response = requests.get(f'https://nominatim.openstreetmap.org/search?q={query}&format=geojson')
    return(response.json())

def crime_marker(coord,category,map):
    colors = {'PROPERTY':'Blue','PERSON':'Red','SOCIETY':'#009933'}
    feature_property = folium.FeatureGroup('PROPERTY')
    feature_person = folium.FeatureGroup('PERSON')
    feature_society = folium.FeatureGroup('SOCIETY')
    group = {'PROPERTY':feature_property,'PERSON':feature_person,'SOCIETY':feature_society}
    for x, y in zip(coord, category):
        folium.CircleMarker(
            location = x,
            radius = 3,
            popup = y,
            color = colors[y],
            fill = True,
            fill_color = colors[y]
        ).add_to(group[y])
    for key in group.keys():
        group[key].add_to(map)

def crime_table(data,type, start, end):
    df =data[data['Crime Against Category'] == type].sort_values('Report DateTime', ascending = True)
    #df['date']=pd.to_datetime(df['Report DateTime']).dt.date
    date_mask = (pd.to_datetime(df['Report DateTime']) >= start) & (pd.to_datetime(df['Report DateTime']) <= end)
    return df[date_mask].groupby('Offense').count()['Report Number'].sort_values(ascending = False).reset_index()
    
# def crime_trend_plot(data,type, start):

#     df =data[data['Crime Against Category'] == type].sort_values('Report DateTime', ascending = True)
#     #df['date']=pd.to_datetime(df['Report DateTime']).dt.date
#     date_mask = (pd.to_datetime(df['Report DateTime']) >= start) & (pd.to_datetime(df['Report DateTime']) <= pd.to_datetime(start)+timedelta(90))
#     return df[date_mask].groupby('Offense').count()['Report Number'].reset_index()

# def plot_crime(x,y,label):

#     #x -->list of dates 
#     #y -->list of the cumsum of crime
#     #label --> string of type of crime being plotted

#     ax.plot(x,y, label = label)
#     ax.set_xlabel('Date')
#     ax.set_ylabel('# of Incidences')

#     ax.legend()

def crime_trend_data(data,type, end_date):

    df =data[data['Crime Against Category'] == type].sort_values('Report DateTime', ascending = True)
    #df['date']=pd.to_datetime(df['Report DateTime']).dt.date
    date_mask = (pd.to_datetime(df['Report DateTime']) <= end_date) & (pd.to_datetime(df['Report DateTime']) >= pd.to_datetime(end_date)-timedelta(days=180)) #selects only rows with certain timeframe
    df = df[date_mask]
    offense_names = df['Offense'].unique()
    dff = pd.DataFrame()
    
    fig = go.Figure()
    for o_type in offense_names:
        df_off = df[df['Offense'] == o_type]
        df_off['Report DateTime'] = pd.to_datetime(df_off['Report DateTime'])
        df_off = df_off.resample('M', on='Report DateTime').count()['Report Number'].reset_index()
        #df_off['offense_type'] = o_type
    
    #fig_property = px.line(dff, x ='Report DateTime', y = 'Report Number', color = 'offense_type')
    #fig_property2 = px.scatter(dff, x ='Report DateTime', y = 'Report Number', color= 'offense_type')

        fig.add_trace(go.Scatter(x =df_off['Report DateTime'], y = df_off['Report Number'],
         mode='lines+markers', name = o_type))


    fig.update_layout(legend = dict(
    yanchor = "top",
    y = -0.5,
    xanchor= "left", 
    x = 0.0
    ))
    return fig

def slider_marks(marks,start_date):
    maxmarks=marks
    #tday=pd.Timestamp.today() #gets timestamp of today
    m1date=start_date
    datelist=pd.date_range(m1date, periods=maxmarks, freq='M') # list of months as dates
    dlist=pd.DatetimeIndex(datelist).normalize()
    tags={} #dictionary relating marks on slider to tags. tags are shown as "Apr', "May', etc
    datevalues={} #dictionary relating mark to date value
    x=1
    for i in dlist:
        tags[x]=(i).strftime('%b %y') #gets the string representation of next month ex:'Apr'
        datevalues[x]=i
        x=x+1
    return tags,dlist

def site_names(col_name):
    lst_sites = SPD_data[col_name].unique()
    lst_sites = np.sort(lst_sites)
    result = []
    for site in lst_sites:
        result.append({'label': site,'value':site})
    return result


