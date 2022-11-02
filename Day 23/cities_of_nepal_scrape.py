import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://en.m.wikipedia.org/wiki/List_of_cities_in_Nepal"
request = requests.get(url)
soup = bs(request.content)
table = soup.find_all('table')

# # Testing cell

# table_body=table[2].find_all('tbody')[0]
# table_allrow=table_body.find_all('tr')
# all_links = [i.find_all('a') for i in table_allrow]
# # print(table[2])
# # all_links[1][0].get_text()
# city= [all_links[i][0].get_text() for i in range(1,len(all_links))]
# city

all_city = []


def scrape_all_tables(n):
    tbody = table[n].find_all('tbody')[0]
    table_allrow = tbody.find_all('tr')
    all_links = [i.find_all('a') for i in table_allrow]
    for i in range(1, len(all_links)):
        all_city.append(all_links[i][0].get_text())


for j in range(2, len(table)):
    scrape_all_tables(j)
print(all_city)


df = pd.DataFrame(all_city, columns=["Cities"])
df.drop_duplicates()
df.to_csv('city.csv', index=True)
