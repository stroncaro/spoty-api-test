from pathlib import Path
import json

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
for json_file in key_json_files:
    with json_file.open() as file:
        keys: dict = json.load(file)
        if all(
            required_field in keys for required_field in ["client_id", "client_secret"]
        ):
            print(f"{json_file.name} has required fields")
            # Request access token
            break
        else:
            print(f"{json_file.name} doesn't have required fields")
