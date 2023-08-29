import requests

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the response status code indicates an error
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: Failed to fetch the webpage ({err})")
        return None

def find_links_and_tags(soup, subjects, prefix):
    found_links = []
    for subject in subjects:
        target_word = prefix + subject
        for tag in soup.find_all(string=lambda text: text and target_word in text.lower()):
            parent_tag = tag.parent
            if parent_tag.name == 'a' and parent_tag.get('href'):
                link = parent_tag.get('href')
                found_links.append(link)
    return found_links

def download_file(url, desired_filename, target_filepath):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{desired_filename}.tsv"
        with open(target_filepath + filename, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filename}')
    else:
        print(f"Error: Failed to download {desired_filename} ({response.status_code})")
