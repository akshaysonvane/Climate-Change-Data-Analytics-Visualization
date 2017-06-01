import plotly.plotly as py
import pandas as pd
import numpy as np
import warnings


warnings.filterwarnings('ignore')

global_temp_country = pd.read_csv('Data/GlobalLandTemperaturesByCountry.csv')



#Let's remove the duplicated countries (in the analysis, we don't consider the presence of 
#colonies at this the countries) and countries for which no information about the temperature

global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
     'United Kingdom', 'Africa', 'South America'])]

global_temp_country_clear = global_temp_country_clear.replace(
   ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
   ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

#Let's average temperature for each country

countries = np.unique(global_temp_country_clear['Country'])
mean_temp = []
for country in countries:
    mean_temp.append(global_temp_country_clear[global_temp_country_clear['Country'] == 
                                               country]['AverageTemperature'].mean())



df = pd.DataFrame({'Country':countries,'Temp':mean_temp})

data = [ dict(
        type = 'choropleth',
        locations = df['Country'],
        z = df['Temp'],
        locationmode = 'country names',
        text = df['Country'],
        marker = dict(
            line = dict(color = 'rgb(0,0,0)', width = 1)),
            colorbar = dict(tickprefix = '', 
            title = ' Average\nTemperature,\n')
            )
       ]

layout = dict(
   title = 'Average Temperature',
   geo = dict(
       showframe = False,
       showcoastlines = False,
       projection = dict(
           type = 'Mercator'
       )
   )
)


fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='d3-world-map' )