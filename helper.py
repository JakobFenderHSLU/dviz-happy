import pandas as pd

custom_color_scale = [
    (0.0, "red"),  # Low scores in red
    (0.5, "orange"),  # Medium scores in orange
    (1.0, "green")  # High scores in green
]

# Import data
whr23 = pd.read_csv('data/WHR2023.csv')
world_data = pd.read_csv('data/world-data-2023.csv')
continent_file = pd.read_csv('data/continents2.csv')

# Data cleaning

# Merge the datasets
# Change column names to match the main dataset
continent_file.rename(columns={'name': 'Country name', 'alpha-2': 'country code'}, inplace=True)
column_order = ['Country name', 'region', 'sub-region', 'country code']

# Merge region and sub-region into whr23score after country name
merged_data = whr23.merge(continent_file[['Country name', 'region', 'sub-region', 'country code']], on='Country name')
column_order = ['Country name', 'region', 'sub-region', 'country code'] + [col for col in merged_data.columns if
                                                                           col not in column_order]
merged_data = merged_data[column_order]

# Rename the 'Country' column to 'Country name' in the extra_data DataFrame
world_data.rename(columns={'Country': 'Country name'}, inplace=True)

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
