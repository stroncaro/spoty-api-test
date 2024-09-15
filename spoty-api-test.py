from pathlib import Path
import json
import requests

SPOTIFY_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

# Get directories
script_directory = Path(__file__).parent
keys_directory = script_directory / "keys"

# Check keys directory exists
if not (keys_directory.exists() and keys_directory.is_dir()):
    raise FileNotFoundError

# Get json objects in keys directory
key_json_files = keys_directory.glob("*.json")
if not key_json_files:
    raise FileNotFoundError

# Try each one for valid keys
access_token_json = {}
for json_file in key_json_files:
    with json_file.open() as file:
        keys: dict = json.load(file)
        if all(
            required_field in keys for required_field in ["client_id", "client_secret"]
        ):
            print(f"{json_file.name} has required fields")

            # Request access token
            keys["grant_type"] = "client_credentials"
            response = requests.post(
                SPOTIFY_TOKEN_ENDPOINT,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=keys,
                timeout=10,
            )

            # Handle failure
            if response.status_code != 200:
                print("Could not get access token. Got:")
                print(f"  STATUS {response.status_code}\n  {response.text}")
                continue

            # Success
            print("Got access token!")
            access_token_json = response.json()

        else:
            print(f"{json_file.name} doesn't have required fields")
