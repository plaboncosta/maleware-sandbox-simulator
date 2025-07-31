FROM python:3.12-slim

WORKDIR /sandbox

# Copy project files first (including pyproject.toml)
COPY . .

# Install system dependencies and poetry
RUN apt update && apt install -y tcpdump iptables curl iputils-ping && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]