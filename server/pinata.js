const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

require('dotenv').config();  // To use environment variables

// Replace with your JWT or load it from .env
const pinataJWT = process.env.PINATA_JWT;

async function testAuthentication() {
  try {
    const response = await axios.get('https://api.pinata.cloud/data/testAuthentication', {
      headers: {
        'accept': 'application/json',
        'authorization': `Bearer ${pinataJWT}`
      }
    });

    console.log("Authentication Successful:", response.data);
  } catch (error) {
    console.error("Error during authentication:", error.response ? error.response.data : error.message);
  }
}

testAuthentication();

// Path to the text file to upload
const filePath = './Hurricane helene helplines search_results.txt';

// Create a FormData instance and append the file
const form = new FormData();
form.append('file', fs.createReadStream(filePath), 'Testing.txt');

// Axios options
const options = {
  method: 'POST',
  url: 'https://uploads.pinata.cloud/v3/files',
  headers: {
    Authorization: `Bearer ${pinataJWT}`,  // Use your Pinata JWT token from .env
    ...form.getHeaders()                                  // Important for multipart/form-data
  },
  data: form                                              // The form data containing the file
};

// Perform the request
axios(options)
  .then(response => {
    console.log('File uploaded successfully:', response.data);
  })
  .catch(err => {
    console.error('Error uploading file:', err.response ? err.response.data : err.message);
  });
