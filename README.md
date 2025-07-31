# maleware-sandbox-simulator
Safely execute non-infectious malware samples in a controlled environment and log behavioral indicators (filesystem, network, process activity).

# How to run this project?
python3 -m venv venv

source venv/bin/activate

poetry install

# Copy .env.example file and then create .env
Place a secret key

# Run Flask app
python run.py
