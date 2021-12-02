# Package Description

This package contains csv datasets for flood, fire, and earthquake risks at the zipcode level. These datasets are combined together by grouping them together over the zip code to create a single csv containing all disaster data. 

The disaster risk datasets are grouped in clusters based on similar zipcodes. It also contains a dataset for disaster mitigation actions and results for each zipcode.

The risk_clustering_v2.py file is responsible for clustering the zip codes based on disaster data similarity.

The mitigation_analysis.ipynb jupyter notebook is responsible for cleaning the disaster and mitigation datasets, grouping them over zipcodes and then creating the following visualization files:
1. flood_earthquake_wildfire_data_clustered.csv: contains risk data for each zip code
2. mitigation_data.csv: contains mitigitation data for each zip code
3. mitigation_and_risk_data.csv: contains mitigation data, risk data and cluster information for each zipcode
4. zipcode_cluster_data.csv: maps each zipcode to a cluster

The file also contains examples of graphs and key metrics that could be used for visualization.

Lastly we have a tableau workbook responsible for the visualization ("Natural Disaster Risk Visualization.twbx"). It contains two dashboards that help explore risk and mitigation data among zip codes and facilitates comparisons across similar zip codes:
1. Natural Disaster Risk: This dashboard contains a choropleth map and tables/charts that display the risk and mitigation data of the selected zip codes. By default all zip codes across the US are selected. There are filters at the right of the dashboard to change which zip codes are selected, along with a dropdown menu to change the risk type that is displayed. There is a search bar at the top left of the choropleth map that can be used to zoom the map into specific regions (city, county, state, etc.). Upon selecting a zip code by clicking, there is a link displayed in the tooltip titled "View regions with similar risk profiles" that will take you to the second dashboard described below.
2. Risk Profiles by Cluster: This dashboard contains a choropleth map and tables/charts that display the risk and mitigation data of the cluster linked from the first dashboard. Users can observe the mitigation actions taken amongst the selected cluster and make inferences on which were most popular or beneficial.

# Installation and Execution

1. Visit the following github repository: https://github.com/Zoheb0707/DataVizProject
2. Please click the fork button on the top left corner to fork the repository.
3. Use the `git clone` command to pull the package into your local machine.
4. The risk_clustering_v2.py file can be run in any python editor that supports python 3.7.
5. The mitigation_analysis.ipynb file can be run in iny JupyterHub server that supports a python 3.7 kernel.
5. The "Natural Disaster Risk Visualization_112921.twbx" file can be ran in Tableau Desktop.
