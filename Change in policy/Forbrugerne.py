#%% Loading packages, pat and dataset
import logit 
from logit import *
import numpy as np
import pandas as pd
import estimation
import WhatIfAnalysis as WIA
import requests as rq
from io import BytesIO
import clogit_estimation as cle
import afgiftspligtig_værdi as av


pd.options.display.float_format = '{:.4f}'.format
path = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"

data = rq.get(path).content
dataset = pd.read_excel(BytesIO(data))


# %% Conditional logit
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
print('beta price = ',res['theta_hat'][0])
#ccp = choice_prob(res['theta_hat'], x)


# %% Ændre afgifterne til 2030-afgifterne
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


dataset = dataset.assign(new_prices = new_prices1)
dataset['new_prices'] = np.log(dataset['new_prices'] / 100000)
print("\nnew_prices:\n", dataset['new_prices'])

variables_v2 = ['new_prices', 'Weight (kg)', 'Engine effect (kW)', 'Size (m3)', 'Cost/km (DKK)']

x_v2, y_v2, x_vars_v2 = cle.get_x_y(dataset = dataset, dummyvar = 'Fuel', attributes = variables_v2)

# %%
def CS(theta, x):
    v = util(theta, x, MAXRESCALE=False)
    v_sum = np.sum(np.exp(v), axis=1)
    v_log = np.log(v_sum)
    return v_log

cs = CS(res['theta_hat'], x)
print('\ncs =\n',cs)
print('\ncs shape =',cs.shape)


def CV(theta, x1, x2):
    policy = (1/theta[0])*CS(theta, x1) #Policy, vi skal kun tage 
    baseline = (1/theta[0])*CS(theta, x2)
    C_V = policy - baseline 
    return C_V

cv = CV(res['theta_hat'], x_v2, x)
print('\ncv = \n',cv)
print('cv = ',cv.shape)












def compensating_supply(theta, x): 
    U = util(theta, x, MAXRESCALE=False)
    U_max = U.max(axis=1, keepdims=True)
    print('\nU max transposed =\n', U_max.T)
    print('\nU max transposed shape =\n', U_max.T.shape)
    U_index = U.argmax(axis=1)
    ccp = choice_prob(theta, x) 
    #print('index = ',U_index)

    ccp_lst = []
    for i in range(0, N): 
        ccp_lst.append(ccp[i, U_index[i]])
    print('\nlist =\n',np.array([ccp_lst]).reshape(-1,1))
    ccp_lst = np.array([ccp_lst]).reshape(-1,1)
    print('\nlist shape =\n',ccp_lst.shape)
    U_expected = ccp_lst.T@U_max
    return U_expected 
#cs = compensating_supply(res['theta_hat'],x)
#print('cs =',cs.shape)

    #udregn max(u_ij + e_ij)
    #cs = Udregn expected value af max, og returner denne 
    #return cs

def compensating_variation(theta, x1, x2):
    cv = (1/theta)(compensating_supply(theta, x1)-compensating_supply(theta, x2))
    return cv 
#cv = compensating_variation(res['theta_hat', x, x_v2])




# %%
m = np.zeros([15,1])
print(m.shape)
n = np.zeros([15,1])
print(n.shape)
g = n.T@m
g1 = n@m.T
print('g shape= ',g.shape)
print('g1 shape = ',g1.shape)
# %%
