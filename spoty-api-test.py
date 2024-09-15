from pathlib import Path
import json
import requests

SPOTIFY_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
SPOTIFY_CLIENT_DATA_FIELDS = ["client_id", "client_secret"]


def GetKeysDirectory():
    script_directory = Path(__file__).parent
    keys_directory = script_directory / "keys"
    if not (keys_directory.exists() and keys_directory.is_dir()):
        raise FileNotFoundError()
    return keys_directory


def GetKeysJsonFilePaths():
    key_json_files = GetKeysDirectory().glob("*.json")
    if not key_json_files:
        raise FileNotFoundError()
    return key_json_files


def GetClientDataFromJson(path: Path):
    with path.open() as file:
        data: dict = json.load(file)
    try:
        values = (data[field] for field in SPOTIFY_CLIENT_DATA_FIELDS)
    except KeyError:
        print(f"{path.name} is invalid")
        return None

    return {key: value for key, value in zip(SPOTIFY_CLIENT_DATA_FIELDS, values)}


def RequestAccessToken(client_data: dict | None):
    if not client_data:
        return None

    client_data["grant_type"] = "client_credentials"
    response = requests.post(
        SPOTIFY_TOKEN_ENDPOINT,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=client_data,
        timeout=10,
    )

    if response.status_code != 200:
        print("Could not get access token. Got:")
        print(f"  STATUS {response.status_code}\n  {response.text}")
        return None

    access_token: str = response.json()["access_token"]
    return access_token


def GetAccessToken():
    for key_json in GetKeysJsonFilePaths():
        client_data = GetClientDataFromJson(key_json)
        access_token = RequestAccessToken(client_data)
        if access_token:
            return access_token

    raise RuntimeError("Couldn't get an access token")


if __name__ == "__main__":
    access_token = GetAccessToken()
    print(f"Got access token: {access_token}")
