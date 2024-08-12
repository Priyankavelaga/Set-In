# Set-In
#Google-Cloud
Get GEMINI_API_KEY
Go to Google-AI-Studio and generate new API key 
Get GEMINI_MAPS_API_KEY
Google Console > APIs & Services > Credentials > Create Credentials > API key
Enable Google Maps API, Places API, People API, 
Google Console > APIs & Services > Credentials > Create Credentials > Oauth Client2.0
Set name, redirect uri and get a client-secrect.json file
Google Console > APIs & Services > Credentials > Create Credentials > Service Account
get service-account.json.file
Go to IAM & Admin > Get Permissions
Here set the roles 

## Create .env file in your project directory
GEMINI_MAPS_API_KEY
GEMINI_API_KEY
CLIENT_SECRECT
CLIENT_ID

## Install the Google AI Python SDK
Setup pip in the virtual environment
python3.8 -m venv venv
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install --upgrade pip
pip install google-cloud-aiplatform
pip install google-api-python-client
pip list
Create main .py file to test weather Google Cloud AI Platform SDK is installed and configured
python main.py 
Now Google Cloud AI Platform SDK is installed and configured in your VS Code


export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-file.json"

