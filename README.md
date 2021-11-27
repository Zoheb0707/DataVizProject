# Package Description

This package contains csv datasets for flood, fire, and earthquake risks at the zipcode level. These datasets are combined together by grouping them together over the zip code to create a single csv containing all disaster data. 
The disaster risk datasets are grouped in clusters based on similar zipcodes. It also contains a dataset for disaster mitigation actions and results for each zipcode.

The risk_clustering_v2.py file is responsible for clustering the zip codes based on disaster data similarity.

The mitigation_analysis.ipynb jupyter notebook is responsible for cleaning the disaster and mitigation datasets, grouping them over zipcodes and then creating the following visualization files:
1. flood_earthquake_cluster_data.csv: contains risk data for each zip code
2. mitigation_data.csv: contains mitigitation data for each zip code
3. aggregate_cluster_data.csv: contains risk data for each cluster
4. zipcode_cluster_data.csv: maps each zipcode to a cluster
5. mitigion_and_cluster_aggregate_data.csv: mitigation data for each cluster

The file also contains helper functions that help with visualization.

Lastly we have the tableau files responsible for the visualization. They contain the choropleth map that help explore risk and mitigation data among zip codes and facilitates comparisons across similar zip codes.

# Installation and Execution

1. Visit the following github repository: https://github.com/Zoheb0707/DataVizProject
2. Please click the fork button on the top left corner to fork the repository.
3. Use the `git clone` command to pull the package into your local machine.
4. The risk_clustering_v2.py can be run in any python editor that supports python 3.7.
5. The mitigation_analysis.ipynb can be run in iny JupyterHub server that supports a python 3.7 kernel.
5. TODO: tableau viz.

