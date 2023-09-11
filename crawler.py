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
import json

url = 'https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives'
url_spain = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_Spain' ## Club, Home city
url_italy = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_Italy' ## Team, Home city
url_england = 'https://en.wikipedia.org/wiki/List_of_football_clubs_in_England' ## Club, League/Division

response = requests.get(url_spain)
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
            # club_city = row['League/Division'] if 'League/Division' in df else row['City']
            club_city = row['Home city'] if 'Home city' in df else row['City']

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

                import re

                # Split the text into sections using '==' as the delimiter
                sections = re.split(r'\n==\s+', club.content.strip())

                # Remove any leading or trailing whitespace from each section
                sections = [section.strip() for section in sections if section.strip()]

                # Initialize the result dictionary
                result = {
                    "introduction": sections[0].strip(),
                    "sections": []
                }

                # Process the remaining sections
                for section in sections[1:]:
                    section_parts = section.split('\n')
                    section_name = section_parts[0].strip().replace('==', '')
                    section_content = section_parts[1:]
                    section_content = [item for item in section_content if item]
                    
                    # Sub sections 
                    sub_sections = re.split(r'\n===\s+', "\n".join(section_content))
                    sub_sections = [sub_section.strip() for sub_section in sub_sections if sub_section.strip()]

                    if len(sub_sections) > 1:

                        index = 0 if '===' in sub_sections[0] else 1

                        introduction = '' if index == 0 else sub_sections[0]

                        section_dict = {section_name.strip(): introduction,
                                        "sub_sections": []}
                        
                        for sub_section in sub_sections[index:]:
                            sub_section_parts = sub_section.split('\n')
                            sub_section_name = sub_section_parts[0].strip().replace('===', '')
                            sub_section_content = sub_section_parts[1:]
                            sub_section_content = [item for item in sub_section_content if item]

                            section_dict["sub_sections"].append({sub_section_name.strip(): "\n".join(sub_section_content)})

                    else:
                        # Initialize a dictionary for this section
                        section_dict = {section_name.strip(): "\n".join(section_content)}
                    
                    result["sections"].append(section_dict)

                # Convert the result to JSON
                json_result = json.dumps(result, indent=4)                



                obj['content'] = json_result if club is not None else None

                if club is not None:
                    dataset.append(obj)

            except Exception as e:
                print(f'{club_name} {club_city} not found. Returned search {wiki_pages}')
                print(e)
                continue

# Create a list

# Open the file in write mode
with open('dataset_spain_all_page_sections.json', 'w') as file:
    # Write the list to the file using json.dump()
    json.dump(dataset, file)