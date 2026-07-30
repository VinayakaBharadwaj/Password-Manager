import json
import os

VAULT_FILE = "vault.json"

def initialize_vault(salt_hex: str, verification_hex: str):
    """Creates a brand new vault file structure on disk."""
    data = {
        "salt": salt_hex,
        "verification": verification_hex,
        "credentials": {}
    }
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_vault() -> dict:
    """Reads the JSON database file. Returns empty dict if file doesn't exist."""
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_credentials(credentials: dict):
    """Updates only the passwords section of the database."""
    vault = load_vault()
    if not vault:
        return
    vault["credentials"] = credentials
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)