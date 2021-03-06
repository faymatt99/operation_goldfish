import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash
from dash_extensions.javascript import arrow_function, assign
from dash.dependencies import Output, Input

import json

# Pandas and geopandas stuff
import pandas as pd
import geopandas as gpd

def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + [html.P("Hoover over a state")]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]


classes = [50000, 150000, 250000, 350000, 450000, 550000,  650000, 750000]
colorscale = [ '#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")
housing_geo = pd.read_csv('./data/house_surrounding_avg_prices.csv')
housing_geo = gpd.GeoDataFrame(
    housing_geo, geometry=gpd.points_from_xy(housing_geo.longitude, housing_geo.latitude))

housing_geo = json.loads(housing_geo.to_json())


# Create geojson.
geojson = dl.GeoJSON(data = housing_geo,  # url to geojson file
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     # hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="SalePrice"),
                     id="geojson")
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar, info]), center=[42.03, -93.64], zoom=12],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"},  id="map")


# @app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
# def info_hover(feature):
#     return get_info(feature)


if __name__ == '__main__':
    app.run_server()