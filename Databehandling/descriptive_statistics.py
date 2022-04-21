import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.4f}'.format
path = "/Users/frederikluneborgholmjeppesen/Documents/Universitetet/3. år/Bachelorprojektet/MotorRegisterData-main/"

# Loading the datasets
combined_data = pd.read_excel(path + 'combined_data.xlsx')
print("combined_data:\n", combined_data)

choice_data = pd.read_csv(path + 'choice_data.csv', delimiter = ';', encoding = 'unicode_escape')
print("choice_data:\n", choice_data)

# MAKING FUEL EFFICIENCY PLOT
fe_data = combined_data[['Year', 'kmL', 'Fuel']].set_index(['Fuel'])
print("\nFE data for plotting:\n", fe_data)

fe_el_data = fe_data.loc['El']
fe_el_means = fe_el_data.groupby('Year')['kmL'].mean()
print("\nFE EL means:\n", fe_el_means)

fe_benzin_data = fe_data.loc['Benzin']
fe_benzin_means = fe_benzin_data.groupby('Year')['kmL'].mean()
print("\nFE Benzin means :\n", fe_benzin_means)

fe_diesel_data = fe_data.loc['Diesel']
fe_diesel_means = fe_diesel_data.groupby('Year')['kmL'].mean()
print("\nFE Diesel means :\n", fe_diesel_means)

fig, ax1 = plt.subplots()

ax1.set_xlabel('Years')
ax1.set_ylabel('km - EL', color = 'black') 
plot_1 = ax1.plot(list(fe_el_data['Year'].drop_duplicates()), fe_el_means, color = 'green', label = 'EL') 
ax1.tick_params(axis ='y', labelcolor = 'black') 

ax2 = ax1.twinx()
ax2.set_ylabel('km/l - Benzin/Diesel', color = 'black') 
plot_2 = ax2.plot(list(fe_benzin_data['Year'].drop_duplicates()), fe_benzin_means, color = 'red', label = 'Benzin') 
ax2.tick_params(axis ='y', labelcolor = 'black')

plot_3 = plt.plot(list(fe_diesel_data['Year'].drop_duplicates()), fe_diesel_means, color = 'blue', label = 'Diesel') 

lns = plot_1 + plot_2 + plot_3
labels = [l.get_label() for l in lns]
plt.legend(lns, labels, loc = 0)

plt.show()

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

plt.plot(list(size_el_data['Year'].drop_duplicates()), size_el_means, color = 'g', label = 'EL')
plt.plot(list(size_benzin_data['Year'].drop_duplicates()), size_benzin_means, color = 'r', label = 'Benzin')
plt.plot(list(size_diesel_data['Year'].drop_duplicates()), size_diesel_means, color = 'b', label = 'Diesel')

plt.xlabel("Years")
plt.ylabel("m3")
plt.title("Size")
  
plt.legend()
plt.show()

