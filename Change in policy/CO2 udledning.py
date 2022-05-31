#%% Loading packages, path and dataset
import logit
import numpy as np
import pandas as pd
import estimation
import WhatIfAnalysis as WIA
import requests as rq
from io import BytesIO
import clogit_estimation as cle
import afgiftspligtig_værdi as av

pd.options.display.float_format = '{:.4f}'.format

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

#cp = logit.choice_prob(res['theta_hat'], x)
#cp = cp.reshape(N*J,)
#print('cp1 = ',cp)
#print('x = ',x)

#%% Calculating prices, and predict new pricest

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

new_prices1 = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 77094.65, reg_beløb_2 = 239721.34, 
            bundfradrag = 25658.84, el_bundfradrag_1 = 147500.0, el_fradrag_2 = 0, indfasning = 0.80)

"""

new_prices = []
for i in range(0, dataset.shape[0]):
    av_i = dataset.loc[i, 'afgiftspligtig_værdi']
    fuel_i = dataset.loc[i, 'Fuel']
    if fuel_i == 'El':
        new_price = av.pris_efter_reg_afgift_el(afgiftspligtig_værdi = av_i, bundfradrag = 25658.84, ekstra_bundfradrag = 147500.0, indfasning = 0.80, 
                            reg_beloeb1 = 77094.65, reg_beloeb2 = 239721.34, el_fradrag = 0.0,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5)
        new_prices.append(new_price)
    elif fuel_i == 'Benzin':
        new_price = av.pris_efter_reg_afgift_ben(afgiftspligtig_værdi = av_i, bundfradrag = 25658.84, reg_beloeb1 = 77094.65, reg_beloeb2 = 239721.34, 
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5)
        new_prices.append(new_price)
    else:
        new_price = av.pris_efter_reg_afgift_die(afgiftspligtig_værdi = av_i, bundfradrag = 25658.84, reg_beloeb1 = 77094.65, reg_beloeb2 = 239721.34,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5)
        new_prices.append(new_price)
"""

dataset = dataset.assign(new_prices = new_prices1)
dataset['new_prices'] = np.log(dataset['new_prices'] / 100000)
print("\nnew_prices:\n", dataset['new_prices'])

variables_v2 = ['new_prices', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

x_v2, y_v2, x_vars_v2 = cle.get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = variables_v2)

#cp2 = logit.choice_prob(res['theta_hat'], x_v2)
#cp = cp.reshape(N*J,)
#print('cp2 = ',cp2)
#print('x_v2 = ',x_v2)
#dataset = dataset.assign(cp = cp)


#%% Predict kørsel og CO2
cost_km_index = 4

def cost_km(index = cost_km_index, pfuel_relative = 1.0):
    p_km = x_v2[:, :, index] * pfuel_relative
    return p_km

def gamma_fuel_value(gamma_fuel, theta = res['theta_hat'], x = x_v2, pr = 1.0, pr_relative = 1.01, p_km_baseline = x[:, :, cost_km_index]):
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

km = predict_driving(res['theta_hat'], x_v2)
print("\nkm:\n", km.mean())


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
#print("\nCO2 Benzin:\n", CO2_benzin_data)

CO2_diesel_data = CO2_data.loc['Diesel']
CO2_diesel_mean = CO2_diesel_data['CO2'].mean()
#print("\nCO2 Diesel:\n", CO2_diesel_data)

CO2_el_data = CO2_data.loc['El']
CO2_el_mean = CO2_el_data['CO2'].mean()
#print("\nCO2 EL\n:", CO2_el_data)

#print("\nMean of CO2 for each fueltype:")
#print(CO2_benzin_mean, CO2_diesel_mean, CO2_el_mean)





# %% emiision 
emission = [CO2_benzin_mean, CO2_diesel_mean, CO2_el_mean]
cars = ['Gasoline car', 'Diesel car', 'EV']

table1 = pd.DataFrame({'CO2 emissions' : emission}, index = cars)
print("\nCO2 emission for each car type:\n", table1)
# %%
