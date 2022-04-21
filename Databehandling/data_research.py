import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# CHOICE DATA
choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
#choice_data = choice_data.rename(columns = {'Make-model-year-fuel' : 'key'})
choice_data['key'] = choice_data['Make'] + '-' + choice_data['Model'] + '-' + choice_data['Year'].astype(str) + '-' + choice_data['Fuel']
choice_data['key'] = choice_data['key'].str.replace(' ', '-')
choice_data_subset = choice_data[['Year', 'Shares', 'Fuel', 'Weight (kg)', 'Engine effect (kW)', 'Prices (2015-DKK)', 'key']]
print("Choice_data subset:\n", choice_data_subset)

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

combined_data['kmL'] = pd.to_numeric(combined_data['kmL'], errors = 'coerce')
combined_data['kmL'] = combined_data['kmL'].astype(float)
combined_data = combined_data.reset_index(drop = True)
print("\ncombined_data after drop duplicates:\n", combined_data)

# Converting from panadas dataframes into excel-files
combined_data.to_excel(path + 'combined_data.xlsx', index = False)
choice_data_subset.to_excel(path + 'choice_data_subset.xlsx', index = False)

