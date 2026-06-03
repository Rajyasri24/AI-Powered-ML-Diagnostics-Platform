import os

def ensure_dirs():
    os.makedirs("static", exist_ok=True)