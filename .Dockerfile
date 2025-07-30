FROM python:3.11-slim

WORKDIR /sandbox

COPY . .

RUN apt update && apt install -y tcpdump iptables && \
    pip install flask watchdog pyyaml

EXPOSE 5000

CMD ["python3", "run.py"]