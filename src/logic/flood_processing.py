import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from rasterio.features import shapes
import os

# Path to your NDWI tif - directly in data folder
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
TIF_PATH = os.path.join(DATA_DIR, 'Dehradun_NDWI.tif')

# Pixels above this value = water/flood
NDWI_THRESHOLD = 0.0


def load_and_process_tif():
    """Load Dehradun_NDWI.tif and extract flood zones"""
    if not os.path.exists(TIF_PATH):
        return None, None, f"TIF file not found at: {TIF_PATH}"

    try:
        with rasterio.open(TIF_PATH) as src:
            data = src.read(1).astype(float)
            transform = src.transform
            crs = src.crs
            bounds = src.bounds
            nodata = src.nodata

        # Replace nodata with nan
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)

        # NDWI > 0 means water
        flood_mask = (data > NDWI_THRESHOLD).astype(np.uint8)

        # Convert flood pixels to polygons
        flood_polygons = []
        for geom, val in shapes(flood_mask, transform=transform):
            if val == 1:
                flood_polygons.append(shape(geom))

        if not flood_polygons:
            return None, None, "No flood zones detected. Try lowering NDWI threshold."

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
    """Calculate flood area in km2"""
    if flood_gdf is None or flood_gdf.empty:
        return {}
    try:
        flood_utm = flood_gdf.to_crs(epsg=32644)
        total_area_km2 = flood_utm.geometry.area.sum() / 1e6
        return {
            "total_flood_area_km2": round(total_area_km2, 3),
            "flood_polygon_count": len(flood_gdf),
        }
    except Exception:
        return {"total_flood_area_km2": 0, "flood_polygon_count": 0}