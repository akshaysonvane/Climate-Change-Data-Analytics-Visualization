import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from   sklearn import linear_model
import warnings
warnings.filterwarnings("ignore")


# Load data GlobalTemperatures

def Visualization():
    colnames    = ['dt', 'LandAverageTemperature', 'LandAverageTemperatureUncertainty']
    newnames    = ['dt', 'at', 'atu']
    datatypes   = {'dt': 'str','at':'float32','atu':'float32'}
    temperature = pd.read_csv("Data/GlobalTemperatures.csv", 
                                usecols = colnames, 
                                dtype = datatypes)

    temperature.columns = newnames
    temperature = temperature[pd.notnull(temperature['at'])]
    temperature['dt'] = temperature['dt'].map(lambda x: int(x.split('-')[0]))
    group = temperature.groupby('dt').mean()



    plt.figure(figsize=(8,6))
    plt.scatter(group.index, group['at'], s=40, c='darkblue', alpha=0.5, linewidths=0, label='Mean Temperature')
    plt.legend(loc='upper left')
    plt.xlabel('Year')
    plt.ylabel('Temperature')
    plt.title('Mean of temperature by years')
    plt.savefig('temperature.png')


    indian_cities = {'Ahmadabad', 'Bangalore' , 'Bombay' , 'Kanpur', 'Lakhnau', 'Nagpur', 'Madras','Pune', 'Calcutta' , 'Surat', 'New Delhi', 'Jaipur', 'Hyderabad'}
    global_temp = pd.read_csv('Data/GlobalLandTemperaturesByMajorCity.csv')

    # drop unnecessary columns
    global_temp = global_temp[['dt', 'City', 'AverageTemperature']]

    global_temp['dt'] = pd.to_datetime(global_temp['dt'])
    global_temp['year'] = global_temp['dt'].map(lambda x: x.year)
    global_temp['month'] = global_temp['dt'].map(lambda x: x.month)
    global_temp['City'] = global_temp['City']

    min_year = global_temp['year'].min()
    max_year = global_temp['year'].max()
    years = range(min_year, max_year + 1)

    global_temp['season'] = global_temp['month'].apply(get_season)

    spring_temps = []
    summer_temps = []
    autumn_temps = []
    winter_temps = []

    for year in years:
        curr_years_data = global_temp[global_temp['year'] == year]
        spring_temps.append(curr_years_data[curr_years_data['season'] == 'spring']['AverageTemperature'].mean())
        summer_temps.append(curr_years_data[curr_years_data['season'] == 'summer']['AverageTemperature'].mean())
        autumn_temps.append(curr_years_data[curr_years_data['season'] == 'autumn']['AverageTemperature'].mean())
        winter_temps.append(curr_years_data[curr_years_data['season'] == 'winter']['AverageTemperature'].mean())


    #print spring_temps
    #print summer_temps
    #print autumn_temps
    #print winter_temps


    f, ax = plt.subplots(figsize=(10, 6))

    plt.plot(years, summer_temps, label='Summers average temperature', color='orange')
    plt.plot(years, autumn_temps, label='Autumns average temperature', color='r')
    plt.plot(years, spring_temps, label='Springs average temperature', color='g')
    plt.plot(years, winter_temps, label='Winters average temperature', color='b')
    ax.set_ylabel('Average temperature')
    ax.set_xlabel('Year')
    ax.set_title('Average temperature in each season for major cities in India')
    legend = plt.legend(bbox_to_anchor=(1, 0.5), frameon=True, borderpad=1, borderaxespad=0.)
    plt.savefig('seasons.png')
    #plt.show()

def get_season(month):
    if month >= 3 and month <= 5:
        return 'spring'
    elif month >= 6 and month <= 8:
        return 'summer'
    elif month >= 9 and month <= 11:
        return 'autumn'
    else:
        return 'winter'

Visualization()
