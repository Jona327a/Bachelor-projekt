import pandas as pd
import math
import afgiftspligtig_værdi as av

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# Choice Data and Choice Data Subset
choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
choice_data = choice_data.rename(columns = {'Make-model-year-fuel' : 'key'})
choice_data['key'] = choice_data['key'].str.replace(' ', '-')

# Making the variable afgiftspligtig_værdi in Choice Data
goal_seeks_choice_data = av.afgiftspligtig_veardi(choice_data)
choice_data = choice_data.assign(afgiftspligtig_værdi = goal_seeks_choice_data)
afgiftspligtig_data = choice_data[['Year', 'afgiftspligtig_værdi', 'Fuel']]

# Chosing the variables for Choice Data Subset
choice_data_subset = choice_data[['key', 'Year', 'Fuel', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Prices (2015-DKK)', 'No. of registrations', 'afgiftspligtig_værdi', 'Cost/km (DKK)']]
print("Choice_data subset before changing number of obs:\n", choice_data_subset)

# Making the variable 'Markedsandele' in Choice Data
J = choice_data[['Year', 'key']].groupby('Year').count()
aarstal = choice_data['Year'].drop_duplicates()
choice_data['Markedsandele'] = choice_data['No. of registrations']
for aar in aarstal:
    I = J.loc[aar].tolist()[0]
    reg_sum = choice_data[['Year', 'No. of registrations']].set_index("Year").loc[aar].sum()[0]
    shares = (choice_data[['Year', 'Markedsandele']].set_index("Year").loc[aar] / reg_sum).values
    for i in range(0, I):
        car_i = choice_data.set_index("Year").loc[aar].iloc[i]
        index = choice_data.index
        condition = choice_data['key'] == car_i.loc['key']
        row = index[condition].tolist()[0]
        choice_data.loc[row, 'Markedsandele'] = shares[i][0]
markedsandele_data = choice_data[['Year', 'Markedsandele', 'Fuel']]

# BILBASEN SCRAPE
bilbasen_data = pd.read_csv(path + 'bilbasen_scrape.csv', delimiter=';', encoding = 'unicode_escape')
bilbasen_data.rename(columns = {'Unnamed: 2': 'Make'}, inplace = True)
bilbasen_data.rename(columns = {'Unnamed: 3': 'Model'}, inplace = True)
bilbasen_data.rename(columns = {'Unnamed: 6': 'Make-model-year'}, inplace = True)
bilbasen_data['key'] = bilbasen_data['Make-model-year'] + '-' + bilbasen_data['drivkraft']
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace('km/l', '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace('km', '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace("\(NEDC\)", '')
bilbasen_data['kmL'] = bilbasen_data['kmL'].str.replace(',', '.')
bilbasen_data['kmL'] = pd.to_numeric(bilbasen_data['kmL'], errors = 'coerce')
bilbasen_data['kmL'] = bilbasen_data['kmL'].astype(float)
bilbasen_data_subset = bilbasen_data[['aargang', 'kmL', 'drivkraft', 'key']]
for i in bilbasen_data_subset.index:
    aargang_check = bilbasen_data_subset['aargang'].loc[i]
    kmL_check = math.isnan(bilbasen_data_subset['kmL'].loc[i])
    if kmL_check == True or aargang_check < 2006:
        bilbasen_data_subset = bilbasen_data_subset.drop(labels = i, axis = 0)
bilbasen_data_subset = bilbasen_data_subset[['aargang', 'kmL', 'drivkraft']]
bilbasen_data_subset = bilbasen_data_subset.reset_index(drop = True)

# Making sure that every Year has the same number of observations in Choice Data Subset
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

# Making the variable 'Markedsandele' in Choice Data Subset
J = choice_data_subset[['Year', 'key']].groupby('Year').count().min().tolist()[0]
aarstal = choice_data_subset['Year'].drop_duplicates()
choice_data_subset['Markedsandele'] = choice_data_subset['No. of registrations']
for aar in aarstal:
    reg_sum = choice_data_subset[['Year', 'No. of registrations']].set_index("Year").loc[aar].sum()[0]
    shares = (choice_data_subset[['Year', 'Markedsandele']].set_index("Year").loc[aar] / reg_sum).values
    for i in range(0, J):
        car_i = choice_data_subset.set_index("Year").loc[aar].iloc[i]
        index = choice_data_subset.index
        condition = choice_data_subset['key'] == car_i.loc['key']
        row = index[condition].tolist()[0]
        choice_data_subset.loc[row, 'Markedsandele'] = shares[i][0]
print("\nChoice_data subset after changing number of obs:\n", choice_data_subset)

# Converting from panadas dataframes into excel-files
afgiftspligtig_data.to_excel(path + 'afgiftspligtig_data.xlsx', index = False)
markedsandele_data.to_excel(path + 'markedsandele_data.xlsx', index = False)
bilbasen_data_subset.to_csv(path + 'bilbasen_data_subset.csv', index = False)
choice_data_subset.to_excel(path + 'choice_data_subset.xlsx', index = False)
