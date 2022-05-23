import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# Loading the datasets
bilbasen_data_subset = pd.read_csv(path + 'bilbasen_data_subset.csv', delimiter = ',', encoding = 'unicode_escape')
print("bilbasen_data_subset:\n", bilbasen_data_subset)

choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
print("choice_data:\n", choice_data)

afgiftspligtig_data = pd.read_excel(path + 'afgiftspligtig_data.xlsx')
print("afgiftspligtig_data:\n", afgiftspligtig_data)

markedsandele_data = pd.read_excel(path + 'markedsandele_data.xlsx')
print("markedsandele_data:\n", markedsandele_data)

# MAKING SIZE (m3) PLOT
size_data = choice_data[['Year', 'Size (m3)', 'Fuel']].set_index(['Fuel'])
print("\nSize data for plotting:\n", size_data)

size_el_data = size_data.loc['El']
size_el_means = size_el_data.groupby('Year')['Size (m3)'].mean()
print("\nSize EL means:\n", size_el_means)

size_benzin_data = size_data.loc['Benzin']
size_benzin_means = size_benzin_data.groupby('Year')['Size (m3)'].mean()
print("\nSize Benzin means :\n", size_benzin_means)

size_diesel_data = size_data.loc['Diesel']
size_diesel_means = size_diesel_data.groupby('Year')['Size (m3)'].mean()
print("\nSize Diesel means :\n", size_diesel_means)

plt.plot(list(size_el_data['Year'].drop_duplicates()), size_el_means, color = 'g', label = 'El')
plt.plot(list(size_benzin_data['Year'].drop_duplicates()), size_benzin_means, color = 'r', label = 'Benzin')
plt.plot(list(size_diesel_data['Year'].drop_duplicates()), size_diesel_means, color = 'b', label = 'Diesel')
plt.ylim(ymin = 10, ymax = 14)

plt.xlabel("År")
plt.ylabel("m3")
  
plt.legend()
plt.grid()
plt.show()

# MAKING PRICES (2015-DKK)
price_data = choice_data[['Year', 'Prices (2015-DKK)', 'Fuel']].set_index(['Fuel'])
print("\nPrice data for plotting:\n", price_data)

price_el_data = price_data.loc['El']
price_el_means = price_el_data.groupby('Year')['Prices (2015-DKK)'].mean()
print("\nPrice EL means:\n", price_el_means)

price_benzin_data = price_data.loc['Benzin']
price_benzin_means = price_benzin_data.groupby('Year')['Prices (2015-DKK)'].mean()
print("\nPrice Benzin means :\n", price_benzin_means)

price_diesel_data = price_data.loc['Diesel']
price_diesel_means = price_diesel_data.groupby('Year')['Prices (2015-DKK)'].mean()
print("\nPrice Diesel means :\n", price_diesel_means)

plt.plot(list(price_el_data['Year'].drop_duplicates()), price_el_means, color = 'g', label = 'El')
plt.plot(list(price_benzin_data['Year'].drop_duplicates()), price_benzin_means, color = 'r', label = 'Benzin')
plt.plot(list(price_diesel_data['Year'].drop_duplicates()), price_diesel_means, color = 'b', label = 'Diesel')
plt.ylim(ymin = 0, ymax = 900000)

plt.xlabel("År")
plt.ylabel("Priser i DKK")
  
plt.legend()
plt.grid()
plt.show()

# MAKING Cost/km (DKK)
cost_data = choice_data[['Year', 'Cost/km (DKK)', 'Fuel']].set_index(['Fuel'])
print("\nCost/km data for plotting:\n", cost_data)

cost_el_data = cost_data.loc['El']
cost_el_means = cost_el_data.groupby('Year')['Cost/km (DKK)'].mean()
print("\nCost/km EL means:\n", cost_el_means)

cost_benzin_data = cost_data.loc['Benzin']
cost_benzin_means = cost_benzin_data.groupby('Year')['Cost/km (DKK)'].mean()
print("\nCost/km Benzin means :\n", cost_benzin_means)

cost_diesel_data = cost_data.loc['Diesel']
cost_diesel_means = cost_diesel_data.groupby('Year')['Cost/km (DKK)'].mean()
print("\nCost/km Diesel means :\n", cost_diesel_means)

plt.plot(list(cost_el_data['Year'].drop_duplicates()), cost_el_means, color = 'g', label = 'El')
plt.plot(list(cost_benzin_data['Year'].drop_duplicates()), cost_benzin_means, color = 'r', label = 'Benzin')
plt.plot(list(cost_diesel_data['Year'].drop_duplicates()), cost_diesel_means, color = 'b', label = 'Diesel')
#plt.ylim(ymin = 0, ymax = 900000)

plt.xlabel("År")
plt.ylabel("Omkostninger per km i DKK")
  
plt.legend()
plt.grid()
plt.show()

# MAKING afgiftspligtig værdi
afgiftspligtig_værdi_data = afgiftspligtig_data[['Year', 'afgiftspligtig_værdi', 'Fuel']].set_index(['Fuel'])
print("\nAfgiftspligtig_værdi data for plotting:\n", afgiftspligtig_værdi_data)

afgiftspligtig_værdi_el_data = afgiftspligtig_værdi_data.loc['El']
afgiftspligtig_værdi_el_means = afgiftspligtig_værdi_el_data.groupby('Year')['afgiftspligtig_værdi'].mean()
print("\nAfgiftspligtig_værdi EL means:\n", afgiftspligtig_værdi_el_means)

afgiftspligtig_værdi_benzin_data = afgiftspligtig_værdi_data.loc['Benzin']
afgiftspligtig_værdi_benzin_means = afgiftspligtig_værdi_benzin_data.groupby('Year')['afgiftspligtig_værdi'].mean()
print("\nAfgiftspligtig_værdi Benzin means :\n", afgiftspligtig_værdi_benzin_means)

afgiftspligtig_værdi_diesel_data = afgiftspligtig_værdi_data.loc['Diesel']
afgiftspligtig_værdi_diesel_means = afgiftspligtig_værdi_diesel_data.groupby('Year')['afgiftspligtig_værdi'].mean()
print("\nAfgiftspligtig_værdi Diesel means :\n", afgiftspligtig_værdi_diesel_means)

plt.plot(list(afgiftspligtig_værdi_el_data['Year'].drop_duplicates()), afgiftspligtig_værdi_el_means, color = 'g', label = 'El')
plt.plot(list(afgiftspligtig_værdi_benzin_data['Year'].drop_duplicates()), afgiftspligtig_værdi_benzin_means, color = 'r', label = 'Benzin')
plt.plot(list(afgiftspligtig_værdi_diesel_data['Year'].drop_duplicates()), afgiftspligtig_værdi_diesel_means, color = 'b', label = 'Diesel')
plt.ylim(ymin = 0, ymax = 900000)

plt.xlabel("År")
plt.ylabel("Afgiftspligtig værdi i DKK")
  
plt.legend()
plt.grid()
plt.show()

# MAKING FUEL EFFICIENCY PLOT
fe_data = bilbasen_data_subset[['aargang', 'kmL', 'drivkraft']].set_index(['drivkraft'])
print("\nFE data for plotting:\n", fe_data)

fe_el_data = fe_data.loc['El']
fe_el_means = fe_el_data.groupby('aargang')['kmL'].mean()
print("\nFE EL means:\n", fe_el_means)

fe_benzin_data = fe_data.loc['Benzin']
fe_benzin_means = fe_benzin_data.groupby('aargang')['kmL'].mean()
print("\nFE Benzin means:\n", fe_benzin_means)

fe_diesel_data = fe_data.loc['Diesel']
fe_diesel_means = fe_diesel_data.groupby('aargang')['kmL'].mean()
print("\nFE Diesel means:\n", fe_diesel_means)

fig, ax1 = plt.subplots()

ax1.set_xlabel('År')
ax1.set_ylabel('km (elbiler)', color = 'black') 
plot_1 = ax1.plot(fe_el_data['aargang'].drop_duplicates().sort_values(), fe_el_means, color = 'green', label = 'El') 
ax1.tick_params(axis ='y', labelcolor = 'black') 
ax1.set_ylim([0, 500])

ax2 = ax1.twinx()
ax2.set_ylabel('km/l (benzin- eller dieselbiler)', color = 'black') 
plot_2 = ax2.plot(fe_benzin_data['aargang'].drop_duplicates().sort_values(), fe_benzin_means, color = 'red', label = 'Benzin') 
ax2.tick_params(axis ='y', labelcolor = 'black')
ax2.set_ylim([0, 25])

plot_3 = plt.plot(fe_diesel_data['aargang'].drop_duplicates().sort_values(), fe_diesel_means, color = 'blue', label = 'Diesel') 

lns = plot_1 + plot_2 + plot_3
labels = [l.get_label() for l in lns]

plt.legend(lns, labels, loc = 0)

ax1.grid()
plt.show()

# MAKING Markedsandele
markedsandele_data = markedsandele_data[['Year', 'Markedsandele', 'Fuel']].set_index(['Fuel'])
print("\nMarkedsandele data for plotting:\n", markedsandele_data)

markedsandele_el_data = markedsandele_data.loc['El']
markedsandele_el_means = markedsandele_el_data.groupby('Year')['Markedsandele'].sum()
print("\nMarkedsandele EL means:\n", markedsandele_el_means)

markedsandele_benzin_data = markedsandele_data.loc['Benzin']
markedsandele_benzin_means = markedsandele_benzin_data.groupby('Year')['Markedsandele'].sum()
print("\nMarkedsandele Benzin means :\n", markedsandele_benzin_means)

markedsandele_diesel_data = markedsandele_data.loc['Diesel']
markedsandele_diesel_means = markedsandele_diesel_data.groupby('Year')['Markedsandele'].sum()
print("\nMarkedsandele Diesel means :\n", markedsandele_diesel_means)

fig, ax1 = plt.subplots()

ax1.set_xlabel('År')
ax1.set_ylabel('Markedsandele (elbiler)', color = 'black') 
plot_1 = ax1.plot(markedsandele_el_data['Year'].drop_duplicates(), markedsandele_el_means, color = 'g', label = 'El')
ax1.tick_params(axis ='y', labelcolor = 'black') 
ax1.set_ylim([0.0, 0.10])

ax2 = ax1.twinx()
ax2.set_ylabel('Markedsandele (benzin- eller dieselbiler)', color = 'black') 
plot_2 = ax2.plot(markedsandele_benzin_data['Year'].drop_duplicates(), markedsandele_benzin_means, color = 'r', label = 'Benzin')
ax2.tick_params(axis ='y', labelcolor = 'black')
ax2.set_ylim([0.0, 1.0])

plot_3 = plt.plot(markedsandele_diesel_data['Year'].drop_duplicates(), markedsandele_diesel_means, color = 'b', label = 'Diesel')

lns = plot_1 + plot_2 + plot_3
labels = [l.get_label() for l in lns]

plt.legend(lns, labels, loc = 0)

ax1.grid()
plt.show()

# MAKING WEIGHT (kg) PLOT
x1 = []
x2 = []
x3 = []
x4 = []
x5 = [] 
x6 = [] 
x7 = [] 
x8 = []
x9 = [] 
x10 = []
x11 = []
x12 = []
x13 = []
x14 = []
x15 = []

for i in choice_data.index:
    weight_check = choice_data['Weight (kg)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Diesel' and year_check == 2006:
        x1.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2007:
        x2.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2008:
        x3.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2009:
        x4.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2010:
        x5.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2011:
        x6.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2012:
        x7.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2013:
        x8.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2014:
        x9.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2015:
        x10.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2016:
        x11.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2017:
        x12.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2018:
        x13.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2019:
        x14.append(weight_check)
    if fuel_check == 'Diesel' and year_check == 2020:
        x15.append(weight_check)

weight_diesel = [np.average(x1),
                 np.average(x2),
                 np.average(x3),
                 np.average(x4),
                 np.average(x5),
                 np.average(x6),
                 np.average(x7),
                 np.average(x8),
                 np.average(x9),
                 np.average(x10),
                 np.average(x11),
                 np.average(x12),
                 np.average(x13),
                 np.average(x14),
                 np.average(x15)]

y1 = []
y2 = []
y3 = []
y4 = []
y5 = [] 
y6 = [] 
y7 = [] 
y8 = []
y9 = [] 
y10 = []
y11 = []
y12 = []
y13 = []
y14 = []
y15 = []

for i in choice_data.index:
    weight_check = choice_data['Weight (kg)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Benzin' and year_check == 2006:
        y1.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2007:
        y2.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2008:
        y3.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2009:
        y4.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2010:
        y5.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2011:
        y6.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2012:
        y7.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2013:
        y8.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2014:
        y9.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2015:
        y10.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2016:
        y11.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2017:
        y12.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2018:
        y13.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2019:
        y14.append(weight_check)
    if fuel_check == 'Benzin' and year_check == 2020:
        y15.append(weight_check)

weight_gasoline = [np.average(y1), 
                   np.average(y2), 
                   np.average(y3), 
                   np.average(y4), 
                   np.average(y5), 
                   np.average(y6), 
                   np.average(y7),
                   np.average(y8), 
                   np.average(y9), 
                   np.average(y10), 
                   np.average(y11), 
                   np.average(y12), 
                   np.average(y13),
                   np.average(y14), 
                   np.average(y15)]

z1 = []
z2 = []
z3 = []
z4 = []
z5 = [] 
z6 = [] 
z7 = [] 
z8 = []
z9 = [] 
z10 = []
z11 = []
z12 = []
z13 = []
z14 = []
z15 = []

for i in choice_data.index:
    weight_check = choice_data['Weight (kg)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'El' and year_check == 2006:
        z1.append(weight_check)
    if fuel_check == 'El' and year_check == 2007:
        z2.append(weight_check)
    if fuel_check == 'El' and year_check == 2008:
        z3.append(weight_check)
    if fuel_check == 'El' and year_check == 2009:
        z4.append(weight_check)
    if fuel_check == 'El' and year_check == 2010:
        z5.append(weight_check)
    if fuel_check == 'El' and year_check == 2011:
        z6.append(weight_check)
    if fuel_check == 'El' and year_check == 2012:
        z7.append(weight_check)
    if fuel_check == 'El' and year_check == 2013:
        z8.append(weight_check)
    if fuel_check == 'El' and year_check == 2014:
        z9.append(weight_check)
    if fuel_check == 'El' and year_check == 2015:
        z10.append(weight_check)
    if fuel_check == 'El' and year_check == 2016:
        z11.append(weight_check)
    if fuel_check == 'El' and year_check == 2017:
        z12.append(weight_check)
    if fuel_check == 'El' and year_check == 2018:
        z13.append(weight_check)
    if fuel_check == 'El' and year_check == 2019:
        z14.append(weight_check)
    if fuel_check == 'El' and year_check == 2020:
        z15.append(weight_check)

weight_EV = [np.average(z1), 
             np.average(z2), 
             np.average(z3), 
             np.average(z4), 
             np.average(z5),
             np.average(z6), 
             np.average(z7),
             np.average(z8), 
             np.average(z9), 
             np.average(z10), 
             np.average(z11), 
             np.average(z12), 
             np.average(z13),
             np.average(z14), 
             np.average(z15)]

year = np.array([2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

plt.xlabel("År")
plt.ylabel("Kilo")

plt.plot(year, weight_diesel, label = "Diesel", color= "blue")
plt.plot(year, weight_gasoline, label = "Benzin", color = "red")
plt.plot(year, weight_EV, label = "El", color = "green")

plt.ylim([1600, 2400])

plt.legend()
plt.grid()

plt.show()

# MAKING Engine effect (kW) PLOT
a1 = []
a2 = []
a3 = []
a4 = []
a5 = [] 
a6 = [] 
a7 = [] 
a8 = []
a9 = [] 
a10 = []
a11 = []
a12 = []
a13 = []
a14 = []
a15 = []

for i in choice_data.index:
    engine_effect = choice_data['Engine effect (kW)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Benzin' and year_check == 2006:
        a1.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2007:
        a2.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2008:
        a3.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2009:
        a4.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2010:
        a5.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2011:
        a6.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2012:
        a7.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2013:
        a8.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2014:
        a9.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2015:
        a10.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2016:
        a11.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2017:
        a12.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2018:
        a13.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2019:
        a14.append(engine_effect)
    if fuel_check == 'Benzin' and year_check == 2020:
        a15.append(engine_effect)

effect_gasoline = [np.average(a1), 
                   np.average(a2), 
                   np.average(a3), 
                   np.average(a4), 
                   np.average(a5), 
                   np.average(a6), 
                   np.average(a7),
                   np.average(a8), 
                   np.average(a9), 
                   np.average(a10), 
                   np.average(a11), 
                   np.average(a12), 
                   np.average(a13),
                   np.average(a14), 
                   np.average(a15)]

b1 = []
b2 = []
b3 = []
b4 = []
b5 = [] 
b6 = [] 
b7 = [] 
b8 = []
b9 = [] 
b10 = []
b11 = []
b12 = []
b13 = []
b14 = []
b15 = []

for i in choice_data.index:
    engine_effect = choice_data['Engine effect (kW)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Diesel' and year_check == 2006:
        b1.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2007:
        b2.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2008:
        b3.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2009:
        b4.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2010:
        b5.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2011:
        b6.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2012:
        b7.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2013:
        b8.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2014:
        b9.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2015:
        b10.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2016:
        b11.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2017:
        b12.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2018:
        b13.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2019:
        b14.append(engine_effect)
    if fuel_check == 'Diesel' and year_check == 2020:
        b15.append(engine_effect)

effect_diesel = [np.average(b1), 
                   np.average(b2), 
                   np.average(b3), 
                   np.average(b4), 
                   np.average(b5), 
                   np.average(b6), 
                   np.average(b7),
                   np.average(b8), 
                   np.average(b9), 
                   np.average(b10), 
                   np.average(b11), 
                   np.average(b12), 
                   np.average(b13),
                   np.average(b14), 
                   np.average(b15)]

c1 = []
c2 = []
c3 = []
c4 = []
c5 = [] 
c6 = [] 
c7 = [] 
c8 = []
c9 = [] 
c10 = []
c11 = []
c12 = []
c13 = []
c14 = []
c15 = []

for i in choice_data.index:
    weight_check = choice_data['Engine effect (kW)'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'El' and year_check == 2006:
        c1.append(weight_check)
    if fuel_check == 'El' and year_check == 2007:
        c2.append(weight_check)
    if fuel_check == 'El' and year_check == 2008:
        c3.append(weight_check)
    if fuel_check == 'El' and year_check == 2009:
        c4.append(weight_check)
    if fuel_check == 'El' and year_check == 2010:
        c5.append(weight_check)
    if fuel_check == 'El' and year_check == 2011:
        c6.append(weight_check)
    if fuel_check == 'El' and year_check == 2012:
        c7.append(weight_check)
    if fuel_check == 'El' and year_check == 2013:
        c8.append(weight_check)
    if fuel_check == 'El' and year_check == 2014:
        c9.append(weight_check)
    if fuel_check == 'El' and year_check == 2015:
        c10.append(weight_check)
    if fuel_check == 'El' and year_check == 2016:
        c11.append(weight_check)
    if fuel_check == 'El' and year_check == 2017:
        c12.append(weight_check)
    if fuel_check == 'El' and year_check == 2018:
        c13.append(weight_check)
    if fuel_check == 'El' and year_check == 2019:
        c14.append(weight_check)
    if fuel_check == 'El' and year_check == 2020:
        c15.append(weight_check)

effect_EV = [np.average(c1), 
             np.average(c2), 
             np.average(c3),
             np.average(c4),
             np.average(c5),
             np.average(c6),
             np.average(c7),
             np.average(c8),
             np.average(c9),
             np.average(c10),
             np.average(c11),
             np.average(c12),
             np.average(c13),
             np.average(c14),
             np.average(c15)]

plt.xlabel("År")
plt.ylabel("kW")

plt.plot(year, effect_gasoline, label = "Benzin", color = "red")
plt.plot(year, effect_diesel, label = "Diesel", color= "blue")
plt.plot(year, effect_EV, label = "El", color = "green")

plt.ylim([25, 220])

plt.legend()
plt.grid()

plt.show()

# MAKING No. of registrations PLOT
d1 = []
d2 = []
d3 = []
d4 = []
d5 = [] 
d6 = [] 
d7 = [] 
d8 = []
d9 = [] 
d10 = []
d11 = []
d12 = []
d13 = []
d14 = []
d15 = []

for i in choice_data.index:
    registration_check = choice_data['No. of registrations'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'El' and year_check == 2006:
        d1.append(registration_check)
    if fuel_check == 'El' and year_check == 2007:
        d2.append(registration_check)
    if fuel_check == 'El' and year_check == 2008:
        d3.append(registration_check)
    if fuel_check == 'El' and year_check == 2009:
        d4.append(registration_check)
    if fuel_check == 'El' and year_check == 2010:
        d5.append(registration_check)
    if fuel_check == 'El' and year_check == 2011:
        d6.append(registration_check)
    if fuel_check == 'El' and year_check == 2012:
        d7.append(registration_check)
    if fuel_check == 'El' and year_check == 2013:
        d8.append(registration_check)
    if fuel_check == 'El' and year_check == 2014:
        d9.append(registration_check)
    if fuel_check == 'El' and year_check == 2015:
        d10.append(registration_check)
    if fuel_check == 'El' and year_check == 2016:
        d11.append(registration_check)
    if fuel_check == 'El' and year_check == 2017:
        d12.append(registration_check)
    if fuel_check == 'El' and year_check == 2018:
        d13.append(registration_check)
    if fuel_check == 'El' and year_check == 2019:
        d14.append(registration_check)
    if fuel_check == 'El' and year_check == 2020:
        d15.append(registration_check)

number_reg_EV = [np.average(d1), 
             np.average(d2), 
             np.average(d3),
             np.average(d4),
             np.average(d5),
             np.average(d6),
             np.average(d7),
             np.average(d8),
             np.average(d9),
             np.average(d10),
             np.average(d11),
             np.average(d12),
             np.average(d13),
             np.average(d14),
             np.average(d15)]

e1 = []
e2 = []
e3 = []
e4 = []
e5 = [] 
e6 = [] 
e7 = [] 
e8 = []
e9 = [] 
e10 = []
e11 = []
e12 = []
e13 = []
e14 = []
e15 = []

for i in choice_data.index:
    registration_check = choice_data['No. of registrations'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Benzin' and year_check == 2006:
        e1.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2007:
        e2.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2008:
        e3.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2009:
        e4.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2010:
        e5.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2011:
        e6.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2012:
        e7.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2013:
        e8.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2014:
        e9.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2015:
        e10.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2016:
        e11.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2017:
        e12.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2018:
        e13.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2019:
        e14.append(registration_check)
    if fuel_check == 'Benzin' and year_check == 2020:
        e15.append(registration_check)

number_reg_Benzin = [np.average(e1), 
             np.average(e2), 
             np.average(e3),
             np.average(e4),
             np.average(e5),
             np.average(e6),
             np.average(e7),
             np.average(e8),
             np.average(e9),
             np.average(e10),
             np.average(e11),
             np.average(e12),
             np.average(e13),
             np.average(e14),
             np.average(e15)]

f1 = []
f2 = []
f3 = []
f4 = []
f5 = [] 
f6 = [] 
f7 = [] 
f8 = []
f9 = [] 
f10 = []
f11 = []
f12 = []
f13 = []
f14 = []
f15 = []

for i in choice_data.index:
    registration_check = choice_data['No. of registrations'].iloc[i]
    fuel_check = choice_data['Fuel'].iloc[i]
    year_check = choice_data['Year'].iloc[i]
    if fuel_check == 'Diesel' and year_check == 2006:
        f1.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2007:
        f2.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2008:
        f3.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2009:
        f4.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2010:
        f5.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2011:
        f6.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2012:
        f7.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2013:
        f8.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2014:
        f9.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2015:
        f10.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2016:
        f11.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2017:
        f12.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2018:
        f13.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2019:
        f14.append(registration_check)
    if fuel_check == 'Diesel' and year_check == 2020:
        f15.append(registration_check)

number_reg_Diesel = [np.average(f1), 
             np.average(f2), 
             np.average(f3),
             np.average(f4),
             np.average(f5),
             np.average(f6),
             np.average(f7),
             np.average(f8),
             np.average(f9),
             np.average(f10),
             np.average(f11),
             np.average(f12),
             np.average(f13),
             np.average(f14),
             np.average(f15)]

plt.xlabel("År")
plt.ylabel("Antal registreringer")

plt.plot(year, number_reg_Benzin, label = "Benzin", color = "red")
plt.plot(year, number_reg_Diesel, label = "Diesel", color= "blue")
plt.plot(year, number_reg_EV, label = "El", color = "green")

plt.ylim([0, 1700])

plt.legend()
plt.grid()

plt.savefig('plot_registrations')

plt.show()
