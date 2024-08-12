# Set-In
## Features
    •    Google OAuth2 Authentication: Secure user login using Google accounts.
    •    Image Generation: Generate images based on selected styles stored in Google Cloud Storage.
    •    Location-Based Search: Find nearby stores or services using Google Maps API.
    •    Session Management: Handles user sessions securely with Flask-Session.
## Prerequisites
    •    Python 3.7 or higher
    •    Google Cloud Project with the following APIs enabled:
    ◦    Google Cloud Vision API
    ◦    Google Maps API
    •    Google Service Account with credentials file
    •    Flask, Flask-Session, Flask-CORS, and Authlib for Python

- Set Up Google Cloud Project:
	•	Go to the Google Cloud Console.
	•	Create a new project or use an existing one.
	•	Enable the AutoML and Cloud Storage APIs.
	•	Set up billing if you haven't already.
- Create a Dataset for AutoML Vision:
	•	Upload your labeled images to a Google Cloud Storage bucket.
	•	In the Google Cloud Console, navigate to AutoML Vision.
	•	Create a new dataset and import images from your Cloud Storage bucket.
	•	Label your images according to the categories (e.g., different styles, furniture types).
- Train a Model:
	•	Once your dataset is ready, you can train a custom model.
	•	Choose the model type (classification, object detection, etc.).
	•	Google AutoML will automatically train the model based on your dataset.
- Deploy the Model:
	•	After training, you can deploy your model to make it accessible via an API.
	• Deploy the model in the Google Cloud Console and get the API endpoint.

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
python -c 'import secrets; print(secrets.token_hex(16))' (Generates Secrect_Key)

## Setup
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-repo/VisionGem.git
cd VisionGem
2. Install Dependencies
Ensure you have Python 3.7+ installed. Then, install the required Python packages:
bash
Copy code
pip install -r requirements.txt
3. Set Up Google Cloud Credentials
    •    Download your Google Cloud service account key file and save it as path/to/your/service-account-file.json in the project directory.
    •    Set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-file.json"
4. Configure Environment Variables
Create a .env file in the project directory with the following contents:
makefile
Copy code
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
Replace the placeholders with your actual values.
5. Configure Google Cloud Storage
Ensure your Google Cloud Storage bucket is set up and named correctly in the BUCKET_NAME variable within the Flask application:
python
Copy code
BUCKET_NAME = 'set-in'
Organize your images in folders by style within the bucket.
6. Running the Application
You can start the Flask application using the following command:
bash
Copy code
python app.py
The application will run in debug mode by default. Access it by navigating to http://localhost:5000 in your web browser.
7. Using the Application
    •    Login: Navigate to the home page, and you'll be redirected to the login page. Use your Google account to log in.
    •    Image Generation: After logging in, go to the "Design" page to generate images based on selected styles.
    •    Search: Use the search feature to find nearby services or stores based on location and category.
8. Logging Out
Click the "Logout" button to end your session and be redirected to the login page.



