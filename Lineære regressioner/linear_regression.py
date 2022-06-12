import numpy as np
import pandas as pd
import LinearModels as LM
import requests as rq
from io import BytesIO

pd.options.display.float_format = '{:.4f}'.format
path = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"

data = rq.get(path).content
dataset = pd.read_excel(BytesIO(data))

# Changing the measure of 'Prices (2015-DKK)' into log in 100000 kr.
dataset['Prices (2015-DKK)'] = np.log(dataset['Prices (2015-DKK)'] / 100000)

# Changing the measure of 'Weight (kg)' into tons
dataset['Weight (kg)'] = dataset['Weight (kg)'] / 1000

# Changing the measure of 'Engine effect' into 100 kW
dataset['Engine effect (kW)'] = dataset['Engine effect (kW)'] / 100

print("Dataset:\n", dataset)

y = dataset['Markedsandele'].values.astype(float)
y = pd.DataFrame({'Markedsandele' : y})
print("\ny:\n", y)

x1 = dataset['Weight (kg)'].values.astype(float)
x2 = np.ones(x1.shape).astype(float)
x3 = dataset['Engine effect (kW)'].values.astype(float)
x4 = dataset['Size (m3)'].values.astype(float)
x5 = dataset['Prices (2015-DKK)'].values.astype(float)
x6 = dataset['Cost/km (DKK)'].values.astype(float) #
x7 = dataset['Fuel'].values.astype(str)

x = pd.DataFrame({'Konstant' : x2, 'Vægt (tons)' : x1, 'Bilmotorens effekt (100 kW)' : x3, 'Størrelse (m3)' : x4, 'log(Priser) (100.000 DKK)' : x5, 'Omkostninger/km (DKK)' : x6, 'Drivkraft': x7})
x = pd.get_dummies(data = x, drop_first = True)
print("\nX:\n", x)

y_label = list(y.columns)[0]
print("\ny_label:", y_label)
x_labels = list(x.columns)
print("x_labels:", x_labels)

y = np.array(y)
print("\ny:\n", y)
x = np.array(x)
print("\nX:\n", x)

pols = LM.estimate(y, x, robust_se = True)

print("\n")
table = LM.print_table((y_label, x_labels), pols, title = "Lineær regression", floatfmt='.4f')
