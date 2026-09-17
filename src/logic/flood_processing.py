import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from rasterio.features import shapes
from pyproj import CRS
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
TIF_PATH = os.path.join(DATA_DIR, 'Dehradun_NDWI.tif')

NDWI_THRESHOLD = 0.0


def load_and_process_tif():
    if not os.path.exists(TIF_PATH):
        return None, None, f"TIF file not found at: {TIF_PATH}"
    try:
        with rasterio.open(TIF_PATH) as src:
            data = src.read(1).astype(float)
            transform = src.transform
            crs = src.crs
            bounds = src.bounds
            nodata = src.nodata

        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)

        flood_mask = (data > NDWI_THRESHOLD).astype(np.uint8)

        flood_polygons = []
        for geom, val in shapes(flood_mask, transform=transform):
            if val == 1:
                flood_polygons.append(shape(geom))

        if not flood_polygons:
            return None, None, "No flood zones detected."

        # Force CRS to EPSG:4326 if missing
        if crs is None:
            crs = CRS.from_epsg(4326)

        flood_gdf = gpd.GeoDataFrame(
            geometry=flood_polygons,
            crs=crs
        ).to_crs(epsg=4326)

        bounds_wgs84 = {
            "min_lon": bounds.left,
            "max_lon": bounds.right,
            "min_lat": bounds.bottom,
            "max_lat": bounds.top
        }

        return flood_gdf, bounds_wgs84, "success"

    except Exception as e:
        return None, None, str(e)


def get_flood_statistics(flood_gdf):
    if flood_gdf is None or flood_gdf.empty:
        return {}
    try:
        # Force epsg:32644 for India UTM zone
        flood_utm = flood_gdf.copy()
        flood_utm = flood_utm.set_crs(epsg=4326, allow_override=True)
        flood_utm = flood_utm.to_crs(epsg=32644)
        total_area_km2 = flood_utm.geometry.area.sum() / 1e6
        return {
            "total_flood_area_km2": round(total_area_km2, 3),
            "flood_polygon_count": len(flood_gdf),
        }
    except Exception:
        return {
            "total_flood_area_km2": 0,
            "flood_polygon_count": len(flood_gdf),
        }
        