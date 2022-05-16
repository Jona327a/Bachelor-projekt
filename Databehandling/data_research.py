import pandas as pd
import math
import WhatIfAnalysis as WIA

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# CHOICE DATA
choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
choice_data = choice_data.rename(columns = {'Make-model-year-fuel' : 'key'})
choice_data['key'] = choice_data['key'].str.replace(' ', '-')
choice_data_subset = choice_data[['key', 'Year', 'Fuel', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Prices (2015-DKK)', 'No. of registrations', 'Cost/km (DKK)']]
print("Choice_data subset before changing number of obs:\n", choice_data_subset)

# Inserting extra variable in CHOICE DATA
def pris_efter_reg_afgift_ben(afgiftspligtig_værdi, bundfradrag = 21700.0, reg_beloeb1 = 65000.0, reg_beloeb2 = 202200.0, 
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
    CO2_NEDC = 111.6
    CO2_takst = 250
    CO2_tillaeg = CO2_NEDC * CO2_takst
    if afgiftspligtig_værdi < reg_beloeb1:
        reg_part1 = part_1 * afgiftspligtig_værdi
        endelig_reg_afgift = reg_part1 + CO2_tillaeg - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
        return afgiftspligtig_værdi + endelig_reg_afgift
    else:
        reg_part1 = part_1 * reg_beloeb1
        if afgiftspligtig_værdi < reg_beloeb2:
            reg_part2 = part_2 * (afgiftspligtig_værdi - reg_beloeb1)
            endelig_reg_afgift = reg_part1 + reg_part2 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
            reg_part3 = part_3 * (afgiftspligtig_værdi - reg_beloeb2)
            endelig_reg_afgift = reg_part1 + reg_part2 + reg_part3 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift

def pris_efter_reg_afgift_die(afgiftspligtig_værdi, bundfradrag = 21700.0, reg_beloeb1 = 65000.0, reg_beloeb2 = 202200.0,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
    CO2_NEDC = 113.9
    CO2_takst = 250
    CO2_tillaeg = CO2_NEDC * CO2_takst
    if afgiftspligtig_værdi < reg_beloeb1:
        reg_part1 = part_1 * afgiftspligtig_værdi
        endelig_reg_afgift = reg_part1 + CO2_tillaeg - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
        return afgiftspligtig_værdi + endelig_reg_afgift
    else:
        reg_part1 = part_1 * reg_beloeb1
        if afgiftspligtig_værdi < reg_beloeb2:
            reg_part2 = part_2 * (afgiftspligtig_værdi - reg_beloeb1)
            endelig_reg_afgift = reg_part1 + reg_part2 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
            reg_part3 = part_3 * (afgiftspligtig_værdi - reg_beloeb2)
            endelig_reg_afgift = reg_part1 + reg_part2 + reg_part3 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift

kWh = 45
def pris_efter_reg_afgift_el(afgiftspligtig_værdi, bundfradrag = 21700.0, ekstra_bundfradrag = 170000.0, indfasning = 0.40, 
                            reg_beloeb1 = 65000, reg_beloeb2 = 202200.0, el_fradrag = 1700.0,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
        samlet_el_fradrag = el_fradrag * kWh
        ny_afgiftspligtig_værdi = afgiftspligtig_værdi - samlet_el_fradrag
        if ny_afgiftspligtig_værdi < reg_beloeb1:
            reg_part1 = part_1 * ny_afgiftspligtig_værdi
            endelig_reg_afgift = reg_part1 - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
            if endelig_reg_afgift < 0:
                return afgiftspligtig_værdi
            else: 
                return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part1 = part_1 * reg_beloeb1
            if ny_afgiftspligtig_værdi < reg_beloeb2:
                reg_part2 = part_2 * (ny_afgiftspligtig_værdi - reg_beloeb2)
                reg_før_indfas = reg_part1 + reg_part2 - bundfradrag
                indfasning_reg_afgift = indfasning * reg_før_indfas
                endelig_reg_afgift = indfasning_reg_afgift - ekstra_bundfradrag
                if endelig_reg_afgift < 0:
                    return afgiftspligtig_værdi
                else: 
                    return afgiftspligtig_værdi + endelig_reg_afgift
            else:
                reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
                reg_part3 = part_3 * (ny_afgiftspligtig_værdi - reg_beloeb2)
                reg_før_indfas = reg_part1 + reg_part2 + reg_part3 - bundfradrag
                indfasning_reg_afgift = indfasning * reg_før_indfas
                endelig_reg_afgift = indfasning_reg_afgift - ekstra_bundfradrag
                if endelig_reg_afgift < 0:
                    return afgiftspligtig_værdi
                else: 
                    return afgiftspligtig_værdi + endelig_reg_afgift

# Making the variable afgiftspligtig_værdi in Choice Data
goal_seeks = []
for i in range(0, choice_data.shape[0]):
    fuel = choice_data.loc[i, 'Fuel']
    price = choice_data.loc[i, 'Prices (2015-DKK)']
    if fuel == 'El':
        gs = WIA.GoalSeek(pris_efter_reg_afgift_el, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
    elif fuel == 'Benzin':
        gs = WIA.GoalSeek(pris_efter_reg_afgift_ben, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
    else:
        gs = WIA.GoalSeek(pris_efter_reg_afgift_die, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
choice_data = choice_data.assign(afgiftspligtig_værdi = goal_seeks)
afgiftspligtig_data = choice_data[['Year', 'afgiftspligtig_værdi', 'Fuel']]

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
kmL_data = bilbasen_data[['aargang', 'kmL', 'drivkraft', 'key']]
for i in kmL_data.index:
    aargang_check = kmL_data['aargang'].loc[i]
    kmL_check = math.isnan(kmL_data['kmL'].loc[i])
    if kmL_check == True or aargang_check < 2006:
        kmL_data = kmL_data.drop(labels = i, axis = 0)
bilbasen_subset = kmL_data[['key', 'kmL']]
kmL_data = kmL_data[['aargang', 'kmL', 'drivkraft']]
bilbasen_subset = bilbasen_subset.reset_index(drop = True)
kmL_data = kmL_data.reset_index(drop = True)

# COMBINING THE TWO DATASETS
combined_data = pd.merge(choice_data_subset, bilbasen_subset, on = ['key'])
print("\ncombined_data before drop duplicates:\n", combined_data)
combined_data.drop_duplicates(subset = ['key'], keep = 'last', inplace = True, ignore_index = True)
for i in combined_data.index:
    weight_check = combined_data['Weight (kg)'].loc[i]
    engine_check = combined_data['Engine effect (kW)'].loc[i]
    size_check = combined_data['Size (m3)'].loc[i]
    cost_check = combined_data['Cost/km (DKK)'].loc[i]
    if weight_check == '-' or engine_check == '-' or size_check == '-' or cost_check == '-':
        combined_data = combined_data.drop(labels = i, axis = 0)
combined_data = combined_data.reset_index(drop = True)

# Making the variable 'Markedsandele' in combined_data
J = combined_data[['Year', 'key']].groupby('Year').count()
aarstal = combined_data['Year'].drop_duplicates()
combined_data['Markedsandele'] = combined_data['No. of registrations']
for aar in aarstal:
    I = J.loc[aar].tolist()[0]
    reg_sum = combined_data[['Year', 'No. of registrations']].set_index("Year").loc[aar].sum()[0]
    shares = (combined_data[['Year', 'Markedsandele']].set_index("Year").loc[aar] / reg_sum).values
    for i in range(0, I):
        car_i = combined_data.set_index("Year").loc[aar].iloc[i]
        index = combined_data.index
        condition = combined_data['key'] == car_i.loc['key']
        row = index[condition].tolist()[0]
        combined_data.loc[row, 'Markedsandele'] = shares[i][0]

# Making the variable afgiftspligtig_værdi in combined_data
goal_seeks = []
for i in range(0, combined_data.shape[0]):
    fuel = combined_data.loc[i, 'Fuel']
    price = combined_data.loc[i, 'Prices (2015-DKK)']
    if fuel == 'El':
        gs = WIA.GoalSeek(pris_efter_reg_afgift_el, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
    elif fuel == 'Benzin':
        gs = WIA.GoalSeek(pris_efter_reg_afgift_ben, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
    else:
        gs = WIA.GoalSeek(pris_efter_reg_afgift_die, goal = price, x0 = 1000000)
        goal_seeks.append(gs)
combined_data = combined_data.assign(afgiftspligtig_værdi = goal_seeks)
print("\ncombined_data after drop duplicates:\n", combined_data)

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
kmL_data.to_csv(path + 'kmL_data.csv', index = False)
combined_data.to_excel(path + 'combined_data.xlsx', index = False)
choice_data_subset.to_excel(path + 'choice_data_subset.xlsx', index = False)
