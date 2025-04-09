import requests
import pandas as pd

def get_spotify_token(client_id, client_secret):
    try:
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': 'fb35b8804b3647b5923d55f472f908d7',
            'client_secret': '2b8d0176b0a444f3b8fac85e14efd48e',
        })
        auth_response.raise_for_status()  # Raise an HTTPError for bad responses
        auth_data = auth_response.json()
        return auth_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error getting Spotify token: {e}")
        return None

def search_track(track_name, artist_name, token):
    try:
        query = f"{track_name} artist:{artist_name}"
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        json_data = response.json()
        items = json_data.get('tracks', {}).get('items', [])

        if items:
            first_result = items[0]
            return first_result['id']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error searching track: {e}")
        return None

def get_track_details(track_id, token):
    try:
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        json_data = response.json()
        image_url = json_data.get('album', {}).get('images', [])[0].get('url')
        return image_url
    except requests.exceptions.RequestException as e:
        print(f"Error getting track details: {e}")
        return None

# Your Spotify API Credentials
client_id = 'fb35b8804b3647b5923d55f472f908d7'
client_secret = '2b8d0176b0a444f3b8fac85e14efd48e'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

if access_token:
    # Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
    try:
        df_spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

        # Create an empty list to cover URL
        cover_urls = []

        # Loop through each row to get track details and add to DataFrame
        for i, row in df_spotify.iterrows():
            track_id = search_track(row['track_name'], row['artist(s)_name'], access_token)
            if track_id:
                image_url = get_track_details(track_id, access_token)
                df_spotify.at[i, 'image_url'] = image_url

        # Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
        df_spotify.to_csv('updated_file.csv', index=False)

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: Unable to parse the CSV file.")
else:
    print("Error: Access token not obtained. Check your credentials and network connection.")