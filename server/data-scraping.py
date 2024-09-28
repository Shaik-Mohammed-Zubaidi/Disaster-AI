import requests
import os
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pinata import upload_text_file  # Import the upload function

load_dotenv()

def google_search(query, api_key, cse_id, num_results=5, exactTerms=''):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': num_results,
        'exactTerms': exactTerms,
    }
    
    response = requests.get(url, params=params, timeout=5)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def extract_links_from_results(results):
    links = []
    for item in results.get('items', []):
        link = item['link']
        links.append(link)
    return links

# Replace with your own API key and Custom Search Engine ID
API_KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CSE_ID')
NO_OF_RESULTS = 10
EXACT_TERMS = 'call'

query = "Hurricane helene helplines"
results = google_search(query, API_KEY, CSE_ID, NO_OF_RESULTS, EXACT_TERMS)

# Extract links from the search results
links = extract_links_from_results(results)

# Print the list of extracted links
for link in links:
    print(link)

# Loop over each URL and extract content
for idx, url in enumerate(links, start=1):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the main content from the page (assuming <p> tags)
    content = "\n".join(paragraph.get_text() for paragraph in soup.find_all('p'))

    # Upload the content as a text file to Pinata
    filename = f"webpage_content_{idx}.txt"  # Name the file
    upload_text_file(content.encode('utf-8'), filename)  # Encode the content to bytes

print(f"\nUploaded content from {len(links)} webpages to Pinata.")
