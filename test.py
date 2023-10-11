import geopandas as gpd
import folium
import shapely
from pathlib import Path

root =  Path("/home/mfeijoo/yo/arboles/")

# Leo arboles
path_trees = root.joinpath("platanos_reduced.geojson")
data_trees = gpd.read_file(path_trees).dropna()

# Leo ciclovias
path_bikes = root.joinpath("ciclovias/Red_Ciclovias.shp")
data_bikes = gpd.read_file(path_bikes).dropna()
data_bikes = data_bikes.to_crs(epsg=4326)
# data_bikes.to_file(root.joinpath('ciclovias.geojson'), driver='GeoJSON')


# Mapa base
mapa = folium.Map(location=[-34.598642165984955, -58.45019424141781], zoom_start=12)



features = []
lats = data_trees['lat']
lons = data_trees['long']
for lat, lon in zip(lats[:], lons[:]):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]  # Swap the order from [lat, lon] to [lon, lat]
        },
    }
    features.append(feature)

# Create a GeoJSON FeatureCollection
trees_json = {
    "type": "FeatureCollection",
    "features": features
}


# Agrego Arboles
folium.GeoJson(
    trees_json, name='Platanos', marker=folium.CircleMarker(
        radius = 3, weight = 0, fill_color = '#1CBC1C', fill_opacity = .7
    )
).add_to(mapa)

# Agrego ciclovias
folium.GeoJson(str(root.joinpath('ciclovias.geojson')), name='Bicis').add_to(mapa)

folium.LayerControl().add_to(mapa)

mapa.save('mapita.html')
