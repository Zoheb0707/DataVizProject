import pandas as pd


dataframe = pd.read_csv("zipcode_data.txt",sep='\t', header=None)

print(dataframe.head(5))
zip_lat_lon_df = dataframe[[1, 9, 10]]
zip_lat_lon_df.rename(columns={"1": "zip_code", "9": "lat", "10": "lon"})
print(zip_lat_lon_df.head(5))
zip_lat_lon_df.to_csv("zipcode_lat_lon.csv", encoding='utf-8', index=False)
