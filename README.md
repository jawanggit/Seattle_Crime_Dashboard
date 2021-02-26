# Seattle Crime Dashboard with Hypothesis Testing
EDA project using Seattle Crime Data

## Project Overview & Background:
### Problem Description
Gaining insight into the understanding of the crime in your area can be very difficult. Not only is it important to understand the types and frequency of crimes happening in your area, it is critical to visualize this data across space and time. 

### Background
To show how insights can be gained from crime data, I took Seattle crime data from the [Seattle Police Department](https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5) and built an interactive dashboard that allows users to create individual views of crime in their area by type, location, and date range. In addition, on the hypothese testing tab, you can hypothesis test if certain areas in Seattle have statistically signficant greater incidences of a certain crime than another.


## Data Set Assembly:

### Data Sources
The crime data comes from the [Seattle Police Department](https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5) and ranges from Jan 2017 to Jan 2019. In order to translate inputted addresses, the app calls the MapQuest API which responds back wit a latitude and longitude. 

* Link to [MapQuest API](https://developer.mapquest.com/documentation/open/) documenatation 

### Cleaning the data
To gain a high-level understanding of the raw data, the pandas-profiling library was used generate an html report of the data. This report provides dataset statistics and variable types along with the distinct and missing counts for each variable. This report was extremely useful in quickly understanding what the different values in data represented and which features in the dataset were incomplete or would need to be excluded. 

* Link to [profiling report](https://github.com/jawanggit/Seattle_Crime_Dashboard/blob/main/spd_2018-2019.html)

Since the manipulating the data by a timeframe was a key requirement for the analysis, the "Report DateTime" column was used for reference rather than other datetime fields in the dataset. Filtering by a certain date range required casting the Reprot DateTime field to datetime object using "pd_to_datetime". Once this column was an object datetime object, the range for dataset was set between '2017-01-01' and '2019-01-01'

## Processing the data
In order to build an interactive map for dashboard, inputted addresses need to be translated into latitude and longitude coordinates which then could be applied as parameters to functions that utilized the dataset. The MapQuest API, as mentioned above, did this translation using this helper function:

```python
def address_to_coord(address_string):
 
    result = address_string.replace(' ','+')
    query = f'https://nominatim.openstreetmap.org/search?q={result}&format=geojson'
    response = requests.get(f'https://nominatim.openstreetmap.org/search?q={query}&format=geojson')
    return(response.json())
```

### Helpful functions

Other functions that were used are described below:

1. this function that plotted markers on the graph for the 3 types of Crimes (Property,Person, Society)

```python
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
```

2. this function plotted line graphs showing the 6 month trend for various types of offenses that make up a certain type of Crime Group

```python
def crime_trend_data(data,type, end_date):

    df =data[data['Crime Against Category'] == type].sort_values('Report DateTime', ascending = True)
    date_mask = (pd.to_datetime(df['Report DateTime']) <= end_date) & (pd.to_datetime(df['Report DateTime']) >= pd.to_datetime(end_date)-timedelta(days=180)) #selects only rows with certain timeframe
    df = df[date_mask]
    offense_names = df['Offense'].unique()
    dff = pd.DataFrame()
    
    fig = go.Figure()
    for o_type in offense_names:
        df_off = df[df['Offense'] == o_type]
        df_off['Report DateTime'] = pd.to_datetime(df_off['Report DateTime'])
        df_off = df_off.resample('M', on='Report DateTime').count()['Report Number'].reset_index()
        fig.add_trace(go.Scatter(x =df_off['Report DateTime'], y = df_off['Report Number'], mode='lines+markers', name = o_type))
```

## Dashboard 
### Functionality
The dashboard is hosted on the first tab (Crime Dashboard) of https://seattle-crime-app.herokuapp.com/ through Heroku.

The default view is a 1 mile radius of Pioneer Square from the dates Jan 1, 2017 to Mar 31,2017. Using the folium library allows you to filter by the Crime type in the map (click on the icon in the top right of the displayed map)

As user can specify a Seattle Address, multiple mile radius, and time range (slider) to view the number of offenses committed by Crime type. 

The 3 tables are sorted in descending order based on the inputs from the user and the 3 line graphs show the historic 6 month trend for various offenses from the end date specified. Using plotly library allows users to select and deselect specific trend lines and zoom in or zoom out on the graph.   

## Hypthesis Testing Page
### Functionality
The hypothesis page is hosted on the second tab (Hypothesis Testing on Crime Data) of https://seattle-crime-app.herokuapp.com/ through Heroku.

The default view is set to the offense of 'Simple Assault', the first location being 'Pioneer Square', and the second location being 'Wallingford'.

Based on a signficance level  of .05. a conclusion is generated whether to reject the null hypothesis.

A frequency histogram for the sampled data of the two locations is provided on the right along with a Probability Density Graph showing the significance level threshold as a shaded area

## Key Findings

Some interesting findings from using the dashboard and hypothesis testing page:
- While the dataset only covers 2 years, one can see that certain offenses trend up or down based on the time of year. For example, in 2017, 'shoplifting' seems to rise in the summer months and decline in the fall and winter,except for in November - most likely due to Black Friday shopping! 

- When it comes to property crimes, crimes rate of 'theft from motor vehicles' is not statistically higher in commercial areas like Pioneer Square than more residential neighborhoods like Ballard or Greenwood. However, when it comes to 'simple assault', Pioneer Square has a statistically higher rate of incidences than Ballard or Greenwwod.  
