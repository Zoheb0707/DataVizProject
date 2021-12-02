# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:02:02 2021

@author: dcruz
"""
#%%
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import shapefile

flood_zip = pd.read_csv("flood_risk_data.csv")
zipcolnames = ['country', 'zipcode', 'place_name', 'state_name', 'state_abbr', 'region', 'region_code', 'region2', 'region2_code', 'latitude', 'longitude', 'accuracy_code']
zipcode_data = pd.read_csv("zipcode_data.txt", sep = "\t", header = None)
zipcode_data = zipcode_data.rename(columns = dict(zip(zipcode_data.columns, zipcolnames)))
census_colnames = ["name", "total_population"]
census_zipdata = pd.read_csv("census_zipcode_info.csv", header = 2).iloc[:,1:3]
census_zipdata = census_zipdata.rename(columns = dict(zip(census_zipdata.columns, census_colnames)))
census_zipdata["zipcode"] = census_zipdata.name.str.split().apply(lambda x : x[1]).astype('int64')
flood_data = (flood_zip.merge(zipcode_data, on = "zipcode")
                  .merge(census_zipdata, on = "zipcode")
                  .sort_values(by = 'total_population', ascending=False))
def get_usda_region(state_abbr):
    if state_abbr in ['ME', 'NH', 'VT', 'MA', 'CT', 'NJ', 'NY', 'PA', 'VA', 'WV', 'MD', 'DE', 'RI', 'DC']:
        return "Northeast"
    elif state_abbr in ['AR', 'LA', 'MS', 'TN', 'AL', 'GA', 'FL', 'SC', 'NC']:
        return "Southeast"
    elif state_abbr in ['MI', 'WI', 'MN', 'MO', 'IA', 'KY', 'IN', 'OH', 'IL']:
        return "Midwest"
    elif state_abbr in ['TX', 'OK', 'NM', 'KS', 'CO', 'NE', 'SD', 'ND', 'MT', 'WY']:
        return "Plains"
    elif state_abbr=="PR":
        return "Puerto Rico"
    elif state_abbr in ['AZ', 'UT', 'NV', 'CA', 'ID', 'OR', 'WA', 'AK', 'HI']:
        return "Pacific West"
    else:
        return "Other"
flood_data['usda_region'] = flood_data.state_abbr.map(get_usda_region)
#%%
shapefilepath = 'shapefiles/cb_2018_us_zcta510_500k.shp'
sf = shapefile.Reader(shapefilepath)
records = sf.records()
fields = [x[0] for x in sf.fields][1:]
shps = [s.points for s in sf.shapes()]

shapefile_dataframe = pd.DataFrame(columns=fields, data=records)
shapefile_dataframe = shapefile_dataframe.assign(coords=shps)

shapefile_dataframe['zipcode'] = shapefile_dataframe.ZCTA5CE10.astype('int')
shapefile_dataframe['pct_water'] = shapefile_dataframe.AWATER10 / (shapefile_dataframe.ALAND10 + shapefile_dataframe.AWATER10)

flood_data = shapefile_dataframe.merge(flood_data, on = 'zipcode')
#just using land area for pop density. Convert from m^2 to km^2 
flood_data['pop_density'] = 10**6 * flood_data.total_population/flood_data['ALAND10']
earthquake_risk = pd.read_csv('earthquake_risk_zipcode.csv')
risk_data = flood_data.merge(earthquake_risk, how = 'left', left_on = 'zipcode', right_on = 'zip')
#%%
wildfire_risk = pd.read_csv("wildfire_risk_data.csv")
risk_data = risk_data.merge(wildfire_risk, how = 'left', left_on = 'zipcode', right_on = 'ZIP')
#%%
wildfire_risk_metric = np.log(risk_data['WHP Continuous Mean']+0.1)
wildfire_risk_metric= scale(wildfire_risk_metric)
#%%
#'pct_fs_risk|itude|pct_water|pop_density|mmi'
#create a single flood risk metric
flood_risk_data = risk_data.loc[:, risk_data.columns.str.contains('pct_fs_risk')]
flood_risk_data = scale(np.log(flood_risk_data+0.1))
flood_risk_metric = PCA(n_components = 1).fit(flood_risk_data).transform(flood_risk_data)
#create a single earthquake risk metric
earthquake_risk_data = scale(risk_data.loc[:, risk_data.columns.str.contains('mmi')])
earthquake_risk_metric = PCA(n_components = 1).fit(earthquake_risk_data).transform(earthquake_risk_data)

normalized_long = scale(risk_data.longitude)

normalized_lat = scale(risk_data.latitude)

normalized_log_density = scale(np.log(risk_data.pop_density+0.1))

cluster_data = pd.DataFrame.from_dict({'log_flood_risk':flood_risk_metric[:, 0], 
                                       'log_fire_risk' : wildfire_risk_metric,
                                       'quake_risk':earthquake_risk_metric[:, 0],
                                       #'lat':normalized_lat,
                                       #'long':normalized_long,
                                       'log_density':normalized_log_density
                                       })

#%% impute wildfire risk for missing zip codes
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors = 5, weights = "uniform")
cluster_matrix_imputed = imputer.fit_transform(cluster_data)

#3 components gets ~97%, 4 gets ~99%
#PCAfitter = PCA(n_components = 3)
#test = PCAfitter.fit(cluster_data)
#reduced_data = PCAfitter.transform(cluster_data)
#%%
# k_df = pd.DataFrame({"k":[], "score":[], "min_size":[]})
# for k in range(5,76,5):
#     clusterModel = KMeans(n_clusters = k)
#     clusterModel.fit(reduced_data)
    
#     smallest_cluster_size = pd.Series(clusterModel.labels_).value_counts().min()
#     score = clusterModel.inertia_
#     result = pd.DataFrame({"k":[k], "score":[score], "min_size":[smallest_cluster_size]})
#     k_df = k_df.append(result)
#     print("For {} clusters, smallest cluster = {} leaves".format(k, smallest_cluster_size))
# k_df.plot.line(x='k', y = 'score')
#%%
clusterModel = KMeans(n_clusters = 30)
clusterModel.fit(cluster_matrix_imputed)
risk_data["cluster_label"] = clusterModel.labels_

cluster_groupby = (risk_data.loc[:, risk_data.columns.str.contains('avg_risk_score_all|cluster', regex=True)]
                            .groupby("cluster_label"))

highest_risk_cluster = cluster_groupby.mean().sort_values(by = "avg_risk_score_all", ascending = False).index[0]
lowest_risk_cluster = cluster_groupby.mean().sort_values(by = "avg_risk_score_all", ascending = False).index[-1]


highest_risk_zips = risk_data.loc[risk_data.cluster_label==highest_risk_cluster, :]
lowest_risk_zips = risk_data.loc[risk_data.cluster_label==lowest_risk_cluster, :]
highest_risk_zips = risk_data.loc[risk_data.cluster_label == highest_risk_cluster, :]
#%%
my_zipcode = 10010

my_cluster = risk_data.loc[risk_data.zipcode==my_zipcode, :].cluster_label.iloc[0]
similar_zips = risk_data.loc[risk_data.cluster_label==my_cluster, :]
print(similar_zips.usda_region.value_counts(normalize=True))

#%%
risk_data.rename(columns = {'coords':'geometry'}, inplace=True)
risk_data = risk_data.loc[:, risk_data.columns.str.contains("zipcode|place_name|state_name|pct_fs_risk|WHP|mmi|region|total_population|pop_density|cluster_label|itude|count_property", regex = True)]
risk_data['Log Flood Risk'] = cluster_data.log_flood_risk
risk_data['Log Fire Risk'] = cluster_data.log_fire_risk
risk_data['Quake Risk'] = cluster_data.quake_risk
risk_data['Log Population Density'] = cluster_data.log_density

risk_data.to_csv('flood_earthquake_wildfire_data_clustered.csv')

#%%
import matplotlib.pyplot as plt
threedee = plt.figure(figsize = (20,15)).gca(projection='3d')
threedee.scatter(cluster_data.iloc[:,0], cluster_data.iloc[:,1], cluster_data.iloc[:, 2], c = risk_data.cluster_label)
plt.show()
