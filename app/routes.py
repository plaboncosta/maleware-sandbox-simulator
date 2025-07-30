import json
import os

import yaml
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

from sandbox import sandbox_controller

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'py', 'exe', 'bat', 'sh'}


def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading config: {e}")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def home():
    return render_template('dashboard.html')


@main.route('/upload', methods=['POST'])
def upload():
    if 'sample' not in request.files:
        flash('No file part in request.')
        return redirect(url_for('main.home'))

    file = request.files['sample']

    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('main.home'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        config = load_config()

        # Run analysis
        logs = sandbox_controller.run_sample(path, config)

        # Save analysis result to file
        result_path = os.path.join(config['sandbox']['log_directory'], f"{filename}_log.json")
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        with open(result_path, 'w') as f:
            json.dump(logs, f, indent=2)

        return redirect(url_for('main.view_result', filename=filename))

    flash('Invalid file type. Allowed: .py, .exe, .bat, .sh')
    return redirect(url_for('main.home'))


@main.route('/results/<filename>')
def view_result(filename):
    log_path = os.path.join('logs', f"{filename}_log.json")
    if not os.path.exists(log_path):
        flash('Log file not found.')
        return redirect(url_for('main.home'))

    with open(log_path) as f:
        logs = json.load(f)

    return render_template('dashboard.html', logs=logs, filename=filename)
