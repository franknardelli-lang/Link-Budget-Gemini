#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# Configuration for Link-Budget-Gemini App
SERVER_USER="alan"
SERVER_IP="192.168.2.90"
APP_FOLDER="/opt/stacks/link-budget-gemini" # <-- Dockge-compatible location
REPO_URL="https://github.com/franknardelli-lang/Link-Budget-Gemini.git"

echo "🚀 Pushing changes to GitHub..."
git push

echo "🔄 Deploying to Linux Server ($SERVER_IP) using Docker Compose..."

# Execute the commands on the remote server via SSH
ssh $SERVER_USER@$SERVER_IP 'bash -s' <<EOF
	set -e # Ensure remote script also exits on error

	# Check if the app directory exists and is a git repository
	if [ -d "$APP_FOLDER/.git" ]; then
	  echo "[REMOTE] Git repository exists. Pulling latest code..."
	  cd "$APP_FOLDER"
	  git pull
	else
	  echo "[REMOTE] Cloning repository to $APP_FOLDER..."
	  # Remove directory if it exists but is not a git repo
	  rm -rf "$APP_FOLDER"
	  git clone "$REPO_URL" "$APP_FOLDER"
	  cd "$APP_FOLDER"
	fi

	echo "[REMOTE] Deploying with Docker Compose..."
	docker compose up -d --build
EOF

echo "✅ Deployment complete! App should be running at http://$SERVER_IP:8502"