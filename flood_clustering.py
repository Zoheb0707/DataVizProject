# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:02:02 2021

@author: dcruz
"""
#%%
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import shapefile

flood_zip = pd.read_csv("Flood Risk/01_DATA/Climate_Risk_Statistics/v1.3/Zip_level_risk_FEMA_FSF_v1.3.csv")
zipcolnames = ['country', 'zipcode', 'place_name', 'state_name', 'state_abbr', 'region', 'region_code', 'region2', 'region2_code', 'latitude', 'longitude', 'accuracy_code']
zipcode_data = pd.read_csv("Zipcodes/zipcode_data.txt", sep = "\t", header = None)
zipcode_data = zipcode_data.rename(columns = dict(zip(zipcode_data.columns, zipcolnames)))
census_colnames = ["name", "total_population"]
census_zipdata = pd.read_csv("Zipcodes/census_zipcode_info.csv", header = 2).iloc[:,1:3]
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
shapefilepath = 'Zipcodes/shapefiles/cb_2018_us_zcta510_500k.shp'
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
#%%
cluster_data = pd.concat([flood_data.loc[:, flood_data.columns.str.contains('pct_fs_risk|itude|pct_water|pop_density', regex=True)], pd.get_dummies(flood_data.usda_region)], axis = 1)
    

normalized_data = normalize(cluster_data)

#3 components gets ~97%, 4 gets ~99%
PCAfitter = PCA(n_components = 3)
test = PCAfitter.fit(normalized_data)
reduced_data = PCAfitter.transform(normalized_data)
# k_df = pd.DataFrame({"k":[], "score":[], "min_size":[]})
# for k in range(5,76,5):
#     clusterModel = KMeans(n_clusters = k)
#     clusterModel.fit(reduced_data)
    
#     smallest_cluster_size = pd.Series(clusterModel.labels_).value_counts().min()
#     score = clusterModel.inertia_
#     result = pd.DataFrame({"k":[k], "score":[score], "min_size":[smallest_cluster_size]})
#     k_df = k_df.append(result)
#     print("For {} clusters, smallest cluster = {} leaves".format(k, smallest_cluster_size))

clusterModel = KMeans(n_clusters = 40)
clusterModel.fit(reduced_data)
flood_data["cluster_label"] = clusterModel.labels_

cluster_groupby = (flood_data.loc[:, flood_data.columns.str.contains('avg_risk_score_all|cluster', regex=True)]
                            .groupby("cluster_label"))

highest_risk_cluster = cluster_groupby.mean().sort_values(by = "avg_risk_score_all", ascending = False).index[0]
lowest_risk_cluster = cluster_groupby.mean().sort_values(by = "avg_risk_score_all", ascending = False).index[-1]


highest_risk_zips = flood_data.loc[flood_data.cluster_label==highest_risk_cluster, :]
lowest_risk_zips = flood_data.loc[flood_data.cluster_label==lowest_risk_cluster, :]
highest_risk_zips = flood_data.loc[flood_data.cluster_label == highest_risk_cluster, :]
#%%
import matplotlib.pyplot as plt
threedee = plt.figure(figsize = (20,15)).gca(projection='3d')
threedee.scatter(reduced_data[:,0], reduced_data[:,1], reduced_data[:, 2], c = flood_data.cluster_label)
plt.show()

#%%
my_zipcode = 90210
flood_data.rename(columns = {'coords':'geometry'})
flood_data = flood_data.loc[:, flood_data.columns.str.contains("zipcode|geom|pct_fs_risk|place_name|state_name|region|total_population|pop_density|cluster_label|itude|count_property|pct_water", regex = True)]
my_cluster = flood_data.loc[flood_data.zipcode==my_zipcode, :].cluster_label.iloc[0]
similar_zips = flood_data.loc[flood_data.cluster_label==my_cluster, :]

