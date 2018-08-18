from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import timeit

chicago_top100 = "http://results.chicagomarathon.com/2017/?page=1&event=MAR&lang=EN_CAP&num_results=100&pid=list&search%5Bage_class%5D=%25&search%5Bsex%5D=M"

page = urlopen(chicago_top100)
soup = BeautifulSoup(page)
all_links = soup.find_all("a")


# get a link to all the athletes pages

athlete_links = []

for link in all_links:
    if "?content" not in link.get("href"):
        continue
    else:
        athlete_links.append(link.get("href"))

base_link = 'http://results.chicagomarathon.com/2017/'

athlete_links = [base_link + x for x in athlete_links]

athlete_data = []

### scrape info from each athlete page

start = timeit.default_timer()

for runner in range(0, len(athlete_links)):
    # for each runner in the top 100, download the tables for each athlete
    page = urlopen(athlete_links[runner])
    soup = BeautifulSoup(page, features = "lxml")
    
    # extract the splits table
    splits_table = soup.find_all('div', {"class" : "detail-box box-splits"})
    
    result = []
    for td in splits_table:
        result.extend(td.find_all('td'))
    
    splits = []
    for i in result:
        splits.append(i.get_text())
    
    # extract the athlete info table
    info_table = soup.find_all('div', {"class" : "detail-box box-general"})
    
    result = []
    for td in info_table:
        result.extend(td.find_all('td'))
        
    info = []
    for i in result:
        info.append(i.get_text())
    
    athlete = info + splits
    
    athlete_data.append(athlete)
    
    # pause downloads to not overwhelm the website
    time.sleep(3)
    
stop = timeit.default_timer()

print(stop - start)


df = pd.DataFrame(athlete_data)

df.columns = ['Name', 'Age_Group', 'Bib', 'Age', 'City', 'Place', 'Short',
              '5_TOD', '5_Time', '5_Diff', '5_MinMil', '5_MPH',
              '10_TOD', '10_Time', '10_Diff', '10_MinMil', '10_MPH',
              '15_TOD', '15_Time', '15_Diff', '15_MinMil', '15_MPH',
              '20_TOD', '20_Time', '20_Diff', '20_MinMil', '20_MPH',
              'HALF_TOD', 'HALF_Time', 'HALF_Diff', 'HALF_MinMil', 'HALF_MPH',
              '25_TOD', '25_Time', '25_Diff', '25_MinMil', '25_MPH',
              '30_TOD', '30_Time', '30_Diff', '30_MinMil', '30_MPH',
              '35_TOD', '35_Time', '35_Diff', '35_MinMil', '35_MPH',
              '40_TOD', '40_Time', '40_Diff', '40_MinMil', '40_MPH',
              'FIN_TOD', 'FIN_Time', 'FIN_Diff', 'FIN_MinMil', 'FIN_MPH']

columns = ['Short', '5_TOD', '5_Diff', '5_MinMil', '5_MPH',
           '10_TOD', '10_Diff', '10_MinMil', '10_MPH',
              '15_TOD', '15_Diff', '15_MinMil', '15_MPH',
              '20_TOD', '20_Diff', '20_MinMil', '20_MPH',
              'HALF_TOD', 'HALF_Diff', 'HALF_MinMil', 'HALF_MPH',
              '25_TOD', '25_Diff', '25_MinMil', '25_MPH',
              '30_TOD', '30_Diff', '30_MinMil', '30_MPH',
              '35_TOD', '35_Diff', '35_MinMil', '35_MPH',
              '40_TOD', '40_Diff', '40_MinMil', '40_MPH',
              'FIN_TOD', 'FIN_Diff', 'FIN_MinMil', 'FIN_MPH']

df.drop(columns, inplace=True, axis=1)

df.to_csv('Chicago_2017_Results.csv', sep = '\t')



