# 🌊 GeoFlood — Dehradun Flood Intelligence System

Real-time flood detection and prediction for Dehradun using:
- **Sentinel-2 NDWI** satellite image (Dehradun_NDWI.tif)
- **Open-Meteo API** for live rainfall (no API key needed)
- **OpenStreetMap** buildings via osmnx

## Folder Structure
GeoFlood/
├── data/
│   └── Dehradun_NDWI.tif   ← Sentinel-2 NDWI satellite image
├── src/
│   ├── gui/app.py           ← Main Streamlit UI
│   └── logic/               ← All processing logic
├── main.py
└── requirements.txt

## Setup & Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the app
python -m streamlit run main.py

## Modes
- **Post-Flood Detection** → reads NDWI TIF, finds flooded buildings on map
- **Pre-Flood Prediction** → uses live rainfall to predict at-risk buildings