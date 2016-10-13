import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv(r'C:\Users\ifue3702\Downloads\Climate Data Narrabri\IDCJCM0037_053030 (2).csv',
              delimiter=',',
              index_col=None,
              header='infer',
              na_values=' ')
dfa=df.drop("Monthly Climate Statistics for 'NARRABRI WEST POST OFFICE' [053030]", 1)
dfb=dfa.dropna()
dfc=dfb.transpose()
dfc.to_csv(r'C:\Users\ifue3702\Downloads\Climate Data Narrabri\prueba.csv')
data=pd.read_csv(r'C:\Users\ifue3702\Downloads\Climate Data Narrabri\prueba.csv',
              delimiter=',',
              index_col=None,
              header='infer',
              na_values=' ',
              skiprows=range(0,1))
masl=212
albedo=0.23
#list(data.columns.values)
#Add mean temperature = (Tmax+tmin)/2 in Celcius degrees
data['Mean_T']=((data['Mean maximum temperature (Degrees C) for years 1962 to 2002 ']+data['Mean minimum temperature (Degrees C) for years 1962 to 2002 '])/2)
#add mean wind speed in m per second, supossedly at 2 m heigth
data['Mean_wind_speed_']=((data['Mean 9am wind speed (km/h) for years 1962 to 2002 ']+data['Mean 3pm wind speed (km/h) for years 1962 to 2002 '])/2)*1000/3600

data['e0_min']=0.6108*(2.71828**((17.27*data['Mean 9am temperature (Degrees C) for years 1962 to 2002 '])/(data['Mean 9am temperature (Degrees C) for years 1962 to 2002 ']+237.3)))
data['e0_max']=0.6108*2.71828**((17.27*data['Mean 3pm temperature (Degrees C) for years 1962 to 2002 '])/(data['Mean 3pm temperature (Degrees C) for years 1962 to 2002 ']+237.3))
data['es']=(data['e0_min']+data['e0_max'])/2
data['ea_min']=(data['Mean 9am relative humidity (%) for years 1962 to 2002 ']*data['e0_min'])/100
data['ea_max']=(data['Mean 3pm relative humidity (%) for years 1962 to 2002 ']*data['e0_max'])/100
data['ea']=(data['ea_min']+data['ea_max'])/2
data['es_ea']=(data['es']-data['ea'])
data['delta']=(4098*(0.6108*np.exp((17.27*data['Mean_T'])/(data['Mean_T']+237.3))))/(data['Mean_T']+237.3)**2
data['pressure']=101.3*((293-0.0065*masl)/293)**5.26
data['psi']=data['pressure']*0.665*10**(-3)
data['Rns']=(1-albedo)*data['Mean daily solar exposure (MJ/(m*m)) for years 1990 to 2016 ']
data['Ra']=data['Mean daily solar exposure (MJ/(m*m)) for years 1990 to 2016 ']/(0.165*(data['Mean maximum temperature (Degrees C) for years 1962 to 2002 ']-data['Mean minimum temperature (Degrees C) for years 1962 to 2002 '])**0.5)
data['Rso']=(0.75+2*0.00001*212)*data['Ra']
data['Rnl']=4.903*10**(-9)*(((data['Mean maximum temperature (Degrees C) for years 1962 to 2002 ']+273.16)**4+(data['Mean minimum temperature (Degrees C) for years 1962 to 2002 ']+273.16)**4)/2)*(0.34-0.14*data['ea']**0.5)*(1.35*(data['Mean daily solar exposure (MJ/(m*m)) for years 1990 to 2016 ']/data['Rso'])-0.35)
data['Rn']=data['Rns']-data['Rnl']
#def obtaining_G ():
#for row in data['Rns']:
#   if row in data.['Rns'] > 11:
#data['G']
#        return row%11
#  return data['G']
data['G']=0
#data['G'][0]=(data['Rns'][1]-data['Rns'][11])*0.07#data['G']=0.07*R
#figure out how to improve this code, is annoying!!!
data.set_value(0, ['G'], (data['Rns'][1]-data['Rns'][11])*0.07)
data.set_value(1, ['G'], (data['Rns'][2]-data['Rns'][0])*0.07)
data.set_value(2, ['G'], (data['Rns'][3]-data['Rns'][1])*0.07)
data.set_value(3, ['G'], (data['Rns'][4]-data['Rns'][2])*0.07)
data.set_value(4, ['G'], (data['Rns'][5]-data['Rns'][3])*0.07)
data.set_value(5, ['G'], (data['Rns'][6]-data['Rns'][4])*0.07)
data.set_value(6, ['G'], (data['Rns'][7]-data['Rns'][5])*0.07)
data.set_value(7, ['G'], (data['Rns'][8]-data['Rns'][6])*0.07)
data.set_value(8, ['G'], (data['Rns'][9]-data['Rns'][7])*0.07)
data.set_value(9, ['G'], (data['Rns'][10]-data['Rns'][8])*0.07)
data.set_value(10, ['G'], (data['Rns'][11]-data['Rns'][9])*0.07)
data.set_value(11, ['G'], (data['Rns'][0]-data['Rns'][10])*0.07)
data['ET0']=(0.408*data['delta']*(data['Rn']-data['G'])+data['psi']*900/(data['Mean_T']+273)*data['Mean_wind_speed_']*data['es_ea'])/(data['delta']+data['psi']*(1+0.34*data['Mean_wind_speed_']))
clean=data[0:13]
print(clean)
