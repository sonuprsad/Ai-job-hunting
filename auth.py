import json
import os

USERS_FILE = "auth/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register(username, password, role):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return False, "User already exists"

    users.append({
        "username": username,
        "password": password,
        "role": role
    })

    save_users(users)
    return True, "Registered successfully"

def login(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True, "Login successful", user["role"]

    return False, "Invalid credentials", None