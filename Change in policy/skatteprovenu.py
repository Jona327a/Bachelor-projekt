import pandas as pd
import matplotlib.pyplot as plt
import afgiftspligtig_værdi as av
import requests as rq
from io import BytesIO
import matplotlib.ticker as mtick
import matplotlib as mpl

pd.options.display.float_format = '{:.4f}'.format
path = "https://raw.githubusercontent.com/Jona327a/Bachelor-projekt/main/Data/choice_data_subset.xlsx"

data = rq.get(path).content
data_set = pd.read_excel(BytesIO(data))

goal_seeks = av.afgiftspligtig_veardi(data_set)
data_set = data_set.assign(afgiftspligtig_værdi = goal_seeks)

def skatteprovenu(car_prices):
    skatteprovenu_lst = []
    sum_year_registrations = data_set.groupby('Year')['No. of registrations'].sum()
    aarstal = len(sum_year_registrations)
    J = data_set[['Year', 'key']].groupby('Year').count()
    for aar in range(0, aarstal):
        I = J.iloc[aar].tolist()[0]
        for i in range(0, I):
            car_i_markedsandele = data_set.loc[i, 'Markedsandele']
            car_i_skatteindtægt = car_prices.iloc[i] - data_set.loc[i, 'afgiftspligtig_værdi']
            skatteprovenu = car_i_markedsandele * sum_year_registrations.tolist()[aar] * car_i_skatteindtægt
            skatteprovenu_lst.append(skatteprovenu)
    return skatteprovenu_lst

original_prices = data_set['Prices (2015-DKK)']
skatteprovenu_original_prices = skatteprovenu(original_prices)
data_set = data_set.assign(skatteprovenu_original_prices = skatteprovenu_original_prices)

def new_prices(rate_1, rate_2, rate_3, reg_beløb_1, reg_beløb_2, bundfradrag, el_bundfradrag_1, el_fradrag_2, indfasning):
    new_prices = []
    for i in range(0, data_set.shape[0]):
        av_i = data_set.loc[i, 'afgiftspligtig_værdi']
        fuel_i = data_set.loc[i, 'Fuel']
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

#2030 registreringsafgift
#reg_afgift_increase = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 77094.65, reg_beløb_2 = 239721.34, bundfradrag = 25660.0, el_bundfradrag_1 = 137000.0, el_fradrag_2 = 0.0, indfasning = 0.80)

#2025 registreringsafgift
#reg_afgift_increase = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 69827.0, reg_beløb_2 = 217123.0, bundfradrag = 23241.0, el_bundfradrag_1 = 160000.0, el_fradrag_2 = 0.0, indfasning = 0.40)

#2020 registreringsafgift
reg_afgift_increase = new_prices(rate_1 = 0.25, rate_2 = 0.85, rate_3 = 1.5, reg_beløb_1 = 65000.0, reg_beløb_2 = 202200.0, bundfradrag = 21700.0, el_bundfradrag_1 = 170000.0, el_fradrag_2 = 1700.0, indfasning = 0.40)

data_set = data_set.assign(new_prices = reg_afgift_increase)
new_prices = data_set['new_prices']
skatteprovenu_new_prices = skatteprovenu(new_prices)
data_set = data_set.assign(skatteprovenu_new_prices = skatteprovenu_new_prices)

skatteprovenu_new_prices_data = data_set[['Year', 'skatteprovenu_new_prices', 'Fuel']].set_index(['Fuel'])
skatteprovenu_original_prices_data = data_set[['Year', 'skatteprovenu_original_prices', 'Fuel']].set_index(['Fuel'])

skatteprovenu_new_prices_benzin_data = skatteprovenu_new_prices_data.loc['Benzin']
skatteprovenu_new_prices_benzin_sum = skatteprovenu_new_prices_benzin_data.groupby('Year')['skatteprovenu_new_prices'].sum()
print("\nSkatteprovenu af new_prices for benzinbiler:\n", (skatteprovenu_new_prices_benzin_sum.sum() / 1000) / 15 )

skatteprovenu_new_prices_diesel_data = skatteprovenu_new_prices_data.loc['Diesel']
skatteprovenu_new_prices_diesel_sum = skatteprovenu_new_prices_diesel_data.groupby('Year')['skatteprovenu_new_prices'].sum()
print("\nSkatteprovenu af new_prices for dieselbiler:\n", (skatteprovenu_new_prices_diesel_sum.sum() / 1000) / 15 )

skatteprovenu_new_prices_el_data = skatteprovenu_new_prices_data.loc['El']
skatteprovenu_new_prices_el_sum = skatteprovenu_new_prices_el_data.groupby('Year')['skatteprovenu_new_prices'].sum()
print("\nSkatteprovenu af new_prices for elbiler:\n", (skatteprovenu_new_prices_el_sum.sum() / 1000) / 15)
