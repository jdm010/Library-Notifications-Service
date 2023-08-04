import os
import requests
from bs4 import BeautifulSoup

# Making a GET request
response = requests.get('https://www.cambridge.org/core/services/librarians/kbart')

# Checking the response status
if response.status_code == 200:
    page_content = response.text
    print("Page fetched successfully")
else:
    print(f"Error: Failed to fetch the webpage ({response.status_code})")

soup = BeautifulSoup(page_content, 'html.parser')

prefix = 'cambridge ebooks and partner presses: 2023 '
subjects = ['computer','engineering','mathematics','physics','science','statistics']
found_links = []
tags = []

  
for subject in subjects:
    target_word = prefix + subject
    for tag in soup.find_all(text=lambda text: text and target_word in text.lower()):
        # Get the parent element of the found text
        parent_tag = tag.parent

        # Check if the parent element is an anchor tag (link)
        if parent_tag.name == 'a' and parent_tag.get('href'):
            link = parent_tag.get('href')
            tag =  parent_tag.get('data-ga-event-label')
            found_links.append(link)
            tags.append(tag)
    if found_links and tags:
        print(tag)
        print(link)         
    #else:
        #print(f'"{target_word}" not found on the webpage.')


def download_file(url, target_filename, desired_filename):
    response = requests.get(url)    
    if response.status_code == 200:
        filename = f"{desired_filename}"
        target_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(target_filepath, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filename}')
    else:
        print(f"Error: Failed to download {desired_filename} ({response.status_code})")

for link,tag in zip(found_links,tags):
    link2 = 'https://www.cambridge.org' + link
    download_file(link2, link2.split('/')[-1],tag)
