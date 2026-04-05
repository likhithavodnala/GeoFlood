import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
import pandas as pd
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.logic.rainfall_api import get_current_rainfall, classify_rainfall
from src.logic.buildings import fetch_buildings
from src.logic.flood_processing import load_and_process_tif, get_flood_statistics
from src.logic.prediction import predict_flood_buildings, generate_flood_zones
from src.logic.analysis import intersect_buildings_with_flood

st.set_page_config(
    page_title="GeoFlood - Dehradun",
    page_icon="🌊",
    layout="wide"
)

DEHRADUN_LAT = 30.3165
DEHRADUN_LON = 78.0469


@st.cache_data(ttl=1800)
def cached_rainfall():
    return get_current_rainfall()


@st.cache_data(ttl=86400, show_spinner=False)
def cached_buildings_post():
    """Buildings for post flood — bounded by TIF area"""
    flood_gdf, bounds, status = load_and_process_tif()
    if status != "success":
        return None, None, None, status
    buildings_gdf, b_status = fetch_buildings(bounds)
    return flood_gdf, bounds, buildings_gdf, b_status


@st.cache_data(ttl=86400, show_spinner=False)
def cached_buildings_pre():
    """Buildings for pre flood — default Dehradun area"""
    buildings_gdf, b_status = fetch_buildings()
    return buildings_gdf, b_status


def render_rainfall_dashboard(rainfall_data):
    st.subheader("🌧️ Live Rainfall — Dehradun")
    col1, col2, col3, col4 = st.columns(4)
    intensity = rainfall_data["current_intensity_mm_hr"]
    label, _ = classify_rainfall(intensity)
    col1.metric("Current Intensity", f"{intensity} mm/hr")
    col2.metric("Last 24 Hours", f"{rainfall_data['total_24h_mm']} mm")
    col3.metric("IMD Classification", label)
    col4.metric("Last Updated", rainfall_data["last_updated"])
    if not rainfall_data["daily_df"].empty:
        st.bar_chart(
            rainfall_data["daily_df"].set_index("date")["rainfall_mm"],
            use_container_width=True
        )


def show_streamlit_legend(mode):
    """Render legend using Streamlit HTML — works reliably below st_folium map"""
    if mode == "post":
        st.markdown("""
        <div style="
            display: flex;
            gap: 24px;
            align-items: center;
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 6px;
            font-family: Arial, sans-serif;
            font-size: 13px;
            color: white;
        ">
            <span style="font-weight:bold; margin-right:4px;">🗺️ Legend:</span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:#FF0000; border-radius:3px;"></span>
                Flooded Buildings
            </span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:#00FF00; border-radius:3px;"></span>
                Safe Buildings
            </span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:cyan; border-radius:3px;"></span>
                Flood Zone (NDWI Satellite)
            </span>
        </div>
        """, unsafe_allow_html=True)

    else:  # pre
        st.markdown("""
        <div style="
            display: flex;
            gap: 24px;
            align-items: center;
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 6px;
            font-family: Arial, sans-serif;
            font-size: 13px;
            color: white;
        ">
            <span style="font-weight:bold; margin-right:4px;">🗺️ Legend:</span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:#FF0000; border-radius:3px;"></span>
                At-Risk Buildings
            </span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:#00FF00; border-radius:3px;"></span>
                Safe Buildings
            </span>
            <span style="display:flex; align-items:center; gap:7px;">
                <span style="display:inline-block; width:14px; height:14px;
                             background:cyan; border-radius:3px;"></span>
                Predicted Flood Zone
            </span>
        </div>
        """, unsafe_allow_html=True)


def build_fast_map(buildings_gdf, flood_gdf, flood_col):
    """
    Fast map using GeoJson with style_function on whole layer
    instead of looping row by row
    """
    m = folium.Map(
        location=[DEHRADUN_LAT, DEHRADUN_LON],
        zoom_start=13,
        tiles="CartoDB dark_matter"
    )

    # Add flood zones as one single layer
    if flood_gdf is not None and not flood_gdf.empty:
        folium.GeoJson(
            flood_gdf.__geo_interface__,
            name="Flood Zones",
            style_function=lambda x: {
                "fillColor": "cyan",
                "color": "cyan",
                "weight": 2,
                "fillOpacity": 0.3
            }
        ).add_to(m)

    # Split buildings into 2 groups and add as 2 layers
    if buildings_gdf is not None and not buildings_gdf.empty:
        flooded = buildings_gdf[buildings_gdf[flood_col] == True]
        safe = buildings_gdf[buildings_gdf[flood_col] == False]

        # Safe buildings - green layer
        if not safe.empty:
            folium.GeoJson(
                safe[['geometry']].to_json(),
                name=f"Safe Buildings ({len(safe)})",
                style_function=lambda x: {
                    "fillColor": "#00FF00",
                    "color": "#00FF00",
                    "weight": 0.5,
                    "fillOpacity": 0.5
                }
            ).add_to(m)

        # Flooded buildings - red layer
        if not flooded.empty:
            folium.GeoJson(
                flooded[['geometry']].to_json(),
                name=f"Flooded Buildings ({len(flooded)})",
                style_function=lambda x: {
                    "fillColor": "#FF0000",
                    "color": "#FF0000",
                    "weight": 0.5,
                    "fillOpacity": 0.7
                }
            ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


def run_app():
    st.title("🌊 GeoFlood — Dehradun Flood Intelligence System")
    st.markdown("Real-time flood **detection** & **prediction** using Sentinel-2 NDWI + Open-Meteo")

    with st.spinner("Fetching live rainfall..."):
        rainfall_data = cached_rainfall()

    render_rainfall_dashboard(rainfall_data)
    st.divider()

    mode = st.radio(
        "Select Mode",
        ["🛰️ Post-Flood Detection", "🔮 Pre-Flood Prediction"],
        horizontal=True
    )

    st.divider()

    # ── POST FLOOD ────────────────────────────────────────
    if mode == "🛰️ Post-Flood Detection":
        st.subheader("🛰️ Post-Flood Detection")
        st.info("Reads **Dehradun_NDWI.tif** → finds flooded buildings")

        if st.button("🔍 Detect Flooded Buildings", type="primary"):

            with st.spinner("Loading satellite image + buildings (first time: ~1 min)..."):
                flood_gdf, bounds, buildings_gdf, status = cached_buildings_post()

            if buildings_gdf is None:
                st.error(f"Error: {status}")
                return

            with st.spinner("Analysing flood intersections..."):
                result, stats = intersect_buildings_with_flood(buildings_gdf, flood_gdf)

            flood_stats = get_flood_statistics(flood_gdf)
            st.success("✅ Detection complete!")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Buildings", stats["total_buildings"])
            col2.metric("🔴 Flooded", stats["flooded_buildings"])
            col3.metric("🟢 Safe", stats["safe_buildings"])
            col4.metric("Flood Area", f"{flood_stats.get('total_flood_area_km2', 0)} km²")

            with st.spinner("Rendering map..."):
                m = build_fast_map(result, flood_gdf, flood_col="is_flooded")
                st_folium(m, width=1400, height=600, returned_objects=[])
            show_streamlit_legend("post")        # ← legend appears below map

            report_df = pd.DataFrame({
                "building_id": result["building_id"],
                "is_flooded": result["is_flooded"],
                "geometry": result["geometry"].astype(str)
            })
            st.download_button(
                "📥 Download Report CSV",
                report_df.to_csv(index=False),
                file_name="flood_detection_report.csv",
                mime="text/csv"
            )

    # ── PRE FLOOD ─────────────────────────────────────────
    elif mode == "🔮 Pre-Flood Prediction":
        st.subheader("🔮 Pre-Flood Prediction")
        st.info("Uses live rainfall + river corridors to predict at-risk buildings")

        col1, col2 = st.columns(2)
        with col1:
            use_live = st.checkbox("Use Live Rainfall Data", value=True)
            if use_live:
                rainfall_input = rainfall_data["current_intensity_mm_hr"]
                st.metric("Live Intensity", f"{rainfall_input} mm/hr")
            else:
                rainfall_input = st.slider(
                    "Rainfall Intensity (mm/hr)",
                    min_value=0.0, max_value=100.0,
                    value=25.0, step=0.5
                )
        with col2:
            duration = st.slider(
                "Rainfall Duration (hours)",
                min_value=1, max_value=72, value=6
            )

        if st.button("🔮 Run Prediction", type="primary"):

            with st.spinner("Fetching buildings (first time: ~1 min)..."):
                buildings_gdf, b_status = cached_buildings_pre()

            if buildings_gdf is None:
                st.error(f"Buildings error: {b_status}")
                return

            with st.spinner("Running prediction model..."):
                result, flood_zones = predict_flood_buildings(
                    rainfall_input, duration, buildings_gdf
                )

            if result is not None:
                at_risk = int(result['flood_risk'].sum())
                total = len(result)
                safe = total - at_risk

                st.success("✅ Prediction complete!")

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Buildings", total)
                col2.metric("🔴 At Risk", at_risk,
                            delta=f"{round(at_risk/total*100,1)}%")
                col3.metric("🟢 Safe", safe)

                with st.spinner("Rendering map..."):
                    m = build_fast_map(result, flood_zones, flood_col="flood_risk")
                    st_folium(m, width=1400, height=600, returned_objects=[])
                show_streamlit_legend("pre")     # ← legend appears below map

                report_df = pd.DataFrame({
                    "building_id": result["building_id"],
                    "flood_risk": result["flood_risk"],
                    "risk_label": result["risk_label"],
                    "geometry": result["geometry"].astype(str)
                })
                st.download_button(
                    "📥 Download Prediction CSV",
                    report_df.to_csv(index=False),
                    file_name="flood_prediction_report.csv",
                    mime="text/csv"
                )


if __name__ == "__main__":
    run_app()