# ------ import dependancies: api key, data link, and pandas ------
from config import apiKey
import nasdaqdatalink
import pandas as pd
import matplotlib.pyplot as plt

# ------ Set up API Environment ------
# 1.) define api key
# 2.) configure the api key to work with the data link 
nasdaq_api = apiKey
nasdaqdatalink.ApiConfig.api_key = nasdaq_api

# ------ Create dataframe from entire data set -------
# 1.) create a database variable pointing to the data sourse (inflation rates)
# 2.) acess the metadata information for the data feilds (columns in the data source)
# 3.) Retrieve Datasets Available in the Database
# 4.) convert the 'ds' object to a list and create a dataframe from it
database = nasdaqdatalink.Database('RATEINF')
database.data_fields()
ds = database.datasets()
main_df = pd.DataFrame(ds.to_list())

# ------ create append 'regions' column to a new dat
# 1.) Create a list of table names by iterating through regions in the DataFrame
# 1.2.) and formatting them as "RATEINF/{region}"
# 2.) Sort the 'tables' list in ascending order
# 3.) display tables 
tables = [f"RATEINF/{region}" for region in main_df[1].to_list()]
tables.sort()
tables

# create two empty lists:
# Consumer Price Index and inflation 
data_cpi = []
data_inflation = []

# for loop to loop through the data, appending the df to the list
for region in tables: 
    temp_df = nasdaqdatalink.get(region, paginate=True)
    temp_df.columns = [region.split('/')[-1]]
    temp_df = temp_df.loc['2001-01-01':]
    if 'CPI' in region:
        data_cpi.append(temp_df)
    else:
        data_inflation.append(temp_df)

# Concatenate CPI data, sort the index, and forward-fill missing values for a clean time series.
# Then, create a plot with a specified figure size and subplots for better visualization.
pd.concat(data_cpi).sort_index().ffill().plot(figsize=(10, 8), subplots=True)

#--------- Create inflation rates graphs -------------
# 1.) Concatenate inflation rate data, ensuring proper time series alignment.
# 2.) Sort the index to maintain chronological order of data points.
# 3.) Forward-fill missing values to handle any gaps in the time series.
# 4.) Create a plot with a larger figure size (for better detail) and subplots (to separate data series).
pd.concat(data_inflation).sort_index().ffill().plot(figsize=(18, 16), subplots=True)