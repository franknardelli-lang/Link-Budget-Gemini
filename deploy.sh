#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# Configuration for Link-Budget-Gemini App
SERVER_USER="alan"
SERVER_IP="192.168.1.162"
APP_FOLDER="~/apps/Link-Budget-Gemini" # <-- Updated project folder
IMAGE_NAME="link-budget-app"           # <-- Unique image name
CONTAINER_NAME="link-budget-container" # <-- Unique container name

echo "🚀 Pushing changes to GitHub..."
git push

echo "🔄 Deploying to Linux Server ($SERVER_IP) using Docker..."

# Define the sequence of commands to be executed on the remote server.
REMOTE_COMMANDS=$(cat <<EOF
set -e # Ensure remote script also exits on error

echo "[REMOTE] Changing to app directory: $APP_FOLDER"
cd $APP_FOLDER

echo "[REMOTE] Pulling latest code from GitHub..."
git pull

echo "[REMOTE] Building Docker image '$IMAGE_NAME'..."
docker build -t $IMAGE_NAME .

echo "[REMOTE] Stopping and removing old container '$CONTAINER_NAME' (if it exists)..."
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

echo "[REMOTE] Starting new container '$CONTAINER_NAME'..."
# Maps host port 8502 to the container's internal port 8501
docker run -d --restart unless-stopped --name $CONTAINER_NAME -p 8502:8501 $IMAGE_NAME
EOF
)

# Execute the commands on the remote server via SSH
ssh $SERVER_USER@$SERVER_IP "bash -c '$REMOTE_COMMANDS'"

echo "✅ Deployment complete! App should be running at http://$SERVER_IP:8502"