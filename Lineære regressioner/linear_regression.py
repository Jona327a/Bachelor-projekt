import numpy as np
import pandas as pd
import LinearModels as LM

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# NOTICE: remember to choose the correct dataset
dataset = pd.read_excel(path + 'combined_data.xlsx')
dataset['Fuel'].replace(['El', 'Benzin', 'Diesel'], [0, 1, 2], inplace = True)
print("Dataset:\n", dataset)

# MAKING LINEAR REGRESSION
dataset = dataset.values

y = dataset[:, 1].astype(float)
y = pd.DataFrame({'Shares' : y})
print("\ny:\n", y)

x1 = dataset[:, 2].astype(str)
x2 = np.ones(x1.shape).astype(float)
x3 = dataset[:, 3].astype(float)
x4 = dataset[:, 4].astype(float)
x5 = dataset[:, 7].astype(float)
x6 = dataset[:, 5].astype(float)

x = pd.DataFrame({'Constant' : x2, 'Fuel' : x1, 'Weight' : x3, 'Engine effect' : x4, 'Fuel efficiency (km/l)' : x5, 'Price' : x6})
x = pd.get_dummies(data = x, drop_first = True)
print("\nX:\n", x)

y_label = list(y.columns)[0]
print("\ny_label:", y_label)

x_labels = list(x.columns)
print("x_labels:", x_labels)

y = np.array(y)
#print("y:\n", y)

x = np.array(x)
#print("X:\n", x)

pols = LM.estimate(y, x, robust_se = True)

print("\n")
LM.print_table((y_label, x_labels), pols, title = "Linear regression", floatfmt = '.15f')

