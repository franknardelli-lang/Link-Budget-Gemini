# Azure Container Apps Deployment Guide

This guide explains how to deploy the **Link Budget Calculator Streamlit app** to Azure Container Apps as an independent, containerized web application.

## Overview

This deployment:
- Creates a **separate** Azure Container App (doesn't affect existing deployments)
- Hosts the Streamlit application in a Docker container
- Provides auto-scaling from 0 to 2 replicas
- Includes health checks for reliability
- Uses your Docker Hub account for container images

## Prerequisites

Before starting, ensure you have:

1. **Azure Account**
   - Free tier is sufficient: [Sign up here](https://azure.microsoft.com/free/)
   - Azure CLI installed: [Installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

2. **Docker Hub Account**
   - Free tier is sufficient: [Sign up here](https://hub.docker.com/signup)
   - Docker Desktop installed: [Get Docker](https://www.docker.com/products/docker-desktop/)

3. **Local Tools**
   - Docker running on your machine
   - Azure CLI installed and available in terminal
   - Bash shell (Git Bash on Windows, native on Mac/Linux)

## Quick Deployment

### Step 1: Configure the Script

Edit [deploy-to-azure.sh](deploy-to-azure.sh) and customize these values:

```bash
DOCKER_USERNAME="franknardelli"           # Change to YOUR Docker Hub username
IMAGE_NAME="link-budget-calculator"       # Optional: change image name
RESOURCE_GROUP="link-budget-rg"          # Optional: change resource group name
LOCATION="eastus"                         # Optional: change Azure region
CONTAINER_APP_NAME="link-budget-app"     # Optional: change app name
CONTAINER_ENV_NAME="link-budget-env"     # Optional: change environment name
```

**Important**: Change `DOCKER_USERNAME` to match your Docker Hub account.

### Step 2: Login to Required Services

```bash
# Login to Azure
az login

# Login to Docker Hub
docker login
# Enter your Docker Hub username and password when prompted
```

### Step 3: Run Deployment

```bash
./deploy-to-azure.sh
```

The script will:
1. Build the Docker image
2. Push it to Docker Hub
3. Create Azure resources (resource group, Container Apps environment)
4. Deploy or update the container app
5. Display your application URL

### Step 4: Access Your Application

After deployment completes, you'll see:

```
========================================
Deployment Complete!
========================================
Your Link Budget Calculator is available at:
https://link-budget-app.randomhash.eastus.azurecontainerapps.io
========================================
```

Open the URL in your browser to use your deployed app.

## Files Created

```
Link-Budget-Gemini/
├── Dockerfile                          # Container image configuration
├── deploy-to-azure.sh                  # Automated deployment script
└── CONTAINER_APPS_DEPLOYMENT.md       # This file
```

## Architecture

### Docker Container

The [Dockerfile](Dockerfile) creates a container with:
- **Base Image**: Python 3.11 slim (Debian Bookworm)
- **Dependencies**: Streamlit, NumPy, Matplotlib (from requirements.txt)
- **Port**: 8501 (Streamlit default)
- **Health Check**: Every 30s via Streamlit's built-in health endpoint
- **Entry Point**: Runs `streamlit run app.py`

### Azure Resources Created

The deployment creates these Azure resources:

1. **Resource Group**: `link-budget-rg`
   - Container for all related resources
   - Can be customized via `RESOURCE_GROUP` variable

2. **Container Apps Environment**: `link-budget-env`
   - Shared environment for container apps
   - Manages networking and logging
   - Reused if it already exists

3. **Container App**: `link-budget-app`
   - Your Streamlit application
   - Auto-scales: 0-2 replicas
   - CPU: 0.5 cores per replica
   - Memory: 1.0 GiB per replica
   - Public ingress on port 8501

## Updating Your Application

To deploy updates after changing your code:

```bash
# Method 1: Use the deployment script (rebuilds and redeploys)
./deploy-to-azure.sh

# Method 2: Manual update (if image is already on Docker Hub)
az containerapp update \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --image franknardelli/link-budget-calculator:latest
```

## Managing Your Deployment

### View Application Logs

```bash
# Real-time logs
az containerapp logs show \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --follow

# Recent logs
az containerapp logs show \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --tail 100
```

### Check Application Status

```bash
az containerapp show \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --query "{Status:properties.runningStatus, URL:properties.configuration.ingress.fqdn}"
```

### Scale Configuration

```bash
# Update scaling limits
az containerapp update \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --min-replicas 1 \
    --max-replicas 5

# Update resources
az containerapp update \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --cpu 1.0 \
    --memory 2.0Gi
```

### Delete Resources

```bash
# Delete just the container app
az containerapp delete \
    --name link-budget-app \
    --resource-group link-budget-rg

# Delete entire resource group (including all resources)
az group delete --name link-budget-rg
```

## Cost Information

Azure Container Apps pricing:
- **Free tier**: 180,000 vCPU-seconds, 360,000 GiB-seconds per month
- **Consumption tier** (beyond free): ~$0.000012 per vCPU-second
- With 0.5 vCPU, 1.0 GiB: Very low cost for low-traffic applications
- Scales to zero when not in use (no cost when idle)

See [Azure Container Apps Pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)

## Troubleshooting

### Build Fails

```bash
# Check Dockerfile syntax
docker build -t test-build .

# Verify requirements.txt is valid
cat requirements.txt
```

### Push to Docker Hub Fails

```bash
# Verify you're logged in
docker info | grep Username

# Login again if needed
docker login
```

### Azure Deployment Fails

```bash
# Check Azure CLI login
az account show

# Re-login if needed
az login

# Verify subscription
az account list --output table

# Set correct subscription if you have multiple
az account set --subscription "Your Subscription Name"
```

### Application Not Responding

```bash
# Check container app status
az containerapp show \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --query properties.runningStatus

# Check recent logs
az containerapp logs show \
    --name link-budget-app \
    --resource-group link-budget-rg \
    --tail 50

# Restart the app
az containerapp revision restart \
    --name link-budget-app \
    --resource-group link-budget-rg
```

### Health Check Failures

If health checks fail, verify in [Dockerfile](Dockerfile:14):
- Port 8501 is exposed
- Streamlit runs with `--server.headless=true`
- curl is installed in the container

## Differences from streamlit-antenna-public

This deployment uses the same approach as your `streamlit-antenna-public` project:

- Same Dockerfile structure (Python 3.11, Streamlit on port 8501)
- Same deployment script pattern (bash automation)
- Same Azure Container Apps configuration

**Key differences** (customized for this project):
- Resource names: `link-budget-*` instead of antenna-related names
- Main file: `app.py` instead of `Home.py`
- Image name: `link-budget-calculator`

This ensures it's **completely independent** and won't interfere with your existing deployment.

## Next Steps

After successful deployment:

1. Test all features of your deployed app
2. Set up custom domain (optional): [Guide](https://learn.microsoft.com/en-us/azure/container-apps/custom-domains-managed-certificates)
3. Configure environment variables if needed
4. Set up monitoring and alerts
5. Consider CI/CD with GitHub Actions (see below)

## Optional: GitHub Actions CI/CD

To automate deployments on every push to `main`:

<details>
<summary>Click to see GitHub Actions workflow example</summary>

Create `.github/workflows/deploy-container-app.yml`:

```yaml
name: Deploy to Azure Container Apps

on:
  push:
    branches: [ main ]
  workflow_dispatch:

env:
  DOCKER_USERNAME: franknardelli
  IMAGE_NAME: link-budget-calculator
  RESOURCE_GROUP: link-budget-rg
  CONTAINER_APP_NAME: link-budget-app

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ env.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ env.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Deploy to Azure Container Apps
      uses: azure/CLI@v1
      with:
        inlineScript: |
          az containerapp update \
            --name ${{ env.CONTAINER_APP_NAME }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --image ${{ env.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest
```

**Required GitHub Secrets:**
- `DOCKER_PASSWORD`: Your Docker Hub password or access token
- `AZURE_CREDENTIALS`: Azure service principal credentials

</details>

## Resources

- [Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Hub](https://hub.docker.com/)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Azure Container Apps logs
3. Verify all prerequisites are met
4. Check Docker Hub for successful image push
5. Review Azure Portal for resource status

---

**Note**: This is an **independent deployment** that doesn't affect your existing Azure Container Apps. You can have multiple container apps running simultaneously in different resource groups or even the same resource group with different names.
