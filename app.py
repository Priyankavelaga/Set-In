from flask import Flask, redirect, jsonify, request, render_template, url_for, session
import os
import random
from google.cloud import vision
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
from flask_session import Session
from authlib.integrations.flask_client import OAuth
import secrets
from functools import wraps
import requests
from flask_cors import CORS
from datetime import timedelta


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'YOUR_SERVICE_ACCOUNT.json'

storage_client = storage.Client()
BUCKET_NAME = '<YOUR_BUCKET_NAME'>

app = Flask(__name__)
CORS(app)


load_dotenv()


credentials = service_account.Credentials.from_service_account_file('YOUR_SERVICE_ACCOUNT.json')
vision_client = vision.ImageAnnotatorClient(credentials=credentials)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False


Session(app)

wishlist_items = []

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={
        'scope': 'openid email profile',
        'token_endpoint_auth_method': 'client_secret_post'
    }
)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('renovate'))
    return render_template('login.html')
    
   
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    session['state'] = secrets.token_urlsafe(16)  
    

    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce, state=session['state'])

@app.route('/authorize')
def authorize():
    try:
        nonce = secrets.token_urlsafe(16)
        session['nonce'] = nonce
        session['state'] = secrets.token_urlsafe(16)
        redirect_uri = url_for('authorize_callback', _external=True)
        return google.authorize_redirect(redirect_uri, nonce=nonce, state=session['state'])
    except Exception as e:
        print(f"Exception during authorization: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/authorize_callback')
def authorize_callback():
    try:
        token = google.authorize_access_token()
        nonce = session.pop('nonce', None)
        if nonce is None:
            return jsonify({'error': 'Nonce not found in session'}), 400
        user_info = google.parse_id_token(token, nonce=nonce)
        session['user'] = user_info  
        return redirect(url_for('renovate'))  
    except Exception as e:
        print(f"Exception during authorization: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/design')
@login_required
def renovate():
    return render_template('design.html', active_page='design')


@app.route('/fusion')
@login_required
def fusion():
    return render_template('fusion.html')

@app.route('/search', methods=['POST'])
@login_required
def search():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    category = data.get('category')

    if not lat or not lng:
        print("Invalid location data provided:", lat, lng)
        return jsonify({'error': 'Invalid location data provided.'}), 400
    
    category_type_map = {
        "Furniture Stores": "furniture_store",
        "Electronic Stores": "electronics_store",
        "Electricians": "electrician",
        "Plumbers": "plumber",
        "Interior Designers": "interior_designer"
    }

    types = category_type_map.get(category, None)
    
    if not types:
        return jsonify({'error': 'Invalid category selected.'}), 400

    # Use Google Places API to search for places based on category
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type={types}&keyword={category}&key={GOOGLE_MAPS_API_KEY}"

    response = requests.get(places_url)
    places = response.json()

    # Extract useful information
    if 'results' in places and len(places['results']) > 0:
        results = [{
            'name': place['name'],
            'address': place['vicinity'],
            'rating': place.get('rating', 'N/A'),
            'open_now': place['opening_hours'].get('open_now') if 'opening_hours' in place else None,
            'lat': place['geometry']['location']['lat'],
            'lng': place['geometry']['location']['lng']
        } for place in places['results']]
        return jsonify({'results': results})
    else:
        # No relevant places found
        return jsonify({'results': [], 'message': f'No {category} found in the selected location.'})

@app.route('/generate_images', methods=['POST'])
def generate_images():
    data = request.json
    style = data.get('style')

    if not style:
        return jsonify({"error": "No style selected"}), 400


    bucket = storage_client.bucket(BUCKET_NAME)
    prefix = f"{style}/" 

    image_urls = []
    blobs = list(bucket.list_blobs(prefix=prefix))
    if not blobs:
        return jsonify({"error": "No images found in this category"}), 404

    selected_blobs = random.sample(blobs, min(3, len(blobs)))

    image_urls = []
    for blob in selected_blobs:
        image_url = blob.generate_signed_url(
            expiration=timedelta(minutes=15),  
            version="v4"
        )
        image_urls.append(image_url)

    return jsonify({"images": image_urls})
    

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
