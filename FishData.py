# CRCP Data:
# https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:NCRMP-Fish-Florida
# From 2014-05-01 Onward (Past 2018 not public)
# Latitude: N: 27.1897 to S: 24.4318
# Longitude: E: -79.9938 to W: -83.1036
# Christopher Davis

# Columns:
# Time, Latitude, Longitude, Depth, Species Number, Scientific Name, Common Name, Length, Number Seen
# Files : 1-100, 101-200, 201-500, 501-837
# Units: Time (UTC), Lat & Long (Degrees), Depth (Meters), Length, (CM)

# Ideas:
# Depth by Month for common species
# Types of fish observed (Quantity Profiles)
# Snapper Size by Month
# Stacked Density Plot for Fish Sub Species by Depth
# Tree map of fish by Type - Split into groups by quantity seen.
# Network map of fish by fish seen at the same geographical location - stronger paths for more frequently seen together

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px

def extractmonth(row):
    mystr = row['time']
    mystr.replace('-', ' ').split(' ')
    return int(mystr[5])*10+int(mystr[6])

df1 = pd.read_csv('CRCP_Reef_Fish_Surveys_Florida_'+'1_100'+'.csv')
df2 = pd.read_csv('CRCP_Reef_Fish_Surveys_Florida_'+'101_200'+'.csv')
df3 = pd.read_csv('CRCP_Reef_Fish_Surveys_Florida_'+'201_500'+'.csv')
df4 = pd.read_csv('CRCP_Reef_Fish_Surveys_Florida_'+'501_837'+'.csv')

# Concatenate files into one DF
fishdf = pd.concat([df1,df2,df3,df4])
fishdf['month'] = fishdf.apply(lambda row: extractmonth(row), axis=1)

#CSpecies = fishdf['common_name'].unique()
#print(len(CSpecies))

# Species Specific Dataframe
species = 'yellowtail snapper'
df_species = fishdf.query("common_name==@species")
#print(df_species)
#print(df_species.describe())

# Count Rows of Fish Species (Total Observations not including number in observation)
fishcounts = fishdf['common_name'].value_counts().rename_axis('common_name').reset_index(name='Counts').sort_values('common_name')
fishlength = fishdf.groupby('common_name', as_index=False)['length_fish'].mean()
fishdepth = fishdf.groupby('common_name', as_index=False)['depth'].mean()
fishschool = fishdf.groupby('common_name', as_index=False)['number_seen'].mean()

SummaryFishDF = fishcounts.merge(fishlength, how='left', on='common_name')
SummaryFishDF = SummaryFishDF.merge(fishdepth, how='left', on='common_name')
SummaryFishDF = SummaryFishDF.merge(fishschool, how='left', on='common_name')

#df_smaller = fishcounts.query("Counts<=10 & Counts>=4")
#print(df_smaller['common_name'].unique())

snapperdf = fishdf[fishdf['common_name'].isin(['dog snapper', 'vermilion snapper','glasseye snapper','blackfin snapper','mahogany snapper','mutton snapper','lane snapper','gray snapper','yellowtail snapper'])]

# Figures
fig1, (ax0, ax1) = plt.subplots(ncols = 1, nrows = 2, figsize = (14,8))
fig2, (ax2, ax3) = plt.subplots(ncols = 1, nrows = 2, figsize = (14,8))
fig3, ax4 = plt.subplots(ncols = 1, nrows = 1, figsize = (14,8))

# Depth Plot
plot1 = sns.kdeplot(ax = ax0, data=snapperdf, x="depth", hue="common_name",fill=False, 
    common_norm=False, palette="tab10",alpha=.1, linewidth=6, bw_adjust=.5)
ax0.set_yticklabels([])
ax0.set_ylabel(None)
ax0.set_xlabel('Depth (m)')
plot1.tick_params(left=False)
ax0.set_xlim(0, 35)
plot1.legend(title='Species', loc='upper right', labels=['Dog', 'Vermilion','Glasseye','Blackfin','Mahogany','Mutton','Lane','Gray','Yellowtail'], frameon=False)

plot2 = sns.boxplot(ax = ax1, data=snapperdf, x="common_name", y="length_fish", hue = "common_name", 
   palette="rocket", linewidth=2)
ax1.set_xticks([0,1,2,3,4,5,6,7,8])
ax1.set_xticklabels(['Mutton','Blackfin','Gray','Dog','Mahogany','Lane','Yellowtail','Glasseye','Vermilion'])
ax1.set_ylabel('Length (cm)'); ax1.set_xlabel('Snapper Species Common Name')
ax1.grid(axis='y')
ax1.set_axisbelow(True)
ax1.set_ylim(0, 90)

# Month Data for Select Species
snapperdf2 = snapperdf[snapperdf['common_name'].isin(['mutton snapper','lane snapper','gray snapper','yellowtail snapper'])]
plot3 = sns.boxplot(ax = ax2, data=snapperdf2, x="month", y="length_fish", hue = "common_name", palette="rocket", linewidth=2)
ax2.set_ylabel('Length (cm)'); ax2.set_xlabel('month')
ax2.grid(alpha = 0.5, axis='y')

# plot4 = sns.kdeplot(ax = ax3, data=snapperdf, x="depth", y="length_fish", hue = "common_name", palette="rocket", levels=15)
# ax3.set_ylabel('Length (cm)'); ax3.set_xlabel('Depth (m)')
# ax3.grid(alpha = 0.5)



# Plotly Tree Maps by Fish Type & Depth of Observation #

# Assign groups for categorizing the fish together
fishcountsgroup = []
for fish in SummaryFishDF['common_name'].to_list():
    if 'parrotfish' in fish: fishcountsgroup.append('PARROTFISH')
    elif 'snapper' in fish or 'schoolmaster' in fish: fishcountsgroup.append('SNAPPER')
    elif 'goby' in fish: fishcountsgroup.append('GOBY')
    elif 'wrasse' in fish: fishcountsgroup.append('WRASSE')
    elif 'grunt' in fish: fishcountsgroup.append('GRUNT')
    elif 'porgy' in fish: fishcountsgroup.append('PORGY')
    elif 'grouper' in fish: fishcountsgroup.append('GROUPER')
    elif 'jack' in fish: fishcountsgroup.append('JACK')
    elif 'sardine' in fish: fishcountsgroup.append('SARDINE')
    elif 'triggerfish' in fish: fishcountsgroup.append('TRIGGERFISH')
    elif 'hamlet' in fish: fishcountsgroup.append('HAMLET')
    elif 'filefish' in fish: fishcountsgroup.append('FILEFISH')
    elif 'razorfish' in fish: fishcountsgroup.append('RAZORFISH')
    elif ' ray' in fish or 'stingray' in fish: fishcountsgroup.append('RAY')
    elif 'butterflyfish' in fish: fishcountsgroup.append('BUTTERFLYFISH')
    else: fishcountsgroup.append('OTHER')

# Split Dataframes by count observations. 
SummaryFishDF['Category'] = fishcountsgroup
SummaryFishDFBig = SummaryFishDF[SummaryFishDF['Counts'] > 50]
SummaryFishDFSmall = SummaryFishDF[SummaryFishDF['Counts'] <= 50]
# print(SummaryFishDFBig)
# print(SummaryFishDFBig.describe())
# print(SummaryFishDFSmall)
# print(SummaryFishDFSmall.describe())

fig3 = px.treemap(SummaryFishDFBig, path=['Category','common_name'], values='Counts', 
    color='depth',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(SummaryFishDF['depth']),
    custom_data=['length_fish','depth','Counts','number_seen'], range_color=(0,25))
fig3.update_traces(
    hovertemplate='<b>%{label}</b><br>'+
        'Observations = %{customdata[2]}<br>'+
        'Average Depth (m)=%{customdata[1]:,.2f}<br>'+
        'Average Length (cm)=%{customdata[0]:,.2f}<br>'+
        'Average Group Size (cm)=%{customdata[3]:,.2f}'
)
fig3.show()

fig4 = px.treemap(SummaryFishDFSmall, path=['Category','common_name'], values='Counts', 
    color='depth',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(SummaryFishDF['depth']),
    custom_data=['length_fish','depth','Counts','number_seen'], range_color=(0,25))
fig4.update_traces(
    hovertemplate='<b>%{label}</b><br>'+
        'Observations = %{customdata[2]}<br>'+
        'Average Depth (m)=%{customdata[1]:,.2f}<br>'+
        'Average Length (cm)=%{customdata[0]:,.2f}'
)
fig4.show()


#plt.show()