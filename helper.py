import numpy as np
import pandas as pd

continent_color_map = {
    'Europe': '#1f77b4',
    'Asia': '#ff7f0e',
    'Oceania': '#2ca02c',
    'Americas': '#d62728',
    'Africa': '#9467bd'
}

region_color_map = {
    'Europe': '#1f77b4',
    'Asia': '#ff7f0e',
    'Oceania': '#2ca02c',
    'Americas': '#d62728',
    'Africa': '#9467bd',
    'Northern Europe': '#1f77b4',
    'Eastern Europe': '#1f77b4',
    'Southern Europe': '#1f77b4',
    'Western Europe': '#1f77b4',
    'Eastern Asia': '#ff7f0e',
    'Central Asia': '#ff7f0e',
    'South-eastern Asia': '#ff7f0e',
    'Southern Asia': '#ff7f0e',
    'Western Asia': '#ff7f0e',
    'Australia and New Zealand': '#2ca02c',
    'Northern America': '#d62728',
    'Latin America and the Caribbean': '#d62728',
    'Northern Africa': '#9467bd',
    'Sub-Saharan Africa': '#9467bd',
}

# Import data
whr23 = pd.read_csv('data/WHR2023.csv')
world_data = pd.read_csv('data/world-data-2023.csv')
continent_file = pd.read_csv('data/continents2.csv')

# Data cleaning

# Merge the datasets
# Change column names to match the main dataset
continent_file.rename(columns={'name': 'Country name', 'alpha-2': 'country code'}, inplace=True)
column_order = ['Country name', 'region', 'sub-region', 'country code']

# Renaming countries to match the main dataset
whr23.loc[whr23['Country name'] == 'Congo (Kinshasa)', 'Country name'] = 'Congo (Democratic Republic Of The)'
whr23.loc[whr23['Country name'] == 'Congo (Brazzaville)', 'Country name'] = 'Congo'
whr23.loc[whr23['Country name'] == 'Turkiye', 'Country name'] = 'Turkey'
whr23.loc[whr23['Country name'] == 'Czechia', 'Country name'] = 'Czech Republic'
whr23.loc[whr23['Country name'] == 'Taiwan Province of China', 'Country name'] = 'Taiwan'
whr23.loc[whr23['Country name'] == 'Bosnia and Herzegovina', 'Country name'] = 'Bosnia And Herzegovina'
whr23.loc[whr23['Country name'] == 'Hong Kong S.A.R. of China', 'Country name'] = 'Hong Kong'
whr23.loc[whr23['Country name'] == 'North Macedonia', 'Country name'] = 'Macedonia'
whr23.loc[whr23['Country name'] == 'State of Palestine', 'Country name'] = 'Palestine, State of'
whr23.loc[whr23['Country name'] == 'Ivory Coast', 'Country name'] = 'Côte D\'Ivoire'

# Merge region and sub-region into whr23score after country name
merged_data = whr23.merge(continent_file[['Country name', 'region', 'sub-region', 'country code']], on='Country name')
column_order = ['Country name', 'region', 'sub-region', 'country code'] + [col for col in merged_data.columns if
                                                                           col not in column_order]
merged_data = merged_data[column_order]

# Rename the 'Country' column to 'Country name' in the extra_data DataFrame
world_data.rename(columns={'Country': 'Country name'}, inplace=True)

# Change names of countries to match the main dataset
merged_data.loc[merged_data['Country name'] == 'Ireland', 'Country name'] = 'Republic of Ireland'
merged_data.loc[merged_data['Country name'] == 'Bosnia And Herzegovina', 'Country name'] = 'Bosnia and Herzegovina'
merged_data.loc[merged_data['Country name'] == 'Congo', 'Country name'] = 'Republic of the Congo'
merged_data.loc[merged_data[
                    'Country name'] == 'Congo (Democratic Republic Of The)', 'Country name'] = 'Democratic Republic of the Congo'
merged_data.loc[merged_data['Country name'] == 'Macedonia', 'Country name'] = 'North Macedonia'
merged_data.loc[merged_data['Country name'] == 'Côte D\'Ivoire', 'Country name'] = 'Ivory Coast'
merged_data.loc[merged_data['Country name'] == 'Palestine, State of', 'Country name'] = 'Palestinian National Authority'
merged_data.loc[merged_data['Country name'] == 'Gambia', 'Country name'] = 'The Gambia'

# Change Unenployment rate to a float
world_data['Unemployment rate'] = world_data['Unemployment rate'].str.replace('%', '').astype(float)

# Merge the data for your own new dataset
full_data = merged_data.merge(
    world_data[['Country name', 'Unemployment rate', 'Urban_population', 'Population', 'Official language']],
    on='Country name')

# Now let's add our own math an calculate the percentage living in an urban area
full_data['Urban_population'] = full_data['Urban_population'].str.replace(',', '').astype(float)
full_data['Population'] = full_data['Population'].str.replace(',', '').astype(float)
full_data['Urban population percentage'] = (full_data['Urban_population'] / full_data['Population']) * 100
full_data['Continent'] = full_data['region']
full_data['Region'] = full_data['sub-region']
full_data['Happiness Score'] = full_data['Ladder score']
full_data.drop(['region', 'sub-region', 'Ladder score'], axis=1, inplace=True)

# Normalize the data
full_data["Normalized Logged GDP per capita"] = full_data["Logged GDP per capita"] / full_data["Logged GDP per capita"].max()
full_data["Normalized Social support"] = full_data["Social support"] / full_data["Social support"].max()
full_data["Normalized Healthy life expectancy"] = full_data["Healthy life expectancy"] / full_data["Healthy life expectancy"].max()
full_data["Normalized Freedom to make life choices"] = full_data["Freedom to make life choices"] / full_data["Freedom to make life choices"].max()
full_data["Normalized Happiness Score"] = full_data["Happiness Score"] / full_data["Happiness Score"].max()


# Replace NaN values with the respective column mean
numeric_means = full_data.select_dtypes(include=[np.number]).mean()
full_data.update(full_data.select_dtypes(include=[np.number]).fillna(numeric_means))
