import logit
import numpy as np
import pandas as pd
import estimation
import WhatIfAnalysis as WIA
import requests as rq
from io import BytesIO

pd.options.display.float_format = '{:.4f}'.format

path_1 = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"
path_2 = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/bilbasen_data_subset.csv"

data_1 = rq.get(path_1).content
dataset = pd.read_excel(BytesIO(data_1))

data_2 = rq.get(path_2).content
bilbasen_data_subset = pd.read_csv(BytesIO(data_2), delimiter = ',', encoding = 'unicode_escape')

attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

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
        dummy_names = [f'{dummyvar} = {v}' for v in list(dummies.columns[1:].values)] # omit a reference category 
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

cost_km_index = 4

def cost_km(index = cost_km_index, pfuel_relative = 1.0):
    p_km = x[:, :, index] * pfuel_relative
    return p_km

def gamma_fuel_value(gamma_fuel, theta = res['theta_hat'], x = x, pr = 1.0, pr_relative = 1.01, p_km_baseline = x[:, :, cost_km_index]):
    ccp = logit.choice_prob(theta, x)

    p_km_0 = cost_km(index = 4, pfuel_relative = pr)
    km_0 = 45.0 + (p_km_0 - p_km_baseline) * gamma_fuel
    km_per_car_0 = km_0 * ccp 

    p_km_1 = cost_km(index = 4, pfuel_relative = pr_relative)
    km_1 = 45.0 + (p_km_1 - p_km_baseline) * gamma_fuel
    km_per_car_1 = km_1 * ccp

    diff = km_per_car_1/km_per_car_0 - 1.0
    elasticity = np.mean(np.abs(diff)) / 0.01

    return elasticity

gs = WIA.GoalSeek(gamma_fuel_value, goal = 0.32, x0 = 0.01) # true value: 0.3249087307514338
print("\ngamma_fuel value (Goal Seek value):", gs)

def predict_driving(theta, x, pfuel_relative = 1.0, gamma_fuel = gs, idx_pkm = cost_km_index, p_km_baseline = x[:, :, cost_km_index]):
    ccp = logit.choice_prob(theta, x)
    #print("\ncp:\n", ccp)

    p_km = x[:, :, idx_pkm] * pfuel_relative
    #print("\np_km =", np.mean(p_km))

    km = 45.0 + (p_km - p_km_baseline) * gamma_fuel
    #print("\nkm:\n", km)

    km_per_car = km * ccp
    #print("\nkm_per_car:\n", km_per_car.shape)

    return km_per_car


CO2 = []

kmL_data = bilbasen_data_subset[['aargang', 'kmL', 'drivkraft']].set_index(['drivkraft'])

kmL_benzin_data = kmL_data.loc['Benzin']
kmL_benzin_mean = kmL_benzin_data['kmL'].mean()
#("\nkmL Benzin mean:", kmL_benzin_mean)

kmL_diesel_data = kmL_data.loc['Diesel']
kmL_diesel_mean = kmL_diesel_data['kmL'].mean()
#print("\nkmL Diesel mean:", kmL_diesel_mean)

kmL_el_data = kmL_data.loc['El']
kmL_el_mean = kmL_el_data['kmL'].mean()
#print("\nkmL EL mean:", kmL_el_mean)

km = predict_driving(theta = res['theta_hat'], x = x)
#print("\nkm:\n", km)

for aar in range(0, N):
    for i in range(0, J):
        fuel = dataset[['Year', 'Fuel']].set_index(['Year'])
        fuel = fuel.loc[2006 + aar].iloc[i].values[0]
        if fuel == 'Benzin':
            #print("\nkm[aar][i]:", km[aar][i])
            liters = km[aar][i] / kmL_benzin_mean
            CO2_L_benzin = 2.3 # gns. kg CO2 per liter for benzinbiler
            #dataset.loc[, 'CO2'] = CO2_L_benzin * liters
            car_CO2 = CO2_L_benzin * liters
            CO2.append(car_CO2)
        elif fuel == 'Diesel':
            liters = km[aar][i] / kmL_diesel_mean
            CO2_L_diesel = 2.7 # gns. kg CO2 per liter for dieselbiler
            #dataset.loc[, 'CO2'] = CO2_L_diesel * liters
            CO2.append(car_CO2)
        else:
            liters = km[aar][i] / kmL_el_mean
            CO2_km_el = 0.0009 # gns. kg CO2 per km for elbiler
            #dataset.loc[, 'CO2'] = CO2_km_el * liters
            CO2.append(car_CO2)

dataset = dataset.assign(CO2 = CO2)

CO2_data = dataset[['Year', 'CO2', 'Fuel']].set_index(['Fuel'])

CO2_benzin_data = CO2_data.loc['Benzin']
CO2_benzin_mean = CO2_benzin_data['CO2'].mean()
print("\nCO2 Benzin:\n", CO2_benzin_data)

CO2_diesel_data = CO2_data.loc['Diesel']
CO2_diesel_mean = CO2_diesel_data['CO2'].mean()
print("\nCO2 Diesel:\n", CO2_diesel_data)

CO2_el_data = CO2_data.loc['El']
CO2_el_mean = CO2_el_data['CO2'].mean()
print("\nCO2 EL\n:", CO2_el_data)

print("\nMean of CO2 for each fueltype:")
print(CO2_benzin_mean, CO2_diesel_mean, CO2_el_mean)

