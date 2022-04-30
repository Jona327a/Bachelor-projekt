import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# CHOICE DATA
choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
#choice_data = choice_data.rename(columns = {'Make-model-year-fuel' : 'key'})
choice_data['key'] = choice_data['Make'] + '-' + choice_data['Model'] + '-' + choice_data['Year'].astype(str) + '-' + choice_data['Fuel']
choice_data['key'] = choice_data['key'].str.replace(' ', '-')
choice_data_subset = choice_data[['Year', 'Shares', 'Fuel', 'Weight (kg)', 'Engine effect (kW)', 'Prices (2015-DKK)', 'key', 'Size segment', 'No. of registrations', 'Horsepower', 'Cost/km (DKK)']]
print("Choice_data subset before changing number of obs:\n", choice_data_subset)

# BILBASEN SCRAPE
bilbasen_data = pd.read_csv(path + 'bilbasen_scrape.csv', delimiter=';', encoding = 'unicode_escape')
bilbasen_data.rename(columns = {'Unnamed: 6': 'make model year'}, inplace = True)
bilbasen_data['key'] = bilbasen_data['make model year'] + '-' + bilbasen_data['drivkraft']
bilbasen_subset = bilbasen_data[['kmL', 'key']]
print("\nBilbasen subset:\n", bilbasen_subset)

# COMBINING THE TWO DATASETS
combined_data = pd.merge(choice_data_subset, bilbasen_subset, on = "key")
print("\ncombined_data before drop duplicates:\n", combined_data)
combined_data.drop_duplicates(subset = ['key'], keep = 'last', inplace = True, ignore_index = True)
combined_data['kmL'] = combined_data['kmL'].str.replace('km/l', '')
combined_data['kmL'] = combined_data['kmL'].str.replace('km', '')
combined_data['kmL'] = combined_data['kmL'].str.replace("\(NEDC\)", '')
combined_data['kmL'] = combined_data['kmL'].str.replace(',', '.')

for i in combined_data.index:
    share_check = combined_data['Shares'].loc[i]
    fuel_check = combined_data['Fuel'].loc[i]
    weight_check = combined_data['Weight (kg)'].loc[i]
    engine_check = combined_data['Engine effect (kW)'].loc[i]
    kmL_check = combined_data['kmL'].loc[i]
    price_check = combined_data['Prices (2015-DKK)'].loc[i]
    if share_check == '-' or fuel_check == '-' or weight_check == '-' or engine_check == '-' or kmL_check == '-' or price_check == '-':
        combined_data = combined_data.drop(labels = i, axis = 0)

"""
for i in choice_data_subset.index:
    year_check = choice_data_subset['Year'].loc[i]
    if year_check < 2011:
        choice_data_subset = choice_data_subset.drop(labels = i, axis = 0)


index = choice_data_subset.index
aar_data = choice_data_subset.set_index("Year").loc[2020]
aar_fuel_data = aar_data.set_index("Fuel").loc['Diesel']
min_reg = aar_fuel_data[aar_fuel_data['No. of registrations'] == aar_fuel_data['No. of registrations'].min()]
condition = choice_data_subset['key'] == min_reg.key[0]
print("condition:", condition)
row = index[condition].tolist()[0]
print("row:", row)


# Making sure that every Year has the same number of observations
lowest_obs = choice_data_subset[['Year', 'key']].groupby('Year').count().min().tolist()[0]
aarstal = choice_data_subset['Year'].drop_duplicates()
for aar in aarstal:
    i = 0
    while choice_data_subset.set_index("Year").loc[aar].shape[0] > lowest_obs:
        car_i = choice_data_subset.set_index("Year").loc[aar].iloc[i]
        two_indices = choice_data_subset.set_index(["Year", "Fuel"])
        if car_i['Fuel'] != 'El':
            index = choice_data_subset.index
            condition = choice_data_subset['key'] == car_i.loc['key']
            #print(condition)
            row = index[condition].tolist()[0]
            choice_data_subset = choice_data_subset.drop(labels = row, axis = 0)
        else:
            i = 1 + i
print("Choice_data subset after changing number of obs:\n", choice_data_subset)
"""

# Making sure that every Year has the same number of observations
lowest_obs = choice_data_subset[['Year', 'key']].groupby('Year').count().min().tolist()[0]
aarstal = choice_data_subset['Year'].drop_duplicates()
for aar in aarstal:
    i = 0
    while choice_data_subset.set_index("Year").loc[aar].shape[0] > lowest_obs:
        car_i = choice_data_subset.set_index("Year").loc[aar].iloc[i]
        index = choice_data_subset.index
        aar_data = choice_data_subset.set_index("Year").loc[aar]
        if car_i['Fuel'] == 'Benzin':
            aar_fuel_data = aar_data.set_index("Fuel").loc['Benzin']
            min_reg = aar_fuel_data[aar_fuel_data['No. of registrations'] == aar_fuel_data['No. of registrations'].min()]
            condition = choice_data_subset['key'] == min_reg.key[0]
            row = index[condition].tolist()[0]
            choice_data_subset = choice_data_subset.drop(labels = row, axis = 0)
        elif car_i['Fuel'] == 'Diesel':
            aar_fuel_data = aar_data.set_index("Fuel").loc['Diesel']
            min_reg = aar_fuel_data[aar_fuel_data['No. of registrations'] == aar_fuel_data['No. of registrations'].min()]
            condition = choice_data_subset['key'] == min_reg.key[0]
            row = index[condition].tolist()[0]
            choice_data_subset = choice_data_subset.drop(labels = row, axis = 0)
        else:
            i = 1 + i
print("Choice_data subset after changing number of obs:\n", choice_data_subset)

combined_data['kmL'] = pd.to_numeric(combined_data['kmL'], errors = 'coerce')
combined_data['kmL'] = combined_data['kmL'].astype(float)
combined_data = combined_data.reset_index(drop = True)
print("\ncombined_data after drop duplicates:\n", combined_data)

# Converting from panadas dataframes into excel-files
combined_data.to_excel(path + 'combined_data.xlsx', index = False)
choice_data_subset.to_excel(path + 'choice_data_subset.xlsx', index = False)
