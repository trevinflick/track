###
### scrapes results from USATF website for 2017 Indoor Women's top marks
###

from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

### scrape the web page ###
html = urlopen("http://www.usatf.org/statistics/topMarks/2017/Indoor-Women.aspx")
html_soup = BeautifulSoup(html, 'html.parser')

all_rows_in_html_page = html_soup.findAll("tr")
my_table = html_soup.findAll("table", id="fancyTbl")

# extract the soup
# Generate lists
time=[]
heat=[]
blnk=[]
name=[]
team=[]
date=[]
race=[]

for row in html_soup.findAll("tr"):
    cells = row.findAll('td')
    if len(cells)==7: # Only extract table body not heading
        time.append(cells[0].find(text=True))
        heat.append(cells[1].find(text=True))
        blnk.append(cells[2].find(text=True))
        name.append(cells[3].find(text=True))
        team.append(cells[4].find(text=True))
        date.append(cells[5].find(text=True))
        race.append(cells[6].find(text=True))
        
# convert to dataframe and rename the columns
df=pd.DataFrame(time,columns=['time'])
df['heat']=heat
df['name']=name
df['team']=team
df['date']=date
df['race']=race



### clean the data frame ###

df = df.replace(to_replace = "\r\n\t\t\t\t\t", value="", regex = True)
df = df.replace(to_replace = "\xa0", value="", regex = True)
df.replace('', np.nan, inplace=True)

df = df.dropna(how='all') # drop rows with all NaN values
df = df.reset_index(drop=True)

# loop to fill in missing times 
# time equals the time in the previous row
for x in range(1,len(df)):
    if pd.isnull(df.iloc[x,0]):
        df.set_value(x,'time', df.iloc[x-1,0])
    else:
        continue

# make a list of the events
events = []

df['is_event'] = df['time'].str.contains('[A-Za-z]', regex=True)
for x in range(0, len(df)):
    if df.ix[x, 'is_event'] == True:
        events.append(df.ix[x, 'time'])
    else:
        continue

matching = [s for s in events if "i!" in s]
events = [s for s in events if s not in matching]
events = list(filter(lambda x: x != "Oversized Track:", events))

# map the events to a new column
row = []
event = []
for x in range(0,len(df)):
    if df.iloc[x,0] in events:
        row.append(x)
        event.append('')
    else:
        event.append(events[len(row)-1])
        
se = pd.Series(event)
df['event'] = se.values


# make a new column for oversized tracks
df['is_oversized'] = df['time'].str.contains('Oversized')
check = True
oversized = []
for x in range(0,len(df)):
    if df.iloc[x,6] == True and df.iloc[x,8] == True:
        check = False
        oversized.append("YES")
    elif df.iloc[x,6] == True and df.iloc[x,8] == False:
        check = True
        oversized.append("NO")
    else:    
        if check == True:
            oversized.append("NO")
        else:
            oversized.append("YES")

se = pd.Series(oversized)
df['is_oversized'] = se.values

# change field event format from 'meters'/'feet' to 'meters'
field_events = ['HIGH JUMP', 'POLE VAULT', 'LONG JUMP', 'TRIPLE JUMP', 'SHOT', 'WEIGHT']

jump_throw_events = df[df['event'].isin(field_events)]
jump_throw_events['time'] = jump_throw_events['time'].str.extract('(.*?)(?=\/)', expand=True)

running_events = df[~df['event'].isin(field_events)]
df = pd.concat([running_events, jump_throw_events])

# drop rows with just event title in them
events=[]
for possible_value in set(df["event"].tolist()):
    if len(possible_value) > 1:
        events.append(possible_value)
    else:
        continue
        
df = df[~df['time'].isin(events)]

df.to_csv('indoor_women_2017.csv')

df
