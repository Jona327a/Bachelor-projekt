import logit 
from logit import *
import numpy as np
import pandas as pd
import estimation
import requests as rq
from io import BytesIO
import afgiftspligtig_værdi as av

pd.options.display.float_format = '{:.4f}'.format
path = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"

data = rq.get(path).content
dataset = pd.read_excel(BytesIO(data))

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

attributes_original = ['Prices (2015-DKK)', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']
x_original, y_original, x_vars_original = get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = attributes_original)
theta0 = logit.starting_values(y = y_original, x = x_original)
res = estimation.estimate(q = logit.q, theta0 = theta0, y = y_original, x = x_original, cov_type = 'Sandwich', method = 'BFGS', options = {'disp':True, 'maxiter':10_000}, tol = 1e-8)

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

prices_2020 = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 65000, reg_beløb_2 = 202200, 
                        bundfradrag = 21700, el_bundfradrag_1 = 170000, el_fradrag_2 = 1700, indfasning = 0.40)
dataset = dataset.assign(prices_2020 = prices_2020)
dataset['prices_2020'] = np.log(dataset['prices_2020'] / 100000)
print("\nprices_2020:\n", dataset['prices_2020'])
attributes = ['prices_2020', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']
x_2020, y_2020, x_vars_2020 = get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = attributes)

new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 77094.65, reg_beløb_2 = 239721.34, 
                bundfradrag = 25658.84, el_bundfradrag_1 = 137000.0, el_fradrag_2 = 0, indfasning = 0.80)
                #2030 - satserne 

#new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 74101.0, reg_beløb_2 = 230413.0, 
               #bundfradrag = 24663.0, el_bundfradrag_1 = 146200.0, el_fradrag_2 = 0.0, indfasning = 0.64)
                #2028 - satserne 

#new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 68458.0, reg_beløb_2 = 212866.0, 
               #bundfradrag = 22785.0, el_bundfradrag_1 = 162500.0, el_fradrag_2 = 500.0, indfasning = 0.40)
                #2024 - satserne 

#new_prices = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 65800.0, reg_beløb_2 = 204600.0, 
               #bundfradrag = 21900.0, el_bundfradrag_1 = 167500.0, el_fradrag_2 = 1300.0, indfasning = 0.40)
                #2022 - satserne 

dataset = dataset.assign(new_prices = new_prices)
dataset['new_prices'] = np.log(dataset['new_prices'] / 100000)
print("\nnew_prices:\n", dataset['new_prices'])

variables_v2 = ['new_prices', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

x_new, y_new, x_vars_new = get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = variables_v2)

def CS(theta, x):
    v = util(theta, x, MAXRESCALE=False)
    v_sum = np.sum(np.exp(v), axis=1)
    v_log = np.log(v_sum)
    return v_log

def CV(theta, x1, x2):
    policy = (1/theta[0])*CS(theta, x1)
    baseline = (1/theta[0])*CS(theta, x2)
    C_V = policy - baseline 
    return C_V

CV = CV(res['theta_hat'], x1 = x_new, x2 = x_2020)
print('\nCV:\n', CV)


CV_2022 = np.array([-0.00389878, -0.00392702, -0.0040203,  -0.00387936, -0.00397949, -0.00390592, -0.00369635, -0.00362468,])
print('\nCV 2022\n',CV_2022.mean())


CV_2024 = np.array([-0.01775808, -0.01794734, -0.01796454, -0.01728082, -0.01781973, -0.01815415, -0.01717108, -0.01666829])
#print('\nCV 2024\n',CV_2024)


CV_2028 = np.array([-0.04634704, -0.04666788, -0.04557422, -0.04479413, -0.04531776, -0.04631163, -0.04347299, -0.04131665])
#print('\nCV 2028\n',CV_2028)


CV_2030 = np.array([-0.06120409, -0.06141781, -0.05982742, -0.05892245, -0.05945665, -0.06014766, -0.05705052, -0.05376497])
print('\nCV 2030\n',CV_2030.mean())

Procent_aendring_2022_2024 = ((CV_2022-CV_2024)/CV_2022)*100
print('\nProcentvis ændring fra 2022 til 2024\n',Procent_aendring_2022_2024.mean())

Procent_aendring_2024_2028 = ((CV_2024-CV_2028)/CV_2024)*100
print('\nProcentvis ændring fra 2024 til 2028\n',Procent_aendring_2024_2028.mean())

Procent_aendring_2028_2030 = ((CV_2028-CV_2030)/CV_2028)*100
print('\nProcentvis ændring fra 2028 til 2030\n',Procent_aendring_2028_2030.mean())

Procent_aendring_2022_2030 = ((CV_2022-CV_2030)/CV_2022)*100
print('\nProcentvis ændring fra 2022 til 2030\n',Procent_aendring_2022_2030.mean())

Procent_aendring_2022_2030 = ((CV_2030-CV_2022)/CV_2022)*100
print('\nProcentvis ændring fra 2022 til 2030\n',Procent_aendring_2022_2030.mean())


