#%% Loading packages, path and dataset
import logit
import numpy as np
import pandas as pd
import estimation
import WhatIfAnalysis as WIA
import requests as rq
from io import BytesIO
import afgiftspligtig_værdi as av

pd.options.display.float_format = '{:.5f}'.format

path_1 = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"
path_2 = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/bilbasen_data_subset.csv"

data_1 = rq.get(path_1).content
dataset = pd.read_excel(BytesIO(data_1))

data_2 = rq.get(path_2).content
bilbasen_data_subset = pd.read_csv(BytesIO(data_2), delimiter = ',', encoding = 'unicode_escape')

attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

#%% Cleaning the dataset
N = dataset.Year.nunique()
J = dataset[['Year', 'key']].groupby('Year').count().min().tolist()[0]

dataset['Prices (2015-DKK)'] = np.log(dataset['Prices (2015-DKK)'] / 100000)
dataset['Weight (kg)'] = dataset['Weight (kg)'] / 1000
dataset['Engine effect (kW)'] = dataset['Engine effect (kW)'] / 100

def get_x_y(dataset, dummyvar = None, attributes = []):
    x_vars = []
    x_vars += attributes 
    x_attributes = dataset[attributes].values
    
    if dummyvar is not None: 
        dummies = pd.get_dummies(dataset[dummyvar])
        dummy_names = [f'{dummyvar} = {v}' for v in list(dummies.columns[1:].values)]
        x_dummies = dummies.values[:, 1:]
        x_vars += dummy_names
        x = np.hstack([x_attributes, x_dummies]).reshape(N, J, -1)
    else:
        dummy_names = []
        x_dummies = []
        x = x_attributes.reshape(N, J, -1)
    
    y = dataset['Markedsandele'].values.reshape(N, J)
    
    return x, y, x_vars

x, y, x_vars = get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = attributes)

theta0 = logit.starting_values(y = y, x = x)
res = estimation.estimate(q = logit.q, theta0 = theta0, y = y, x = x, cov_type = 'Sandwich', method = 'BFGS', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)
table = pd.DataFrame({'Coefficients' : res['theta_hat'], 'se' : res['se'], 't-values' : res['t']}, index = x_vars)
print("\nConditional logit estimation:\n", table)

#%% Calculating prices, and predict new prices
def new_prices(rate_1, rate_2, rate_3, reg_beløb_1, reg_beløb_2, bundfradrag, el_bundfradrag_1, el_fradrag_2, indfasning):

    new_prices = []
    for i in range(0, dataset.shape[0]):
        av_i = dataset.loc[i, 'afgiftspligtig_værdi']
        fuel_i = dataset.loc[i, 'Fuel']
        if fuel_i == 'El':
            new_price = av.pris_efter_reg_afgift_el(afgiftspligtig_værdi = av_i, bundfradrag = bundfradrag, ekstra_bundfradrag = el_bundfradrag_1, indfasning = indfasning, 
                                                    reg_beloeb1 = reg_beløb_1, reg_beloeb2 = reg_beløb_2, el_fradrag = el_fradrag_2,
                                                    part_1 = rate_1, part_2 = rate_2, part_3 = rate_3)
            new_prices.append(new_price)
        elif fuel_i == 'Benzin':
            new_price = av.pris_efter_reg_afgift_ben(afgiftspligtig_værdi = av_i, bundfradrag = bundfradrag, 
                                                    reg_beloeb1 = reg_beløb_1, reg_beloeb2 = reg_beløb_2, 
                                                    part_1 = rate_1, part_2 = rate_2, part_3 = rate_3)
            new_prices.append(new_price)
        else:
            new_price = av.pris_efter_reg_afgift_die(afgiftspligtig_værdi = av_i, bundfradrag = bundfradrag, 
                                                    reg_beloeb1 = reg_beløb_1, reg_beloeb2 = reg_beløb_2,
                                                    part_1 = rate_1, part_2 = rate_2, part_3 = rate_3)
            new_prices.append(new_price)
    return new_prices

new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 77094.65, reg_beløb_2 = 239721.34, 
                        bundfradrag = 25658.84, el_bundfradrag_1 = 137000.00, el_fradrag_2 = 0, indfasning = 0.80)
                #2030 - satserne 

#new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.95, rate_3 = 1.15, reg_beløb_1 = 69827, reg_beløb_2 = 217123, 
                        #bundfradrag = 23240, el_bundfradrag_1 = 160000, el_fradrag_2 = 0, indfasning = 0.40)
                #2025 - satserne

#new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 65000, reg_beløb_2 = 202200, 
                        #bundfradrag = 21700, el_bundfradrag_1 = 170000, el_fradrag_2 = 1700, indfasning = 0.40)
                #2020 - satserne 

dataset = dataset.assign(new_prices = new_prices)
dataset['new_prices'] = np.log(dataset['new_prices'] / 100000)
variables_v2 = ['new_prices', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']
x_v2, y_v2, x_vars_v2 = get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = variables_v2)

#%% Predict kørsel og CO2
cost_km_index = 4

def cost_km(index = cost_km_index, pfuel_relative = 1.0):
    p_km = x_v2[:, :, index] * pfuel_relative
    return p_km

def gamma_fuel_value(gamma_fuel, theta = res['theta_hat'], x = x_v2, pr = 1.0, pr_relative = 1.01, p_km_baseline = x_v2[:, :, cost_km_index]):
    ccp = logit.choice_prob(theta, x)

    p_km_0 = cost_km(index = 4, pfuel_relative = pr)
    km_0 = 46.6 + (p_km_0 - p_km_baseline) * gamma_fuel
    km_per_car_0 = km_0 * ccp 

    p_km_1 = cost_km(index = 4, pfuel_relative = pr_relative)
    km_1 = 46.6 + (p_km_1 - p_km_baseline) * gamma_fuel
    km_per_car_1 = km_1 * ccp

    diff = km_per_car_1/km_per_car_0 - 1.0
    elasticity = np.mean(np.abs(diff)) / 0.01

    return elasticity

gs = WIA.GoalSeek(gamma_fuel_value, goal = 0.30, x0 = 0.01)
print("\ngamma_fuel value (Goal Seek value):", gs)

def predict_driving(theta, x, pfuel_relative = 1.0, gamma_fuel = gs, idx_pkm = cost_km_index, p_km_baseline = x_v2[:, :, cost_km_index]):
    km_per_car_list = []
    ccp = logit.choice_prob(theta, x)

    p_km = x_v2[:, :, idx_pkm] * pfuel_relative

    km = 46.6 + (p_km - p_km_baseline) * gamma_fuel

    reg = dataset.groupby('Year')['No. of registrations'].sum()

    for aar in range(0, N):
        for i in range(0, J):
            km_per_car_i = km[aar][i] * ccp[aar][i] * reg.tolist()[aar] * 365
            km_per_car_list.append(km_per_car_i)

    return np.array(km_per_car_list).reshape(N,J)

CO2 = []
kmL_data = bilbasen_data_subset[['aargang', 'kmL', 'drivkraft','forbrug (WLTP)']].set_index(['drivkraft'])

kmL_benzin_data = kmL_data.loc['Benzin']
kmL_benzin_mean = kmL_benzin_data['kmL'].mean()

kmL_diesel_data = kmL_data.loc['Diesel']
kmL_diesel_mean = kmL_diesel_data['kmL'].mean()

kmL_el_data = kmL_data.loc['El']
kmL_el_mean = kmL_el_data['kmL'].mean()

forbrug_el_data = kmL_data.loc['El']
forbrug_el_mean = forbrug_el_data['forbrug (WLTP)'].mean()

km = predict_driving(res['theta_hat'], x_v2)

for aar in range(0, N):
    for i in range(0, J):
        fuel = dataset[['Year', 'Fuel']].set_index(['Year'])
        fuel = fuel.loc[2006 + aar].iloc[i].values[0]
        if fuel == 'Benzin':
            liters = km[aar][i] / kmL_benzin_mean
            CO2_L_benzin = 2.3 # gns. kg CO2 per liter for benzinbiler
            car_CO2 = CO2_L_benzin * liters
            CO2.append(car_CO2)
        elif fuel == 'Diesel':
            liters = km[aar][i] / kmL_diesel_mean
            CO2_L_diesel = 2.7 # gns. kg CO2 per liter for dieselbiler
            car_CO2 = CO2_L_diesel * liters
            CO2.append(car_CO2)
        else:
            kWhs = km[aar][i] / (kmL_el_mean / forbrug_el_mean)
            CO2_kWh = 0.213 # gns. kg CO2 per kWh for elbiler
            car_CO2 = CO2_kWh * kWhs
            CO2.append(car_CO2)

dataset = dataset.assign(CO2 = CO2)

CO2_data = dataset[['Year', 'CO2', 'Fuel']].set_index(['Fuel'])

CO2_benzin_data = CO2_data.loc['Benzin']
CO2_benzin_sum = (CO2_benzin_data['CO2'].sum()/15)/1000000

CO2_diesel_data = CO2_data.loc['Diesel']
CO2_diesel_sum = (CO2_diesel_data['CO2'].sum()/15)/1000000

CO2_el_data = CO2_data.loc['El']
CO2_el_sum = (CO2_el_data['CO2'].sum()/15)/1000000


# %% emission 
emission = [CO2_benzin_sum, CO2_diesel_sum, CO2_el_sum]
cars = ['Gasoline car', 'Diesel car', 'EV']

table1 = pd.DataFrame({'CO2 emissions' : emission}, index = cars)
print("\nCO2 emission for each car type:\n", table1)

# %% 
Gasoline_emission_2020 = 252.82
Diesel_emission_2020 = 158.74
EV_emission_2020 = 1.24
emission_2020_sum = Gasoline_emission_2020 + Diesel_emission_2020 + EV_emission_2020
print('Sum af 2020-udledning = ',emission_2020_sum)

Gasoline_emission_2025 = 252.92
Diesel_emission_2025 = 158.64
EV_emission_2025 = 1.24
emission_2025_sum = Gasoline_emission_2025 + Diesel_emission_2025 + EV_emission_2025
print('Sum af 2025-udledning = ',emission_2025_sum)

Gasoline_emission_2030 = 253.12
Diesel_emission_2030 = 158.69
EV_emission_2030 = 1.17
emission_2030_sum = Gasoline_emission_2030 + Diesel_emission_2030 + EV_emission_2030
print('Sum af 2030-udledning = ',emission_2030_sum)

Forskel_i_procent = ((emission_2030_sum - emission_2020_sum)/emission_2020_sum)*100
print('Procentvis forskel i 2020 vs 2030 CO2-udledning = ',Forskel_i_procent)
