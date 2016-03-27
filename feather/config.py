import hashlib

config = {
    "session_secret":"82d65a575279b463b10fbb964ee0f7a9",
}

def set_secret_key(key):
    config[key] = hashlib.md5(key).hexdigest()
