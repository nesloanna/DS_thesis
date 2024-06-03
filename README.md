# Exploration of Ocean Biodiversity Data

### Link to the [Tara Oceans Dashboard](https://tara-dash-2024.nw.r.appspot.com/)

<a href="https://tara-dash-2024.nw.r.appspot.com/"><img src="https://github.com/nesloanna/DS_thesis/blob/main/Dashboard/Dash.jpeg" width="80%"/></a>

## Code used in the thesis
### Ocean Data

* `tara_load_data.py` → Load *Tara* datasets into CSV files
* `tara_preprocess_data.py` → Preprocess data (merge, clean, remove duplicates) 


### Marine Heatwaves

* `marineHeatWaves.py` → *[marineHeatWaves](https://github.com/ecjoliver/marineHeatWaves)* module (required for MHWs detecting)
* `NOAA_data.ipynb` → Prepare NOAA data (match to closest *Tara* locations) 
* `detect_mhws_tara.ipynb` → Detect Marine Heatwaves (MHWs) at *Tara* locations
* `mhws_Tara_2009-13.ipynb` → MHWs (2009-2013) 30 days before *Tara* samplings 



### Tara Oceans Dashboard

* `dashboard.py` → Build the dashboard
* `custom.css` → Custom stylesheet for the dashboard


### Machine Learning
* `classifier_count.ipynb` → Decision tree classification (MHW occurence and counts)
* `classifier_categories.ipynb` → Decision tree classification (MHW categories)


### Link to [Tara Oceans Dashboard](https://tara-dash-2024.nw.r.appspot.com/)
