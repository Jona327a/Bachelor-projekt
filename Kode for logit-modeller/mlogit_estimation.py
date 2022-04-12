import NonLinearModels_mlogit as NLM_mlogit
import numpy as np
import pandas as pd

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# CHOICE DATA
final_data = pd.read_excel(path + 'final_data.xlsx')
final_data['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
print("Dataset:", final_data)

# Multinominal logit estimation
j = 3
print("Number of choices:", j)

theta0 = np.zeros((j-1, j-1))
print("theta0:", theta0)

final_data = final_data.values

y = final_data[:, 3].astype(int)
y = pd.DataFrame({'y' : y})
print("\ny:\n", y)

x1 = final_data[:, 4].astype(float)
x2 = np.ones(x1.shape).astype(float)
x3 = final_data[:, 5].astype(float)
x4 = final_data[:, 8].astype(float)
x5 = final_data[:, 6].astype(float)

x = pd.DataFrame({'Constant' : x2, 'Weight' : x1, 'Engine effect' : x3, 'Fuel efficiency (km/l)' : x4, 'Price' : x5})
print("\nX:\n", x)

y_label = list(y.columns)[0]
print("\ny_label:", y_label)

x_labels = list(x.columns)
print("x_labels:", x_labels)

y = np.array(y)
x = np.array(x)

sim_result = NLM_mlogit.estimate(NLM_mlogit.mlogit, theta0, y, x)
NLM_mlogit.print_table((y_label, x_labels), sim_result)

