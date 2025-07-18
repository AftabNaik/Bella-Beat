# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# import libraries

import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
plt.style.use('ggplot')

#read csv

df = pd.read_csv("/kaggle/input/fitbit/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")

#show id as object

df['Id'] = df['Id'].astype(str)
df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
df.dtypes

#see the difference in between total and tracker

df['distance_diff'] = df['TotalDistance'] - df['TrackerDistance']
df['distance_diff'].value_counts()
df.query('distance_diff > 0.00')

#rename with underscore for better view

df.rename(columns = { 'activitydate':'activity_date', 'totalsteps':'total_steps', 'totaldistance':'total_distance', 'trackerdistance':'tracker_distance',
       'loggedactivitiesdistance':'logged_activities_distance', 'veryactivedistance':'very_active_distance',
       'moderatelyactivedistance':'moderately_active_distance', 'lightactivedistance':'light_active_distance',
       'sedentaryactivedistance':'sedentary_active_distance', 'veryactiveminutes':'very_active_minutes', 'fairlyactiveminutes':'fairly_active_minutes',
       'lightlyactiveminutes':'lightly_active_minutes', 'sedentaryminutes':'sedentary_minutes'}, inplace=True)

#column for weekday and number

day_of_week = df['activity_date'].dt.day_name()
df['day_of_week'] = day_of_week
df['n_day_of_week'] = df['activity_date'].dt.weekday


#create new activity level

df['activity_level'] = [id_activity_level[c] for c in df['id']]

#add in the columns

df = df[['id', 'activity_date', 'total_steps', 'total_distance',
       'very_active_minutes', 'fairly_active_minutes',
       'lightly_active_minutes', 'sedentary_minutes', 'calories',
       'activity_level', 'day_of_week', 'n_day_of_week']].copy()


# group by id and add conditions for various activity levels


id_grp = df.groupby(['id'])
id_avg_step = id_grp['total_steps'].mean().sort_values(ascending=False)
id_avg_step = id_avg_step.to_frame()
conditions = [
    (id_avg_step < 6000),
    (id_avg_step > 6000) & (id_avg_step < 12000), (id_avg_step >= 12000)]

values = ['sedentary', 'active', 'very_active']
id_avg_step['activity_level'] = np.select(conditions, values)
id_activity_level = id_avg_step['activity_level']
id_activity_level
id_avg_step

#show unique rows

print('Number of unique values in id column:',df['id'].nunique())
print()
print('List of id values:',df['id'].unique())

#correlation

ax = sns.scatterplot(x='total_steps', y ='calories',data = df, hue = df['activity_level'])
plt.title('correlation calories vs steps')
plt.tight_layout()
plt.show()


# create a day of week list, create a mean for each day. plot a graph for daily steps for week. add a line for average to find above average. create title and x,y labels.

day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

fig, ax = plt.subplots(1,1,figsize=(8,5))
day_grp = df.groupby(['day_of_week'])
avg_daily_steps = day_grp['total_steps'].mean()
avg_steps = df['total_steps'].mean()

plt.bar(avg_daily_steps.index, avg_daily_steps)

ax.set_xticks(range(len(day_of_week)))
ax.set_xticklabels(day_of_week)

ax.axhline(y=avg_daily_steps.mean(), color='blue', label= 'avg daily steps')

ax.set_ylabel('Steps')
ax.set_xlabel('day of week')

ax.set_title('avg number of steps per day')
plt.legend()
plt.show()

#create a sum for all types of activities and create a pie chart for each category percentage

very_active_minutes = df['very_active_minutes'].sum()
fairly_active_minutes = df['fairly_active_minutes'].sum()
lightly_active_minutes = df['lightly_active_minutes'].sum()
sedentary_minutes = df['sedentary_minutes'].sum()

slices = [very_active_minutes, fairly_active_minutes, lightly_active_minutes, sedentary_minutes]

labels = ['very_active_minutes', 'fairly_active_minutes', 'lightly_active_minutes', 'sedentary_minutes']
explode = [0,0,0,0.1]

plt.pie(slices, labels=labels, explode=explode, autopct = '%1.1f%%')
plt.title('% of activity level in minutes')


#finally create a correlation chart for all the activities w.r.t calories. 

n_day_of_week = [0,1,2,3,4,5,6]

fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(11,15),dpi=70)

sns.scatterplot(data=df,x='calories',y='sedentary_minutes',hue='activity_level',ax=axes[0,0],legend=False)

sns.scatterplot(data=df,x='calories',y='lightly_active_minutes',hue='activity_level',ax=axes[0,1],legend=False)

sns.scatterplot(data=df,x='calories',y='fairly_active_minutes',hue='activity_level',ax=axes[1,0],legend=False)

sns.scatterplot(data=df,x='calories',y='very_active_minutes',hue='activity_level',ax=axes[1,1])


plt.legend(title='Activity level',title_fontsize=20,bbox_to_anchor=(1.8,2.2),fontsize=18,frameon=True,scatterpoints=1)
fig.suptitle('Correlation Between activity level minutes and calories',x=0.5,y=0.92,fontsize=24)
plt.show()

