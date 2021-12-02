# Package Description

This package contains Team 57's project - a tool to visualize the risk of different types of natural disasters across the US, as well as provide information on what mitigation actions are being taken for regions with similar risk profiles. It contains csv datasets for flood, fire, and earthquake risks at the zipcode level (earthquake risk had to be resolved from coordinates to zipcodes using earthquake_lat_lon_to_zip.sql). These datasets are combined together by zip code to create a single csv containing all disaster risks. The disaster risk datasets are grouped in clusters based on similar zipcodes. It also contains a dataset for disaster mitigation actions and results for each zipcode.

The risk_clustering_v2.py file is responsible for merging the different risk models and clustering the zip codes based on disaster risk characteristics.

The mitigation_analysis.ipynb jupyter notebook is responsible for cleaning the disaster and mitigation datasets, grouping them over zipcodes and then creating the following visualization files:
1. flood_earthquake_wildfire_data_clustered.csv: contains risk data for each zip code
2. mitigation_data.csv: contains mitigitation data for each zip code
3. mitigation_and_risk_data.csv: contains mitigation data, risk data and cluster information for each zipcode
4. zipcode_cluster_data.csv: maps each zipcode to a cluster

The file also contains examples of graphs and key metrics that could be used for visualization.

Lastly we have a tableau workbook responsible for the visualization ("Natural Disaster Risk Visualization_112921.twbx"). It contains two dashboards that help explore risk and mitigation data among zip codes and facilitates comparisons across similar zip codes:
1. Natural Disaster Risk: This dashboard contains a choropleth map and tables/charts that display the risk and mitigation data of the selected zip codes. By default all zip codes across the US are selected. There are filters at the right of the dashboard to change which zip codes are selected, along with a dropdown menu to change the risk type that is displayed. There is a search bar at the top left of the choropleth map that can be used to zoom the map into specific regions (city, county, state, etc.). Upon selecting a zip code by clicking, there is a link displayed in the tooltip titled "View data by cluster" that will take you to the second dashboard described below.
2. Risk Profiles by Cluster: This dashboard contains a choropleth map and tables/charts that display the risk and mitigation data of the cluster linked from the first dashboard. Users can observe the mitigation actions taken amongst the selected cluster and make inferences on which were most popular or beneficial.

# Installation
1. Ensure Tableau Desktop is installed and licensed on your computer
2. Download and run the "Natural Disaster Risk Visualization_112921.twbx" file

# Execution
1. Change the type of disaster risk to visualize in the upper right hand corner (Flood, Earthquake, Wildfire)
2. Zoom and pan around the map and select a zip code of interest
3. In the tooltip that pops up near the selected zip code, click the link titled "View Data by Cluster." This will bring you to the second report
4. In the second report, observe the cluster your selected zip code belongs to, and the mitigation actions taken in that cluster
5. If desired, use the Tableau features available to modify or change the visualizations. 
