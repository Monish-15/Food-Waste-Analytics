import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def log(msg):
    print(f"[LOG] {msg}")
