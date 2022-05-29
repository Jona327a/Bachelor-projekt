#%%
import numpy as np
import pandas as pd
import estimation
import logit

pd.options.display.float_format = '{:.6f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"
path = '../Data/'

# NOTICE: remember to choose the correct dataset
dataset = pd.read_excel(path + 'choice_data_subset.xlsx')

#dataset['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
#dataset['Size segment'].replace(['Small', 'Large'], [0, 1], inplace = True)

attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

N = dataset.Year.nunique()
J = dataset[['Year', 'key']].groupby('Year').count().min().tolist()[0]

# Changing the measure of 'Prices (2015-DKK)' into 100000 kr.
dataset['Prices (2015-DKK)'] = np.log(dataset['Prices (2015-DKK)'] / 100000)

# Changing the measure of 'Ownership cost (DKK)' into 100000 kr.
#dataset['Ownership cost (DKK)'] = dataset['Ownership cost (DKK)'] / 100000

# Changing the measure of 'Weight (kg)' into tons
dataset['Weight (kg)'] = dataset['Weight (kg)'] / 1000

# Changing the measure of 'Engine effect' into 100 kW
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

print("Dataset: \n", dataset, "\n")
print("N:", N, "forskellige årstal")
print("J:", J, "alternativer")
print("K:", len(x_vars), "variabler")
print("Variablerne:", x_vars, "\n")

#print("x: \n", x)
print("X's shape:", x.shape, "\n")

print("y (variablen 'Markedsandele'): \n", y)
print("y's shape:", y.shape, "\n")

"""
thetahat, se = estimation.estimate_m(logit, y, x, method = 'BFGS', cov_type = 'Sandwich', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)
t_values = thetahat / se
tab1 = pd.DataFrame({'Coefficients' : thetahat, 'se' : se, 't-values' : t_values}, index = x_vars)
tab1.loc['Q', 'Coefficients'] = np.mean(logit.q(thetahat, y, x))
tab1.loc['Q', 'se'] = ' '
tab1.loc['Q', 't-values'] = ' '
print("\n", tab1)
"""

theta0 = logit.starting_values(y, x)
res = estimation.estimate(logit.q, theta0, y, x, cov_type = 'Sandwich', method = 'BFGS', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)
tab2 = pd.DataFrame({'Coefficients' : res['theta_hat'], 'se' : res['se'], 't-values' : res['t']}, index = x_vars)
print("\n", tab2)

#%% compare observed and predicted shares 
ccp = logit.choice_prob(res['theta_hat'], x)

plt.scatter(y, ccp, alpha=0.1)
plt.plot(np.array([y.min(), y.max()]), np.array([ccp.min(), ccp.max()]), 'r')
plt.xlabel('Observed shares');
plt.ylabel('Predicted shares');

#%% Kørsel 
pkm0 = x[:,:,4]

def predict_driving(theta, x, pfuel_relative=1.0, gamma_fuel=-22.5, idx_pkm = 4, p_km_baseline = pkm0):
    ccp = logit.choice_prob(theta, x)
    p_km = x[:,:,idx_pkm]*pfuel_relative
    km = 45.0 + (p_km - p_km_baseline)*gamma_fuel
    km_per_car = km * ccp 
    return km_per_car

# test elasticity 
km0 = predict_driving(res['theta_hat'], x)
km1 = predict_driving(res['theta_hat'], x, pfuel_relative=1.01)
diff = km1/km0 - 1.0
print(f'Elasticity: {np.mean(np.abs(diff))/0.01 : 5.2%}')

# task: pick gamma_fuel (unknown parameter) so that the elasticity is as close as possible to some value you find in the literature (e.g. Gillingham & Munk-Nielsen, 2019)

# %% miljø
def predict_co2(theta, x, p_fuel_relative=1.0, gamma_fuel=-22.5): 
    km = predict_driving()
    km_per_liter = dataset['kmliter'].values 
    liters = km/km_per_liter
    co2_per_liter = 2.3 # kg CO2 per liter; for diesel 2.7kg
    co2 = liters*co2_per_liter
    return co2 