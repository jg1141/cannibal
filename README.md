# Store Cannibalization Analysis App

This Streamlit application helps visualize and analyze potential customer cannibalization when adding new store locations. It allows users to drop a pin on a map and see which existing stores might be affected by the new location.

## Features

- Interactive map with existing store locations
- Pin drop functionality to mark potential new store locations
- Automatic calculation of cannibalization areas
- Visual representation of affected stores
- Distance-based analysis

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. The app will open in your default web browser
2. Click on the map to place a pin for your new store location
3. The app will automatically calculate and display:
   - Which existing stores might be affected
   - The distance to each affected store
   - Visual circles showing the cannibalization areas
4. Use the "Clear Selection" button to reset the analysis

## Customization

You can modify the following parameters in the code:
- `EXISTING_STORES`: Add or modify existing store locations
- Cannibalization radius (currently set to 50 miles)
- Map center and zoom level
- Visual styling of markers and circles 