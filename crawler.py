""" 
import requests
from bs4 import BeautifulSoup

print('Start')

response = requests.get(
	url="https://en.wikipedia.org/wiki/Web_scraping",
)
print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find(id="firstHeading")
body_content = soup.find(id="mw-content-text")

print(title.string)
print(body_content)
 """

""" import wikiscraper as ws

ws.lang("en")

result = ws.searchBySlug("Barcelona")

# Get article's title
print(result.getTitle())
# Get article's URL
print(result.getURL())

# Get all paragraphs of abstract
print(result.getAbstract())
# Get the second paragraph of abstract
print(result.getAbstract()[1])
# Optional : Get the x paragraphs, starting from the beginning
print(result.getAbstract(2)) """

import wikipedia
# import json

# obj = {}
# ny = wikipedia.page("Barcelona")

# pop = wikipedia.summary("FC Barcelona")

# print(ny.content)


# temp = wikipedia.search("Real Sociedad San Sebastián")
# print(temp[0])

# fcb = wikipedia.page('FC Barcelona', auto_suggest=False)

# obj['title'] = fcb.title
# obj['summary'] = fcb.summary
# obj['url'] = fcb.url


# print(obj)


# 1. I need a list of all the clubs (1) Drive => (1k) json => (10k) json => (100k) json
# 1.1 Google search => Get the club list
# 2. Iterate on each club 
# 2.1 Summary 
# 3. Store the data in json


# from googlesearch import search
# temp = search("fc barcelona wiki", lang="en", advanced=True)

# for row in temp:
#     print(row.url) # title, description



# import wikiscraper as ws
# ws.lang("fr")
# result = ws.searchBySlug("Paris")

from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = 'https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives'
url_spain = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_Spain' ## Club, Home city
url_italy = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_Italy' ## Team, Home city
url_england = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_England' ## Club, League/Division

response = requests.get(url_england)
soup  = BeautifulSoup(response.text, 'html.parser')

## Get table by id 
# table_id = 'votingmembers'
# table_id_2 = 'La_Liga'
# table  = soup.find('table', attrs={'id': table_id_2})
# df = pd.read_html(str(table))

## Get table by class
table_temp =soup.select('table',{'class':"wikitable"})

tables=pd.read_html(str(table_temp))
# convert list to dataframe

dataset = []
for table in tables:
    df = pd.DataFrame(table)

    if 'Club' in df or 'Team' in df:

        for index, row in df.iterrows():

            club_name = row['Team'] if 'Team' in df else row['Club']
            club_city = row['League/Division']##row['Home city'] if 'Home city' in df else row['City']

            print(f'{club_name} {club_city}')
            
            # search_query = f'{club_name} {club_city} club wiki'
            # srch_results = search(search_query, lang="en", advanced=True)

            # for result in srch_results:
            #     result_url = result.url
            #     result_title = result.title

            obj = {}
            # if  'wiki' in result_url:

            # try:
            #     club = wikipedia.page(result_title, auto_suggest=False)
            # except Exception:
            wiki_pages = wikipedia.search(f'{club_name} {club_city}')
            try:
                club = wikipedia.page(wiki_pages[0], auto_suggest=False) if len(wiki_pages) > 0 else None


                obj['title'] = club.title if club is not None else None
                obj['summary'] = club.summary if club is not None else None
                obj['url'] = club.url if club is not None else None

                if club is not None:
                    dataset.append(obj)

            except Exception as e:
                print(f'{club_name} {club_city} not found. Returned search {wiki_pages}')
                continue

import json

# Create a list

# Open the file in write mode
with open('dataset_italy.json', 'w') as file:
    # Write the list to the file using json.dump()
    json.dump(dataset, file)