


SPD_data = pd.read_csv('sample_2018_2019.csv',delimiter = ',')

SPD_data = SPD_data.iloc[:100000,:]
SPD_data= SPD_data.sort_values(by ='Crime Against Category')
SPD_data

m = folium.Map(location=[47.63053012408091, -122.33246064193719],
 zoom_start = 12)

def crime_marker(coord,category):
    colors = {'PROPERTY':'Blue','PERSON':'Red','SOCIETY':'Brown'}
    feature_property = folium.FeatureGroup('PROPERTY')
    feature_person = folium.FeatureGroup('PERSON')
    feature_society = folium.FeatureGroup('SOCIETY')
    group = {'PROPERTY':feature_property,'PERSON':feature_person,'SOCIETY':feature_society}
    for x, y in zip(coord, category):
        folium.CircleMarker(
            location = x,
            radius = .1,
            popup = y,
            color = colors[y],
            fill = True,
            fill_color = colors[y]
        ).add_to(group[y])
    for key in group.keys():
        group[key].add_to(m)

SPD_data['Coord'] = SPD_data[['Latitude', 'Longitude']].values.tolist()

crime_marker(SPD_data['Coord'],SPD_data['Crime Against Category'])

folium.LayerControl(position='topright',collapsed='False').add_to(m)

m.save('Seattle 2019 Crime Map.html')

