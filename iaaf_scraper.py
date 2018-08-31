from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np

def makeLink(distance = "marathon", setting = "outdoor", gender = "women", age = "senior", year = "2018", page = "1"):
    link = "https://www.iaaf.org/records/toplists/road-running/" + distance + '/'+ setting + '/'+ gender + '/'+ age + '/' + year + "?regionType=world&drop=regular&fiftyPercentRule=regular&page=" + page + "&bestResultsOnly=false"
    
    return link

marathon_data = pd.DataFrame()

for page_num in range(1,14):
    link = makeLink(page = str(page_num))

    page = urlopen(link)
    soup = BeautifulSoup(page)

    table = soup.find_all('td', {'data-th': ['Rank', 'Mark', 'Competitor', 'DOB', 'Nat', 'Pos', 'Venue', 'Date']})

    result = []

    for row in table:
        text = row.get_text()
        text = text.strip()
        result.append(text)

    num_rows = int(len(result) / 8)

    df = pd.DataFrame(np.array(result).reshape(num_rows, 8), 
                columns = ['Rank', 'Mark', 'Competitor', 'DOB', 'Nat', 'Pos', 'Venue', 'Date'])

    marathon_data = marathon_data.append(df, ignore_index=True)



marathon_data.to_csv('womens_marathon_2018.csv')