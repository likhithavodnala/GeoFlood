# GeoFlood

## Flood Detection and Building Impact Assessment Using Satellite Imagery

GeoFlood is a geospatial web application developed for flood detection, building impact assessment, and pre-flood risk prediction.

The application combines satellite imagery, live rainfall information, building data, geospatial analysis, and interactive GIS visualization to provide an understanding of flood impact on buildings.

The project focuses on Dehradun, Uttarakhand, India.

GeoFlood provides two main modes of analysis:

1. Post-Flood Detection
2. Pre-Flood Prediction

---

## Project Overview

Flood events can affect buildings and settlements within a short period of time. Identifying the affected area and understanding the impact on buildings are important for rapid flood assessment.

GeoFlood provides an interactive platform to:

- Detect potential flood-affected areas using satellite imagery
- Identify buildings located within flood-affected areas
- Assess potential building impact
- Use live rainfall information for pre-flood risk assessment
- Analyse rainfall intensity and duration
- Visualize flood zones and buildings on an interactive map
- Provide building and flood-area statistics
- Generate downloadable analysis results

---

## Objectives

The main objectives of GeoFlood are:

- Detect potential flood-affected areas using satellite imagery
- Identify buildings affected by the detected flood zone
- Assess the potential impact of flooding on buildings
- Use live rainfall information for pre-flood risk assessment
- Analyse rainfall intensity and duration
- Provide building-level spatial visualization
- Display flood zones and building risk on an interactive map
- Provide statistical summaries and downloadable results
- Support rapid geospatial assessment of flood-related risks

---

## Application Modes

### 1. Post-Flood Detection

The Post-Flood Detection mode is used to identify potential flood-affected areas after a flood event.

The application uses a pre-loaded Sentinel-2 satellite TIFF available within the project.

The user does not need to select or upload satellite imagery.

The satellite data is processed to identify the potential flood zone. Building information is then compared with the detected flood zone to identify flooded and safe buildings.

#### Workflow

```text
Pre-loaded Sentinel-2 Satellite TIFF
                 |
                 v
       Satellite Data Processing
                 |
                 v
          Flood Detection
                 |
                 v
             Flood Zone
                 |
                 v
       Building Information
                 |
                 v
          Spatial Analysis
                 |
          +------+------+
          |             |
          v             v
   Flooded Buildings  Safe Buildings
          |             |
          +------+------+
                 |
                 v
        Interactive GIS Map
                 |
                 v
          Statistics and CSV
```

#### Post-Flood Outputs

- Total number of buildings
- Flooded buildings
- Safe buildings
- Flood area
- Detected flood zone
- Building-level visualization
- Interactive GIS map
- Downloadable CSV report

---

### 2. Pre-Flood Prediction

The Pre-Flood Prediction mode is designed to assess potential building risk before a flood occurs.

The application uses live rainfall data for Dehradun and provides information about current rainfall conditions.

The rainfall section provides:

- Current rainfall intensity
- Rainfall during the last 24 hours
- IMD rainfall classification
- Rainfall trend
- Last updated information

Rainfall duration can also be considered during the prediction process.

The rainfall intensity is used to assess potential building risk and visualize a predicted flood zone.

#### Workflow

```text
Live Rainfall Data
        |
        v
Current Rainfall Intensity
        |
        v
Rainfall Duration
        |
        v
Pre-Flood Risk Assessment
        |
   +----+----+
   |         |
   v         v
At-Risk    Safe
Buildings  Buildings
        |
        v
Predicted Flood Zone
        |
        v
Interactive GIS Map
        |
        v
Statistics and CSV
```

#### Pre-Flood Outputs

- Live rainfall information
- Current rainfall intensity
- Last 24-hour rainfall
- IMD rainfall classification
- Rainfall trend visualization
- Total number of buildings
- At-risk buildings
- Safe buildings
- Percentage of buildings at risk
- Predicted flood zone
- Interactive GIS map
- Downloadable prediction CSV

---

## System Architecture

```text
                         GeoFlood
                            |
             +--------------+--------------+
             |                             |
             v                             v
      POST-FLOOD MODE               PRE-FLOOD MODE
             |                             |
             v                             v
   Pre-loaded Sentinel-2            Live Rainfall Data
       Satellite Data                      |
             |                             v
             v                    Rainfall Intensity
      Flood Detection                      |
             |                             v
             v                    Rainfall Assessment
        Flood Zone                         |
             |                             v
             v                      Risk Assessment
   Building Information                    |
             |                             v
             v                      At-Risk Buildings
    Spatial Analysis                       |
             |                             v
             v                       Safe Buildings
  Flooded and Safe Buildings               |
             |                             |
             +--------------+--------------+
                            |
                            v
                   Interactive GIS Map
                            |
                            v
                       Statistics
                            |
                            v
                    Downloadable CSV
```

---

## Project Workflow

The overall workflow of GeoFlood is:

```text
                    Input Data
                        |
          +-------------+-------------+
          |                           |
          v                           v
   Satellite Data              Live Rainfall Data
          |                           |
          v                           v
   Flood Detection            Rainfall Intensity
          |                           |
          v                           v
      Flood Zone               Risk Assessment
          |                           |
          v                           v
 Building Information          At-Risk Buildings
          |                           |
          v                           v
   Spatial Analysis             Safe Buildings
          |                           |
          +-------------+-------------+
                        |
                        v
               Interactive GIS Map
                        |
                        v
                  Results and Charts
                        |
                        v
                  Downloadable CSV
```

---

## Satellite Data and Flood Detection

GeoFlood uses Sentinel-2 satellite imagery for the post-flood detection component.

A pre-loaded Sentinel-2 GeoTIFF is available within the project. The application processes the satellite information to identify potential water or flood-affected areas.

A water-related spectral index is used to help identify areas containing water. The detected flood area is then represented as a geographical flood zone.

The flood zone is compared with building footprints to determine which buildings are located within the identified flood area.

---

## Building Impact Assessment

Building footprint information is obtained from OpenStreetMap.

The application compares building locations with the detected flood zone through spatial analysis.

Based on the relationship between buildings and the flood zone, the application identifies:

- Flooded buildings
- Safe buildings
- Building-level flood impact
- Percentage of affected buildings
- Spatial distribution of affected buildings

---

## Live Rainfall Analysis

The Pre-Flood Prediction mode uses live rainfall information for Dehradun.

The application provides:

- Current rainfall intensity
- Rainfall during the last 24 hours
- IMD rainfall classification
- Rainfall trend
- Last updated information

The rainfall intensity and rainfall duration are used for the pre-flood risk assessment.

The results are presented through at-risk buildings, safe buildings, and a predicted flood zone.

---

## Interactive GIS Visualization

GeoFlood provides an interactive GIS map for visualizing the analysis results.

### Post-Flood Detection Map

The map displays:

- Flooded Buildings
- Safe Buildings
- Flood Zone detected from satellite data

### Pre-Flood Prediction Map

The map displays:

- At-Risk Buildings
- Safe Buildings
- Predicted Flood Zone

The interactive map allows users to explore the spatial distribution of buildings and flood zones.

---

## Results

GeoFlood provides numerical summaries together with map-based visualization.

### Example Post-Flood Detection Result

```text
Total Buildings : 7349
Flooded         : 12
Safe            : 7337
Flood Area      : 0.023 km²
```

### Example Pre-Flood Prediction Result

```text
Total Buildings : 14147
At Risk         : 5842
Safe            : 8305
At Risk         : 41.3%
```

These are example results from the application interface. Results may vary depending on the available data and analysis conditions.

---

## Technologies Used

- Python
- Streamlit
- GeoPandas
- Rasterio
- Folium
- Shapely
- OpenCV
- NumPy
- Matplotlib
- OpenStreetMap
- Overpass API
- Open-Meteo

---

## Project Structure

```text
GeoFlood/
|
+-- data/
|   +-- Dehradun_NDWI.tif
|
+-- src/
|   +-- gui/
|       +-- app.py
|
+-- .devcontainer/
|
+-- .streamlit/
|
+-- .gitignore
+-- main.py
+-- requirements.txt
+-- README.md
```

### Important Files and Folders

| File or Folder | Purpose |
|---|---|
| `data/` | Contains satellite data used by the application |
| `Dehradun_NDWI.tif` | Pre-loaded satellite data used for flood detection |
| `src/gui/app.py` | Main Streamlit application |
| `.streamlit/` | Streamlit application configuration |
| `.devcontainer/` | Development environment configuration |
| `requirements.txt` | Required Python packages |
| `main.py` | Project entry point |
| `README.md` | Project documentation |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/likhithavodnala/GeoFlood.git
```

### 2. Navigate to the Project

```bash
cd GeoFlood
```

### 3. Create a Virtual Environment

```bash
python -m venv venv311
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv311\Scripts\activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## How to Run

Run the Streamlit application using:

```bash
python -m streamlit run src\gui\app.py
```

The application will open in a web browser.

---

## Downloadable Results

GeoFlood provides downloadable CSV results from the application.

### Post-Flood Detection

The application provides a Flood Detection CSV Report containing building-level analysis results.

### Pre-Flood Prediction

The application provides a Prediction CSV Report containing pre-flood building risk results.

---

## Limitations

- The post-flood detection process depends on the available satellite imagery.
- Building-level assessment depends on the availability and coverage of OpenStreetMap building footprints.
- Live rainfall and building information depend on network and external data-service availability.
- Satellite-based flood detection represents the conditions captured by the available imagery.
- The pre-flood mode provides a potential risk assessment and should not be considered a complete operational flood forecasting system.
- GeoFlood is designed as a geospatial assessment and visualization tool rather than a replacement for professional flood modelling systems.

---

## Future Scope

The project can be further enhanced through the following developments.

### Real-Time Satellite Data

Integrate updated Sentinel-2 satellite imagery through satellite data services to support more timely flood detection.

### Historical Flood Analysis

Incorporate historical flood information to understand previous flood events and identify areas with recurring flood exposure.

### Improved Building Impact Assessment

Include additional building information such as construction type, number of floors, distance from rivers, and other building characteristics to provide a more detailed assessment.

### AI and Machine Learning-Based Risk Assessment

Explore machine learning approaches for more advanced flood-risk and building-impact assessment.

### Improved Rainfall-Based Prediction

Combine rainfall information with additional environmental and geographical factors to improve pre-flood risk assessment.

### 3D Building and Flood Visualization

Develop 3D visualization of buildings and flood zones to provide a clearer visual understanding of flood impact.

The 3D visualization could help understand:

- How much of an individual building may be affected
- The extent of floodwater around buildings
- How nearby buildings may be affected
- The relationship between buildings and surrounding flood zones

### Mobile and Field Applications

Develop a mobile-friendly version and offline capabilities to support field-based disaster assessment.

### Advanced Disaster Risk Assessment

Integrate additional environmental, geographical, infrastructure, and building information to develop a more comprehensive disaster-risk assessment system.

---

## My Contribution

### Geospatial Data Processing and Spatial Visualization

- Prepared and processed geospatial and satellite data.
- Performed spatial analysis for building impact assessment.
- Worked on data cleaning and coordinate-system handling.
- Developed building risk classification based on flood-area overlap.
- Designed the Streamlit application interface.
- Developed interactive GIS map visualization using Folium.
- Implemented map layers and interactive controls.
- Created statistical summaries and visualizations.

---

## Team

Dinesh  
Gayatri  
Likhitha Vodnala

---

## Author

### Likhitha Vodnala

MSc Agriculture Analytics

Areas of Interest:

- Geospatial Analysis
- GIS and Remote Sensing
- Data Analytics
- Data Science
- Artificial Intelligence and Machine Learning
- Geospatial Data Science

GitHub:

https://github.com/likhithavodnala

---

## Project Information

| Category | Details |
|---|---|
| Project Name | GeoFlood |
| Project Type | Geospatial Web Application |
| Domain | GIS and Disaster Management |
| Study Area | Dehradun, Uttarakhand, India |
| Satellite Data | Sentinel-2 |
| Building Data | OpenStreetMap |
| Rainfall Data | Live rainfall information |
| Application Framework | Streamlit |
| Map Visualization | Folium |
| Programming Language | Python |

---

## Project Summary

GeoFlood combines satellite-based flood detection, live rainfall analysis, building-level spatial assessment, and interactive GIS visualization to provide a practical platform for understanding flood impact and potential building risk.
