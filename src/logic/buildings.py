import osmnx as ox
import geopandas as gpd

DEHRADUN_LAT = 30.3165
DEHRADUN_LON = 78.0469


def fetch_buildings(bounds=None):
    """Fetch buildings from OpenStreetMap for Dehradun"""
    try:
        if bounds:
            north = bounds["max_lat"]
            south = bounds["min_lat"]
            east = bounds["max_lon"]
            west = bounds["min_lon"]
        else:
            delta = 0.01
            north = DEHRADUN_LAT + delta
            south = DEHRADUN_LAT - delta
            east = DEHRADUN_LON + delta
            west = DEHRADUN_LON - delta

        tags = {"building": True}
        bbox = (north, south, east, west)
        buildings = ox.features_from_bbox(bbox=bbox, tags=tags)

        buildings = buildings[
            buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])
        ].copy()

        buildings = buildings.to_crs(epsg=4326)

        keep_cols = ['geometry', 'building', 'name', 'addr:street']
        keep_cols = [c for c in keep_cols if c in buildings.columns]
        buildings = buildings[keep_cols]
        buildings['building_id'] = range(len(buildings))

        return buildings, "success"

    except Exception as e:
        return None, str(e)