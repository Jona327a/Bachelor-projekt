import pandas as pd

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# CHOICE DATA
choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
choice_data = choice_data.rename(columns = {'Make-model-year-fuel' : 'key'})
#choice_data['key'] = choice_data['Make'] + '-' + choice_data['Model'] + '-' + choice_data['Year'].astype(str) + '-' + choice_data['Fuel']
choice_data['key'] = choice_data['key'].str.replace(' ', '-')
choice_data_subset = choice_data[['key', 'Year', 'Fuel', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Prices (2015-DKK)', 'Ownership cost (DKK)', 'No. of registrations', 'Horsepower', 'Cost/km (DKK)']]
print("Choice_data subset before changing number of obs:\n", choice_data_subset)

# BILBASEN SCRAPE
bilbasen_data = pd.read_csv(path + 'bilbasen_scrape.csv', delimiter=';', encoding = 'unicode_escape')
bilbasen_data.rename(columns = {'Unnamed: 2': 'Make'}, inplace = True)
bilbasen_data.rename(columns = {'Unnamed: 3': 'Model'}, inplace = True)
bilbasen_data.rename(columns = {'Unnamed: 6': 'Make-model-year'}, inplace = True)
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace('km/l', '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace('km', '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace("\(NEDC\)", '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace(',', '.')
bilbasen_data['key'] = bilbasen_data['Make-model-year'] + '-' + bilbasen_data['drivkraft']
bilbasen_subset = bilbasen_data[['aargang', 'key', 'kmL', 'nypris_kr', 'drivkraft']]
for i in bilbasen_subset.index:
    aargang_check = bilbasen_subset['aargang'].loc[i]
    kmL_check = bilbasen_subset['kmL'].loc[i]
    if kmL_check == '-' or aargang_check < 2006:
        bilbasen_subset = bilbasen_subset.drop(labels = i, axis = 0)
bilbasen_data['kmL'] = pd.to_numeric(bilbasen_data['kmL'], errors = 'coerce')
bilbasen_data['kmL'] = bilbasen_data['kmL'].astype(float)
bilbasen_data = bilbasen_data.reset_index(drop = True)
print("\nBilbasen subset:\n", bilbasen_subset)

# COMBINING THE TWO DATASETS
combined_data = pd.merge(choice_data_subset, bilbasen_subset, on = ['key'])
print("\ncombined_data before drop duplicates:\n", combined_data)
combined_data.drop_duplicates(subset = ['key'], keep = 'last', inplace = True, ignore_index = True)
for i in combined_data.index:
    #price_check = combined_data['Prices (2015-DKK)'].loc[i]
    weight_check = combined_data['Weight (kg)'].loc[i]
    engine_check = combined_data['Engine effect (kW)'].loc[i]
    cost_check = combined_data['Cost/km (DKK)'].loc[i]
    horsepower_check = combined_data['Horsepower'].loc[i]
    kmL_check = combined_data['kmL'].loc[i]
    nypris_check = combined_data['nypris_kr'].loc[i]
    if weight_check == '-' or engine_check == '-' or cost_check == '-' or horsepower_check == '-' or kmL_check == '-' or nypris_check == '-':
        combined_data = combined_data.drop(labels = i, axis = 0)
combined_data['kmL'] = pd.to_numeric(combined_data['kmL'], errors = 'coerce')
combined_data['kmL'] = combined_data['kmL'].astype(float)
combined_data = combined_data.reset_index(drop = True)
print("\ncombined_data after drop duplicates:\n", combined_data)

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

# Converting from panadas dataframes into excel-files
bilbasen_subset.to_csv(path + 'bilbasen_subset.csv', index = False)
combined_data.to_excel(path + 'combined_data.xlsx', index = False)
choice_data_subset.to_excel(path + 'choice_data_subset.xlsx', index = False)
