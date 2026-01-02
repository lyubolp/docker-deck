# Docker Deck

A lightweight web dashboard for monitoring and managing your Docker-based web services.

## Features

- Real-time Docker container monitoring
- Auto-refresh every 5 seconds
- Display container state, ports, and images

## Prerequisites

- Docker installed and running
- Python 3.13+ (if running locally with uv)
- uv package manager (if running locally)

## Running with Docker

The easiest way to run Docker Deck is using Docker itself:

```bash
# Build the Docker image
docker build -t docker-deck:latest .

# Run the container
# Note: Mount the Docker socket to allow container monitoring
docker run -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock docker-deck:latest
```

Then open your browser and navigate to `http://localhost:8080`

## Running Locally with uv

If you prefer to run Docker Deck locally without Docker:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/lyubolp/docker-deck.git
cd docker-deck

# Sync dependencies
uv sync

# Run the application
uv run main.py
```

The application will start on `http://localhost:8080` by default.

## How It Works

Docker Deck uses the Docker CLI to fetch information about running and stopped containers. It displays:

- **Container Name**: The name of the Docker container
- **State**: Running or Stopped
- **Port**: The exposed port (if any)
- **Image**: The Docker image used

The dashboard automatically refreshes every 5 seconds to keep the information up-to-date.
