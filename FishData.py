# CRCP Data:
# https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:NCRMP-Fish-Florida
# From 2014-05-01 Onward (Past 2018 not public)
# Latitude: N: 27.1897 to S: 24.4318
# Longitude: E: -79.9938 to W: -83.1036
# 11/23/2021 Project
# Christopher Davis


# Columns:
# Time, Latitude, Longitude, Depth, Species Number, Scientific Name, Common Name, Length, Number Seen
# Files : 1-100, 101-200, 201-500, 501-837
# Units: Time (UTC), Lat & Long (Degrees), Depth (Meters), Length, (CM)

# Ideas:
# Depth by Month for common species
# Types of fish observed (Quantity Profiles)
# Snapper Size by Month

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import seaborn as sns

Extension = '.csv'
FileValues = ['1_100','101_200','201_500','501_837']
def filestring(val):
    FileString = 'CRCP_Reef_Fish_Surveys_Florida_'+FileValues[val]+Extension
    return FileString

def extractmonth(row):
    mystr = row['time']
    mystr.replace('-', ' ').split(' ')
    return int(mystr[5])*10+int(mystr[6])

df1 = pd.read_csv(filestring(0))
df2 = pd.read_csv(filestring(1))
df3 = pd.read_csv(filestring(2))
#df4 = pd.read_csv(filestring(3))

# Concatenate files into one DF
fishdf = pd.concat([df1,df2,df3])

#CSpecies = fishdf['common_name'].unique()
#print(len(CSpecies))


# Species Specific Dataframe
species = 'yellowtail snapper'
df_species = fishdf.query("common_name==@species")
#print(df_species)
#print(df_species.describe())


# Count Rows of Fish Species
fishdfcounts = fishdf['common_name'].value_counts().rename_axis('common_name').reset_index(name='Counts')

#df_smaller = fishdfcounts.query("Counts<=10 & Counts>=4")
#print(df_smaller['common_name'].unique())

snapperdf = fishdf[fishdf['common_name'].isin(['dog snapper', 'vermilion snapper','glasseye snapper','blackfin snapper','mahogany snapper','mutton snapper','lane snapper','gray snapper','yellowtail snapper'])]
print(snapperdf)

plotdepth = True
if plotdepth == True:
    plot1 = sns.kdeplot(
       data=snapperdf, x="depth", hue="common_name",
       fill=False, common_norm=False, palette="tab10",
       alpha=.1, linewidth=6, bw_adjust=.5
    )
    plot1.set(yticklabels=[])
    plot1.set(ylabel=None)
    plot1.set(xlabel='Depth (m)')
    plot1.tick_params(left=False)
    plot1.set(xlim=(0, 35))
    plot1.legend(title='Species', loc='upper right', labels=['Dog', 'Vermilion','Glasseye','Blackfin','Mahogany','Mutton','Lane','Gray','Yellowtail'], frameon=False)
    plot1.figure.set_figheight(4)
    plot1.figure.subplots_adjust(hspace = 0.2, wspace = 0.2)
    plot1.figure.set_figwidth(24)
    plot1.figure.savefig('Try1.png', transparent=True)

plotsize = False
if plotsize == True:
    
    plot2 = sns.boxplot(
       data=snapperdf, x="common_name", y="length_fish",
       palette="rocket", linewidth=2
    )
    plot2.set(xticklabels=['Mutton','Blackfin','Gray','Dog','Mahogany','Lane','Yellowtail','Glasseye','Vermilion'])
    plot2.set(xlabel=None)
    plot2.set(ylabel='Length (cm)')
    plot2.grid(axis='y')
    plot2.set_axisbelow(True)
    plot2.set(ylim=(0, 90))
    plot2.figure.set_figheight(6)
    plot2.figure.set_figwidth(10)
    plot2.figure.savefig('Try2.png', transparent=True)


snapperdf['month'] = snapperdf.apply (lambda row: extractmonth(row), axis=1)
print(snapperdf)
snapperdf2 = snapperdf[snapperdf['common_name'].isin(['mutton snapper','lane snapper','gray snapper','yellowtail snapper'])]


plotmonths = False
if plotmonths == True:
    
    plot3 = sns.boxplot(
       data=snapperdf2, x="month", y="length_fish", hue = "common_name",
       palette="rocket", linewidth=2
    )
    #plot3.set(xticklabels=['Mutton','Blackfin','Gray','Dog','Mahogany','Lane','Yellowtail','Glasseye','Vermilion'])
    #plot3.set(xlabel=None)
    #plot3.set(ylabel='Length (cm)')
    plot3.grid(axis='y')
    #plot3.set_axisbelow(True)
    #plot3.set(ylim=(0, 90))
    #plot3.figure.set_figheight(6)
    #plot3.figure.set_figwidth(10)
    #plot3.figure.savefig('Try3.png', transparent=True)

plt.show()

## Fish Sorted by Counts
# Counts (1-3)
['pigfish' 'honeycomb cowfish' 'reef silverside' 'marbled blenny'
 'whitefin sharksucker' 'bluespotted cornetfish' 'sponge cardinalfish'
 'greater soapfish' 'dusky jawfish' 'reef squirrelfish'
 'southern stingray' 'tarpon' 'whitespotted soapfish' 'trunkfish'
 'hybrid hamlet' 'spotted goby' 'Atlantic creolefish'
 'sawcheek cardinalfish' 'bridle cardinalfish' 'tiger goby'
 'orangespotted goby' 'banner goby' 'dwarf goatfish' 'papillose blenny'
 'black jack' 'Spanish mackerel' 'Nassau grouper' 'redspotted hawkfish'
 'secretary blenny' 'yellowfin grouper' 'gag' 'golden hamlet'
 'spotted burrfish' 'banded jawfish' 'purplemouth moray' 'indigo hamlet'
 'lancer dragonet' 'spotfin mojarra' 'mutton hamlet' 'black durgon'
 'remora' 'green moray' 'checkered puffer' 'orangeside goby'
 'redfin needlefish' 'lookdown' 'sharptail eel']

# Counts (4-10)
['barred cardinalfish' 'yellow stingray' 'belted cardinalfish'
 'balloonfish' 'southern sennet' 'spotted eagle ray' 'queen triggerfish'
 'little tunny' 'painted wrasse' 'sharknose goby' 'sailfin blenny'
 'goliath grouper' 'wrasse blenny' 'pinfish' 'jackknife-fish'
 'scrawled cowfish' 'reef shark' 'hardhead silverside' 'dog snapper'
 'roughhead blenny' 'spotted drum' 'orange filefish' 'common snook'
 'coney' 'rock hind' 'sand diver' 'bonnetmouth' 'red hind'
 'yellowline goby' 'tan hamlet' 'nurse shark' 'spotted trunkfish'
 'planehead filefish' 'yellownose goby' 'yellowmouth grouper'
 'dusky squirrelfish']

# Counts (11-50)
['blackbar soldierfish' 'greater amberjack' 'sheepshead porgy' 'cubbyu'
 'cherubfish' 'margate' 'yellowfin mojarra' 'smooth trunkfish'
 'bandtail puffer' 'glasseye snapper' 'blackfin snapper' 'almaco jack'
 'glassy sweeper' 'littlehead porgy' 'Seminole goby' 'unicorn filefish'
 'brown garden eel' 'sea bream' 'pallid goby' 'spotfin hogfish'
 'knobbed porgy' 'crevalle jack' 'school bass' 'black grouper'
 'sheepshead' 'yellowcheek wrasse' 'permit' 'flamefish' 'sand perch'
 'Spanish sardine' 'Atlantic bumper' 'horse-eye jack'
 'orangespotted filefish' 'yellowprow goby' 'townsend angelfish' 'scamp'
 'dash goby' 'sand tilefish' 'redear sardine' 'black hamlet' 'bigeye'
 'twospot cardinalfish' 'whitespotted filefish' 'hairy blenny'
 'emerald parrotfish' 'pearly razorfish' 'sharksucker' 'vermilion snapper'
 'rainbow wrasse' 'scaled sardine' 'African pompano' 'silver porgy'
 'belted sandfish' 'jolthead porgy' 'banded rudderfish' 'slender filefish']

# Counts (51-250)
['mutton snapper' 'French angelfish' 'sailors choice' 'scrawled filefish'
 'banded butterflyfish' 'chalk bass' 'squirrelfish' 'tobaccofish'
 'seaweed blenny' 'rainbow parrotfish' 'boga' 'Atlantic spadefish'
 'longspine squirrelfish' 'longfin damselfish' 'colon goby'
 'great barracuda' 'round scad' 'high-hat' 'striped grunt'
 'rosy razorfish' 'red grouper' 'ocean triggerfish' 'mahogany snapper'
 'lantern bass' 'barred hamlet' 'midnight parrotfish' 'blue hamlet'
 'hovering dartfish' 'rosy blenny' 'queen parrotfish'
 'Atlantic trumpetfish' 'spottail pinfish' 'red lionfish' 'reef croaker'
 'ballyhoo' 'Spanish grunt' 'black margate' 'rainbow runner'
 'black sea bass' 'cero' 'mackerel scad']

# Counts (251-1000)
['beaugregory' 'schoolmaster' 'green razorfish' 'rock beauty'
 'bluelip parrotfish' 'lane snapper' 'harlequin bass' 'gray triggerfish'
 'dusky damselfish' 'blue dartfish' 'graysby' 'blue runner'
 'saddled blenny' 'cottonwick' 'blackear wrasse' 'yellowtail parrotfish'
 'smallmouth grunt' 'yellow jack' 'caesar grunt' 'blue angelfish'
 'redtail parrotfish' 'yellowtail reeffish' 'goldspot goby'
 'Spanish hogfish' 'yellowtail damselfish' 'puddingwife' 'queen angelfish'
 'blue parrotfish' 'bucktooth parrotfish' 'yellow goatfish']

# Counts (1001+)
['bluehead' 'bicolor damselfish' 'striped parrotfish' 'slippery dick'
 'yellowtail snapper' 'redband parrotfish' 'yellowhead wrasse'
 'white grunt' 'ocean surgeon' 'masked goby' 'cocoa damselfish'
 'blue tang' 'clown wrasse' 'purple reeffish' 'French grunt'
 'bridled goby' 'doctorfish' 'blue chromis' 'bar jack' 'tomtate'
 'stoplight parrotfish' 'greenblotch parrotfish' 'gray snapper'
 'sharpnose puffer' 'sergeant major' 'creole wrasse' 'bluestriped grunt'
 'foureye butterflyfish' 'spotfin butterflyfish' 'brown chromis'
 'porkfish' 'reef butterflyfish' 'yellowhead jawfish' 'saucereye porgy'
 'neon goby' 'threespot damselfish' 'hogfish' 'princess parrotfish'
 'sunshinefish' 'butter hamlet' 'Bermuda chub' 'spotted goatfish'
 'gray angelfish']