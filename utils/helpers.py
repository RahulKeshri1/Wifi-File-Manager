import os
from flask import redirect, url_for, session
import shutil

def safe_join(base, *paths):
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(os.path.abspath(base)):
        raise ValueError("Unsafe path")
    return final_path

def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def save_file(file, path):
    with open(path, 'wb') as f:
        shutil.copyfileobj(file.stream, f)