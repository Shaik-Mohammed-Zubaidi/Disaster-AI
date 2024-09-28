import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your JWT or load it from .env
pinata_jwt = os.getenv('PINATA_JWT')

def test_authentication():
    try:
        response = requests.get(
            'https://api.pinata.cloud/data/testAuthentication',
            headers={
                'accept': 'application/json',
                'authorization': f'Bearer {pinata_jwt}'
            }
        )
        response.raise_for_status()  # Raise an error for bad responses
        print("Authentication Successful:", response.json())
    except requests.exceptions.RequestException as error:
        print("Error during authentication:", error)

def upload_text_file(content, filename):
    """Uploads a text file's content directly to Pinata."""
    upload_url = 'https://uploads.pinata.cloud/v3/files'
    headers = {
        'Authorization': f'Bearer {pinata_jwt}',
    }
    
    # Create the file-like object
    files = {'file': (filename, content)}
    
    # Use requests.post to upload the content
    response = requests.post(upload_url, headers=headers, files=files)

    # Check the response
    if response.status_code == 200:
        print('File uploaded successfully:', response.json())
    else:
        print('Error uploading file:', response.json())

# Call the authentication function if needed
# test_authentication()
