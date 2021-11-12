import pandas as pd 

dataframe = pd.read_csv("earthquake_risk_lat_lon.csv")

top = 49.3457868 # north lat
left = -124.7844079 # west long
right = -66.9513812 # east long
bottom =  24.7433195 # south lat

def filter_for_us(dataframe):
	in_us = (dataframe["lat"] >= bottom) & (dataframe["lat"] <= top) & (dataframe["lon"] >= left) & (dataframe["lon"] <= right)
	return dataframe[in_us]

us_rows = filter_for_us(dataframe)

us_rows.to_csv("earthquake_risk_lat_lon_us.csv", encoding='utf-8', index=False)
