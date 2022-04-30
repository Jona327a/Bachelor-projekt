import numpy as np
import pandas as pd
import estimation
import logit

pd.options.display.float_format = '{:.10f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# NOTICE: remember to choose the correct dataset
dataset = pd.read_excel(path + 'choice_data_subset.xlsx')
dataset['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
print("Dataset: \n", dataset, "\n")

attributes = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Cost/km (DKK)', 'Horsepower']
N = dataset.Year.nunique()
J = dataset[['Year', 'key']].groupby('Year').count().min().tolist()[0]
K = len(attributes)

print("N:", N, "forskellige årstal")
print("J:", J, "alternativer")
print("K:", K, "alternativer \n")

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
    
    y = dataset['Fuel'].values.reshape(N, J)
    
    return x, y, x_vars

x, y, x_vars = get_x_y(dataset = dataset, dummyvar = 'Size segment', attributes = attributes)

#print("x: \n", x)
#print("x's shape:", x.shape)

#print("y: \n", y)
#print("y's shape:", y.shape, "\n")

thetahat, se = estimation.estimate_m(logit, y, x, method = 'BFGS', cov_type = 'Sandwich', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)

tab = pd.DataFrame({'Coefficients' : thetahat, 'se' : se}, index = x_vars)
tab.loc['Q', 'Coefficients'] = np.mean(logit.q(thetahat, y, x))
tab.loc['Q', 'se'] = ' '
print("\n", tab)
