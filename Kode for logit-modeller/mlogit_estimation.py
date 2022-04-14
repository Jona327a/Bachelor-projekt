import NonLinearModels_mlogit as NLM_mlogit
import numpy as np
import pandas as pd

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# Final data
final_data = pd.read_excel(path + 'final_data.xlsx')
final_data.drop(columns = final_data.columns[0], axis = 1, inplace = True)
final_data['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
print("Dataset:\n", final_data)

# Multinominal logit estimation
final_data = final_data.values

y = final_data[:, 2].astype(int)
y = pd.DataFrame({'y' : y})
#print("\ny:\n", y)

x1 = final_data[:, 3].astype(float)
x2 = np.ones(x1.shape).astype(float)
x3 = final_data[:, 4].astype(float)
x4 = final_data[:, 7].astype(float)
x5 = final_data[:, 5].astype(float)

x = pd.DataFrame({'Constant' : x2, 'Weight' : x1, 'Engine effect' : x3, 'Fuel efficiency (km/l)' : x4, 'Price' : x5})
#print("\nX:\n", x)

y_label = list(y.columns)[0]
print("\ny_label:", y_label)

x_labels = list(x.columns)
print("x_labels:", x_labels)

y = np.array(y)
print("\ny:\n", y)
print("\ny's shape:", y.shape)

x = np.array(x)
print("\nX:\n", x)
print("\nX's shape:", x.shape)

k = x.shape[1]
print("\nThe amount of explanatory variables:", k)
j = 3
print("Number of choices:", j)

theta0 = np.zeros((k, j-1))
print("\ntheta0:\n", theta0)
print("\ntheta0's shape:", theta0.shape, "\n")

sim_result = NLM_mlogit.estimate(NLM_mlogit.mlogit, theta0, y, x)
NLM_mlogit.print_table((y_label, x_labels), sim_result)

