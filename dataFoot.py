import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ["PROJ_LIB"] = "D:\Anaconda\Library\share" #A adapter selon votre path
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import datetime
from operator import itemgetter
from mplsoccer.pitch import Pitch

#Lecture du fichier
df = pd.read_json("coaches.json")
print(df)


#repartition activite
en_activite = len(df.loc[df['currentTeamId']==0])
hors_activite = len(df.loc[df['currentTeamId']!=0])

labels = ['en activite', 'hors activite']
values = [en_activite, hors_activite]

plt.pie(values, labels = labels, autopct='%.2f')
plt.show()


#Repartition pays
df_countries = df['passportArea'].value_counts()

countries = []
occurences = []
autre = 0
for country, occurence in df_countries.items():
    if occurence > 1 :
        countries.append(country['name'])
        occurences.append(occurence)
    else :
        autre += 1
countries.append('autre')
occurences.append(autre)
    
plt.barh(countries, occurences)
plt.show()


#Map
df_2 = pd.read_json("teams.json")
geolocator = Nominatim(user_agent="school_project")

latitudes, longitudes, clubs = [], [], []

for city, club in zip(df_2['city'], df_2['name']):
    try :
        location = geolocator.geocode(str(city))
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
        clubs.append(club)
    except AttributeError :
        print("{} n'a pas pu etre trouvee".format(city))
        
data = pd.DataFrame({'lon':latitudes,'lat':longitudes, 'name':clubs})
    
m=Basemap(llcrnrlon=-160, llcrnrlat=-75,urcrnrlon=160,urcrnrlat=80)
m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
m.drawcoastlines(linewidth=0.1, color="white")
 
m.plot(data['lat'], data['lon'], linestyle='none', marker="o", markersize=3, alpha=0.6, c="orange", markeredgecolor="black", markeredgewidth=1)
plt.show()


#Evolution des scores
df_2 = pd.read_json("teams.json")
df_3 = pd.read_json("matches_England.json")
   


def show_evolution(club_name):
    identifiant_club = df_2.loc[df_2['name'] == club_name, ['wyId']]
    identifiant_club = identifiant_club.iat[0,0]
    
    def filter_id(row):
        return str(identifiant_club) in row['teamsData'].keys()
    
    filtre_bool = df_3.apply(filter_id, axis=1)
    df_club_joue = df_3[filtre_bool]
    
    matchs = list()
    
    for teamdata, date in zip(df_club_joue['teamsData'], df_club_joue['date']):
        score = teamdata[str(identifiant_club)]['score']
        
        try : 
            date_object = datetime.datetime.strptime(date, '%B %d, %Y at %H:%M:%S PM GMT+2')
        except ValueError:
            date_object = datetime.datetime.strptime(date, '%B %d, %Y at %H:%M:%S PM GMT+1')
            
        matchs.append((date,score))
           
    sorted_maths = np.array(sorted(matchs, key=itemgetter(0)))
        
    plt.plot(np.array(matchs)[:,1])
    plt.show()
    
show_evolution('Liverpool')
show_evolution('Manchester City')
show_evolution('Manchester United')
show_evolution('Chelsea')
show_evolution('Arsenal')
show_evolution('Tottenham Hotspur')


#Placements buts
df_2 = pd.read_json("teams.json")
df_4 = pd.read_json("events_England.json")

def show_buts(club_name):
    identifiant_club = df_2.loc[df_2['name'] == club_name, ['wyId']]
    identifiant_club = identifiant_club.iat[0,0]
    
    df_goals = df_4.loc[(df_4['teamId'] == identifiant_club) & (df_4['subEventName'] == 'Goal kick')]
    
    x, y = list(), list()
    for i in df_goals['positions']:
        x.append(i[1]['x'])
        y.append(i[1]['y'])
    
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()
    sc = pitch.scatter(y, x, s=100, ax=ax)
    
show_buts('Chelsea')

    

        
        
    
    
    
