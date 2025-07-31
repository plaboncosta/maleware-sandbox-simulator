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

# Docker build & run
# Rebuild with updated entrypoint.sh
docker build -t sandbox .

# Create custom network (non-internal so browser access works)
docker network create no-internet-visible

# Run the container on that network
docker run -d --rm -p 5000:5000 \
  --name sandbox_container \
  --network no-internet-visible \
  sandbox