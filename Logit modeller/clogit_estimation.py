import numpy as np
import pandas as pd
import estimation
import logit
import requests as rq
from io import BytesIO

pd.options.display.float_format = '{:.4f}'.format
path = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"

data = rq.get(path).content
dataset = pd.read_excel(BytesIO(data))

attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']
#attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)']
#attributes = ['Prices (2015-DKK)', 'Weight (kg)']

N = dataset.Year.nunique()
J = dataset[['Year', 'key']].groupby('Year').count().min().tolist()[0]

# Changing the measure of 'Prices (2015-DKK)' into 100000 kr.
dataset['Prices (2015-DKK)'] = np.log(dataset['Prices (2015-DKK)'] / 100000)

# Changing the measure of 'Weight (kg)' into tons
dataset['Weight (kg)'] = dataset['Weight (kg)'] / 1000

# Changing the measure of 'Engine effect' into 100 kW
dataset['Engine effect (kW)'] = dataset['Engine effect (kW)'] / 100

def get_x_y(dataset, N, J, dummyvar = None, attributes = []):
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

x, y, x_vars = get_x_y(dataset = dataset, dummyvar = None, N = N, J = J, attributes = attributes)

print("N:", N, "forskellige årstal")
print("J:", J, "alternativer")
print("K:", len(x_vars), "variabler")
print("Variablerne:", x_vars, "\n")

def clogt_estimation(x, y, x_vars):
    theta0 = logit.starting_values(y, x)
    res = estimation.estimate(logit.q, theta0, y, x, cov_type = 'Sandwich', method = 'BFGS', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)
    #print("\n", res)
    table = pd.DataFrame({'Coefficients' : res['theta_hat'], 'se' : res['se'], 't-values' : res['t']}, index = x_vars)
    #print("\n", table)
    return res
clogt_estimation(x = x, y = y, x_vars = x_vars)

thetahat, se = estimation.estimate_m(logit, y, x, method = 'BFGS', cov_type = 'Sandwich', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)
t_values = thetahat / se

tab1 = pd.DataFrame({'Coefficients' : thetahat, 'se' : se, 't-values' : t_values}, index = x_vars)
tab1.loc['Q', 'Coefficients'] = np.mean(logit.q(thetahat, y, x))
tab1.loc['Q', 'se'] = ' '
tab1.loc['Q', 't-values'] = ' '
print("\n", tab1)
