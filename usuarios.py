import json
import bcrypt

usuarios = {
    "ivan": bcrypt.hashpw("ivan123".encode(), bcrypt.gensalt()).decode(),
    "user": bcrypt.hashpw("user_1".encode(), bcrypt.gensalt()).decode(),
    "u": bcrypt.hashpw("123".encode(), bcrypt.gensalt()).decode()
}

with open("usuarios.json", "w") as f:
    json.dump(usuarios, f, indent=4)