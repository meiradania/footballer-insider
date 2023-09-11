
import wikipedia
wiki_pages = wikipedia.search(f'FC BARCELONA')
club = wikipedia.page(wiki_pages[0], auto_suggest=False) if len(wiki_pages) > 0 else None
# club = wikipedia.page("New York")


# print(f' URL: {club.url}')
# print(f'TITLE: {club.title}')
# print(f'SUMMARY: {club.summary}')
# print(f'CONTENT: {club.content}')
# print(f'Sections: {club.sections}')
# print(f'Categories: {club.categories}')

# sections = club.content.split('==')
# print(sections[0])
# print(sections[1])

import re
import json


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

    # if section_name != 'Players ':
    #     continue
    
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

# Print the JSON result
print(json_result)