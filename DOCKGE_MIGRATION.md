# Dockge Migration Guide

This guide will help you migrate from the manual Docker deployment to a Docker Compose setup compatible with Dockge.

## ✅ What Has Been Created

1. **compose.yaml** - Docker Compose configuration file
2. **Updated deploy.sh** - Deployment script that uses Docker Compose
3. **This guide** - Step-by-step migration instructions

## 📋 Step 1: One-Time Server Setup

Run these commands **on your server** (192.168.2.90) to create the Dockge directory structure:

```bash
# SSH into your server
ssh alan@192.168.2.90

# Create the stacks directory with proper permissions
sudo mkdir -p /opt/stacks/link-budget-gemini
sudo chown -R alan:alan /opt/stacks
sudo chmod -R 755 /opt/stacks

# Verify the permissions
ls -la /opt/stacks
```

You should see output showing that `alan` owns the directory.

## 🧹 Step 2: Clean Up Old Container (Optional)

If you want to remove the old manually-created container:

```bash
# SSH into your server (if not already connected)
ssh alan@192.168.2.90

# Stop and remove the old container
docker stop link-budget-container
docker rm link-budget-container

# Optionally remove the old image
docker rmi link-budget-app
```

## 🚀 Step 3: Deploy Using the New Script

From your **local development machine**, run:

```bash
cd /home/alan/development/Link-Budget-Gemini
./deploy.sh
```

The script will:
1. Push your code to GitHub
2. Clone/pull the repo into `/opt/stacks/link-budget-gemini` on the server
3. Run `docker compose up -d --build` to build and start the container

## 🎯 Step 4: Verify Deployment

Check that your app is running:

```bash
# From your local machine
curl http://192.168.2.90:8502

# Or open in browser
# http://192.168.2.90:8502
```

## 🔍 Step 5: Managing with Dockge

If you're using Dockge's web interface:

1. Open Dockge (usually at `http://192.168.2.90:5001`)
2. You should see `link-budget-gemini` stack in `/opt/stacks`
3. You can now manage (start/stop/restart) the container from Dockge's UI

## 📝 Key Changes Summary

| Aspect | Old Setup | New Setup |
|--------|-----------|-----------|
| Location | `~/apps/Link-Budget-Gemini` | `/opt/stacks/link-budget-gemini` |
| Deployment | Manual docker commands | `docker compose up -d --build` |
| Configuration | Command-line flags | `compose.yaml` file |
| Management | SSH + docker CLI | SSH, CLI, or Dockge UI |

## 🛠️ Troubleshooting

### Permission Denied
If you get permission errors:
```bash
sudo chown -R alan:alan /opt/stacks/link-budget-gemini
```

### Container Not Starting
Check logs:
```bash
ssh alan@192.168.2.90
cd /opt/stacks/link-budget-gemini
docker compose logs
```

### Port Already in Use
If port 8502 is already taken by the old container:
```bash
docker ps -a | grep 8502
docker stop <container-name>
docker rm <container-name>
```

## 🔄 Future Deployments

Simply run from your local machine:
```bash
./deploy.sh
```

This will:
- Push code to GitHub
- Pull latest code on server
- Rebuild and restart the container with zero downtime
