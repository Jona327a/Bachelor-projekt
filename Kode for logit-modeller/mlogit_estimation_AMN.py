import numpy as np
import pandas as pd
from scipy.optimize import minimize 

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# Final data
final_data = pd.read_excel(path + 'final_data.xlsx')
final_data.drop(columns = final_data.columns[0], axis = 1, inplace = True)
final_data['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
print("Dataset:\n", final_data)

final_data = final_data.values

y = final_data[:, 2].astype(int)
y = pd.DataFrame({'y' : y})
#print("\ny:\n", y)

x1 = final_data[:, 3].astype(float)
x2 = np.ones(x1.shape).astype(float)
#x3 = final_data[:, 4].astype(float)
x4 = final_data[:, 7].astype(float)
x5 = final_data[:, 5].astype(float)

x = pd.DataFrame({'Constant' : x2, 'Weight' : x1, 'Fuel efficiency (km/l)' : x4, 'Price' : x5})
#print("\nX:\n", x)

y_label = list(y.columns)[0]
print("\ny_label:", y_label)

x_labels = list(x.columns)
print("x_labels:", x_labels)

J = 3 # 3 discrete choices: El, Diesel, Benzin
print("\nJ:", J)

K = round(len(x_labels) / (J-1)) # J-1 since we only have covariates for the two 
print("K:", K)

N = final_data.shape[0]
print("N:", N)

y = y.values.reshape((N, ))
print("\ny:\n", y)
print("\ny's shape:", y.shape)

x = x.values.reshape((N, K, J-1))
print("\nx:\n", x)
print("\nx's shape:", x.shape)


theta = 0.1 * np.ones((K, J-1))
print("\ntheta:\n", theta)
print("\ntheta's shape:", theta.shape, "\n")


def util(x, thet): 
    N, K, J_1 = x.shape
    J = J_1 + 1 
    assert thet.size == K * (J-1)
    theta = thet.reshape((K, J-1)) # minimizer may flatten this 
        
    xb = (x * theta).sum(axis = 1) # (N,K,J-1) * (K,J-1), sum over k-axis -> (N,J-1)
    #print("\nxb:\n", xb)
    #print("\nxb's shape:", xb.shape)

    oo = np.zeros((N, 1)) # normalized alternative
    
    u = np.hstack([oo, xb]) # full N*J matrix of utilities 
    #print("\nu:\n", u)
    #print("u's shape:", u.shape)
    
    u -= u.max(axis = 1).reshape((N, 1)) # max rescale
    
    return u 


def ccp(x, theta): 
    N, K, J_1 = x.shape
    u = util(x, theta) # (N,J)

    denom = np.sum(np.exp(u), axis = 1).reshape((N, 1)) # (N,1)
    #print("\ndenom:\n", denom)

    ccp = np.exp(u) / denom # (N,J) matrix
    print("\nccp:\n", ccp)

    return ccp 


def loglike(y, x, theta): 
    N, K, J_1 = x.shape
    J = J_1 + 1 
    assert np.isin(y, np.arange(J)).all()
    
    u = util(x, theta)
    denom = np.sum(np.exp(u), axis = 1).reshape((N, 1))
    
    u_i = np.take_along_axis(u, y.reshape((N, 1)), axis = 1)
    
    ll_i = u_i - np.log(denom)

    return ll_i


def Q(theta): 
    ll_i = loglike(y, x, theta) # reads y,x from global memory 
    return -np.mean(ll_i)


theta0 = np.zeros((K, J-1))
res = minimize(Q, theta0)
print(f'Convergence success? {res.success} (after {res.nit} iterations).')
pd.DataFrame(res.x, index = x_labels, columns = ['coefficients'])