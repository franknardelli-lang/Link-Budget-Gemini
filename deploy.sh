#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# Configuration for Link-Budget-Gemini App
SERVER_USER="alan"
SERVER_IP="192.168.1.162"
APP_FOLDER="~/apps/Link-Budget-Gemini" # <-- Updated project folder
REPO_URL="https://github.com/franknardelli-lang/Link-Budget-Gemini.git"
IMAGE_NAME="link-budget-app"           # <-- Unique image name
CONTAINER_NAME="link-budget-container" # <-- Unique container name

echo "🚀 Pushing changes to GitHub..."
git push

echo "🔄 Deploying to Linux Server ($SERVER_IP) using Docker..."

# Execute the commands on the remote server via SSH
# We pipe the commands to the remote server to avoid complex quoting issues.
# The 'bash -s' command on the remote end executes the script from standard input.
ssh $SERVER_USER@$SERVER_IP 'bash -s' <<EOF
	set -e # Ensure remote script also exits on error

	# Check if the app directory exists, if not, clone the repo
	if [ -d "$APP_FOLDER" ]; then
	  echo "[REMOTE] App directory exists. Pulling latest code..."
	  cd "$APP_FOLDER"
	  git pull
	else
	  # Ensure parent directory exists and clone
	  mkdir -p ~/apps
	  echo "[REMOTE] App directory not found. Cloning repository..."
	  git clone "$REPO_URL" "$APP_FOLDER"
	  cd "$APP_FOLDER"
	fi

	echo "[REMOTE] Building Docker image '$IMAGE_NAME'..."
	docker build -t $IMAGE_NAME .

	echo "[REMOTE] Stopping and removing old container '$CONTAINER_NAME' (if it exists)..."
	docker stop $CONTAINER_NAME || true
	docker rm $CONTAINER_NAME || true

	echo "[REMOTE] Starting new container '$CONTAINER_NAME'..."
	# Maps host port 8502 to the container's internal port 8501
	docker run -d --restart unless-stopped --name $CONTAINER_NAME -p 8502:8501 $IMAGE_NAME
EOF

echo "✅ Deployment complete! App should be running at http://$SERVER_IP:8502"