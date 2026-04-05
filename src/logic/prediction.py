import geopandas as gpd
import numpy as np
from shapely.geometry import Point

DEHRADUN_LAT = 30.3165
DEHRADUN_LON = 78.0469

# Real Rispana and Bindal river corridor coordinates
RIVER_CORRIDORS = [
    {
        "name": "Rispana River",
        "points": [
            (78.0200, 30.3800),
            (78.0350, 30.3600),
            (78.0500, 30.3400),
            (78.0600, 30.3200),
            (78.0700, 30.3000),
        ]
    },
    {
        "name": "Bindal River",
        "points": [
            (78.0800, 30.3800),
            (78.0750, 30.3600),
            (78.0700, 30.3400),
            (78.0650, 30.3200),
            (78.0600, 30.3000),
        ]
    },
    {
        "name": "Song River",
        "points": [
            (78.1200, 30.4000),
            (78.1000, 30.3700),
            (78.0900, 30.3400),
        ]
    }
]


def rainfall_to_radius(rainfall_mm_hr, duration_hrs):
    """Convert rainfall intensity + duration to flood radius in meters"""
    if rainfall_mm_hr < 2.5:
        base = 500
    elif rainfall_mm_hr < 7.5:
        base = 1000
    elif rainfall_mm_hr < 15:
        base = 2000
    elif rainfall_mm_hr < 35.5:
        base = 3500
    elif rainfall_mm_hr < 64.5:
        base = 5000
    else:
        base = 8000

    duration_factor = min(1 + (duration_hrs - 1) * 0.15, 2.5)
    return base * duration_factor


def generate_flood_zones(rainfall_mm_hr, duration_hrs):
    """Generate flood zone polygons along river corridors"""
    radius_m = rainfall_to_radius(rainfall_mm_hr, duration_hrs)
    radius_deg = radius_m / 111000  # convert meters to degrees approx

    zones = []
    for river in RIVER_CORRIDORS:
        for lon, lat in river["points"]:
            zone = Point(lon, lat).buffer(radius_deg)
            zones.append({
                "geometry": zone,
                "river": river["name"],
                "radius_m": round(radius_m)
            })

    flood_gdf = gpd.GeoDataFrame(zones, crs="EPSG:4326")
    flood_gdf = flood_gdf.dissolve().reset_index(drop=True)
    return flood_gdf


def get_risk_label(rainfall_mm_hr):
    if rainfall_mm_hr < 7.5:
        return "Low Risk", "green"
    elif rainfall_mm_hr < 35.5:
        return "Moderate Risk", "orange"
    else:
        return "High Risk", "red"


def predict_flood_buildings(rainfall_mm_hr, duration_hrs, buildings_gdf):
    """Predict which buildings are at risk based on rainfall"""
    if buildings_gdf is None or buildings_gdf.empty:
        return None, None

    flood_zones = generate_flood_zones(rainfall_mm_hr, duration_hrs)
    risk_label, risk_color = get_risk_label(rainfall_mm_hr)

    result = gpd.sjoin(
        buildings_gdf,
        flood_zones[['geometry']],
        how='left',
        predicate='intersects'
    )

    result['flood_risk'] = result['index_right'].notna()
    result['risk_label'] = np.where(result['flood_risk'], risk_label, "Safe")
    result['risk_color'] = np.where(result['flood_risk'], risk_color, "green")

    # Drop duplicates from spatial join
    result = result.drop_duplicates(subset=['building_id'])

    return result, flood_zones