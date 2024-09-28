
### Using google api to get top 10 results
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def google_search(query, api_key, cse_id, num_results=5, exactTerms=''):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,  # Query term
        'key': api_key,  # Your API key
        'cx': cse_id,  # Custom Search Engine ID
        'num': num_results,  # Number of search results to return
        'exactTerms': exactTerms,
    }
    
    response = requests.get(url, params=params, timeout=5)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def save_results_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, item in enumerate(results.get('items', []), start=1):
            title = item['title']
            snippet = item.get('snippet', '')
            link = item['link']
            file.write(f"{i}. {title}\n{snippet}\n{link}\n\n")

# Replace with your own API key and Custom Search Engine ID
API_KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CSE_ID')
NO_OF_RESULTS = 10
EXACT_TERMS = 'call'

query = "Hurricane helene helplines"
results = google_search(query, API_KEY, CSE_ID, NO_OF_RESULTS, EXACT_TERMS)

# Save search results to a text file
save_results_to_file(results, query+ ' search_results.txt')

print(f"Search completed. Results saved to '{query} search_results.txt'")


### Extracting links from the results

import re

def extract_links_from_file(file_path):
    # Open the file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Split the content based on double newlines to separate entries
    entries = file_content.split('\n\n')
    
    # Regex pattern to match URLs
    url_pattern = r'https?://[^\s]+'
    
    # Initialize an empty list to store the links
    links = []
    
    # Iterate through the entries and extract the URLs
    for entry in entries:
        # Search for URLs in the entry
        found_links = re.findall(url_pattern, entry)
        # Add any found URLs to the links list
        links.extend(found_links)
    
    return links

# Specify the file path of the search_results.txt
file_path = query +' search_results.txt'

# Get the links from the file
links = extract_links_from_file(file_path)

# Print the list of extracted links
for link in links:
    print(link)
print(f"\nExtracted {len(links)} links from the file.")


### Extracting content from the links

import requests
import os
from bs4 import BeautifulSoup

# List of URLs to fetch content from
urls = links

folder_path = query

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Loop over each URL and store the content in separate text files
for idx, url in enumerate(urls, start=1):
    # Fetch the webpage content
    response = requests.get(url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the main content from the page (assuming <p> tags)
    content = ""
    for paragraph in soup.find_all('p'):
        content += paragraph.get_text() + "\n"

    # Save the content to a text file with a dynamic filename inside the folder
    filename = f"webpage_content{idx}.txt"
    file_path = os.path.join(folder_path, filename) 
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Webpage content saved to '{filename}'")
print(f"\nSaved content from {len(urls)} webpages.")