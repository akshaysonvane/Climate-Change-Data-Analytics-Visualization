# Climate-Change-Data-Analytics-Visualization
Analyzed and visualized earth surface temperature data provided by Berkeley Earth

### Dataset: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data/

## Features
1. Regression
    - Temperature prediction and visualization for a specific country, city, month and years using Linear Regression.
    - Temperature prediction for a specific year using multiple regression techniques like
      1. Linear regression
      2. Isotonic regression
      3. Bayesian Ridge
      4. RANSAC
      5. Gaussian Process
      6. SVR
2. Clustering
    - Classified earth surface temperature into 3 clusters of hot, mild and cold.
    - Generated a google map with showing the clusters for a specific year.
    ![Clustering](/project/GlobalCluster.png?raw=true "Clustering")
    - Model can predict temperature class of any given latitude and longitude for any year and month.
3. Visualization
    - Earth surface mean temperature rise curve from year 1750.
    ![Temperature](/project/temperature.png?raw=true "Temperature")
    - Divided a year in 4 seasons and visualized the average temperature of major cities in India.
    ![Seasons](/project/seasons.png?raw=true "Seasons")
    - Visualized earth surface average temperature using world map.
    ![Avg temp](/project/GlobalAvgTemp.png?raw=true "Avg temp")

## Technology Stack
- Python Flask
- Spark
- Scikit
- AngularJs
- Google Maps
- Google Charts
- Plotly Js
- Matplotlib
