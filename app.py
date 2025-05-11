from flask import Flask, request, render_template, send_from_directory, redirect, url_for, session, flash, make_response
import os
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
from utils.helpers import safe_join, login_required, save_file
from config import BASE_DIR, USERS, LOG_FILE, SECRET_KEY, MAX_CONTENT_LENGTH

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.errorhandler(413)
def request_entity_too_large(error):
    return make_response("File too large. Maximum size is 10 GB.", 413)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            logging.info(f"User {username} logged in")
            return redirect(url_for('browse'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    session.pop('username', None)
    logging.info(f"User {username} logged out")
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/<path:subpath>', methods=['GET', 'POST'])
@login_required
def browse(subpath):
    rel_path = subpath.strip("/")
    try:
        abs_path = safe_join(BASE_DIR, rel_path)
        if not os.path.exists(abs_path):
            return "Path not found", 404
        if not os.path.isdir(abs_path):
            return "Not a directory", 403
    except ValueError:
        return "Access Denied", 403

    message = None
    if request.method == 'POST' and 'files' in request.files:
        files = request.files.getlist("files")
        for f in files:
            if f and f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join(abs_path, filename))
                logging.info(f"User {session['username']} uploaded file: {filename} to {rel_path}")
        return redirect(request.path)

    items = os.listdir(abs_path)
    folders = sorted([x for x in items if os.path.isdir(os.path.join(abs_path, x))])
    files = sorted([x for x in items if os.path.isfile(os.path.join(abs_path, x))])

    return render_template(
        'file_manager.html',
        rel_path=rel_path,
        parent_path=os.path.dirname(rel_path),
        folders=folders,
        files=files,
        message=message,
        os=os
    )

@app.route('/download/<path:subpath>')
@login_required
def download_file(subpath):
    rel_path = subpath.strip("/")
    try:
        abs_path = safe_join(BASE_DIR, rel_path)
        if not os.path.isfile(abs_path):
            return "File not found", 404
        directory = os.path.dirname(abs_path)
        filename = os.path.basename(abs_path)
        logging.info(f"User {session['username']} downloaded file: {filename} from {rel_path}")
        return send_from_directory(directory, filename, as_attachment=False)
    except ValueError:
        return "Access Denied", 403

@app.route('/create-folder/<path:subpath>', methods=['POST'])
@login_required
def create_folder(subpath):
    rel_path = subpath.strip("/")
    try:
        abs_path = safe_join(BASE_DIR, rel_path)
        folder_name = secure_filename(request.form.get("folder_name"))
        if folder_name:
            os.makedirs(os.path.join(abs_path, folder_name), exist_ok=True)
            logging.info(f"User {session['username']} created folder: {folder_name} in {rel_path}")
        return redirect(url_for("browse", subpath=subpath))
    except ValueError:
        return "Access Denied", 403

@app.route('/delete/<path:subpath>', methods=['POST'])
@login_required
def delete_file(subpath):
    try:
        abs_path = safe_join(BASE_DIR, subpath)
        if not os.path.isfile(abs_path):
            return "File not found", 404
        filename = os.path.basename(abs_path)
        os.remove(abs_path)
        logging.info(f"User {session['username']} deleted file: {filename} from {subpath}")
        parent = os.path.dirname(subpath)
        return redirect(url_for("browse", subpath=parent))
    except ValueError:
        return "Access Denied", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)