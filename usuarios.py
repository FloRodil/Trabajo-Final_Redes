# pip install bcrypt
import json
import bcrypt

usuarios = {
    "flo": bcrypt.hashpw("1234".encode(), bcrypt.gensalt()).decode(),
    "user": bcrypt.hashpw("user_1".encode(), bcrypt.gensalt()).decode(),
    "max": bcrypt.hashpw("pass".encode(), bcrypt.gensalt()).decode()
}

with open("usuarios.json", "w") as f:
    json.dump(usuarios, f, indent=4)