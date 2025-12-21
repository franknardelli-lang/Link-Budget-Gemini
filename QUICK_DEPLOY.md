# Quick Deployment Checklist

Follow these steps to deploy your Link Budget Calculator to Azure Container Apps.

## Prerequisites Checklist

- [ ] Azure account created ([Sign up](https://azure.microsoft.com/free/))
- [ ] Docker Hub account created ([Sign up](https://hub.docker.com/signup))
- [ ] Azure CLI installed ([Installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli))
- [ ] Docker Desktop installed ([Get Docker](https://www.docker.com/products/docker-desktop/))
- [ ] Docker Desktop is running

## Configuration

1. **Edit `deploy-to-azure.sh`** - Change this line to YOUR Docker Hub username:

```bash
DOCKER_USERNAME="franknardelli"  # <-- CHANGE THIS to your Docker Hub username
```

2. **Optional**: Customize other settings in the same file:
   - `IMAGE_NAME` - Name for your container image
   - `RESOURCE_GROUP` - Azure resource group name
   - `LOCATION` - Azure region (e.g., "eastus", "westus", "westeurope")
   - `CONTAINER_APP_NAME` - Name for your container app

## Deployment Steps

### 1. Login to Services

```bash
# Login to Azure (opens browser)
az login

# Login to Docker Hub (enter username and password when prompted)
docker login
```

### 2. Deploy

```bash
# Make script executable (first time only)
chmod +x deploy-to-azure.sh

# Run deployment
./deploy-to-azure.sh
```

### 3. Wait

The script will:
- ✓ Build Docker image (~2-3 minutes)
- ✓ Push to Docker Hub (~1-2 minutes)
- ✓ Create Azure resources (~1 minute)
- ✓ Deploy container app (~2-3 minutes)

**Total time: ~6-9 minutes**

### 4. Access Your App

When complete, you'll see:

```
========================================
Deployment Complete!
========================================
Your Link Budget Calculator is available at:
https://link-budget-app.XXXXXXX.eastus.azurecontainerapps.io
========================================
```

Open that URL in your browser!

## Verify It Works

1. Open the URL in your browser
2. You should see the Link Budget Calculator interface
3. Adjust some parameters and verify calculations work
4. Check that the plot updates correctly

## Update Your App

After making code changes:

```bash
./deploy-to-azure.sh
```

The script automatically detects if the app exists and updates it.

## Common Issues

### "docker: command not found"
**Solution**: Make sure Docker Desktop is installed and running

### "not logged into Azure CLI"
**Solution**: Run `az login`

### "Docker build failed"
**Solution**: Check that you're in the project directory with the Dockerfile

### "Docker push failed"
**Solution**: Run `docker login` and enter your Docker Hub credentials

## What Gets Created in Azure?

- **Resource Group**: `link-budget-rg` (or your custom name)
- **Container Environment**: `link-budget-env` (shared infrastructure)
- **Container App**: `link-budget-app` (your application)

These are **independent** resources that don't affect your existing Azure deployments.

## Cost

Azure Container Apps has a **free tier**:
- 180,000 vCPU-seconds per month
- 360,000 GiB-seconds per month

With the default configuration (0.5 vCPU, 1.0 GiB), this is sufficient for moderate usage. The app scales to zero when not in use (no cost when idle).

## Next Steps

1. ✓ Deploy the app (you're here!)
2. Test all functionality
3. Share the URL with others
4. Set up custom domain (optional)
5. Configure CI/CD with GitHub Actions (optional)

For detailed information, see [CONTAINER_APPS_DEPLOYMENT.md](CONTAINER_APPS_DEPLOYMENT.md)

## Getting Help

- Check [CONTAINER_APPS_DEPLOYMENT.md](CONTAINER_APPS_DEPLOYMENT.md) for troubleshooting
- Review deployment logs in Azure Portal
- Check container logs: `az containerapp logs show --name link-budget-app --resource-group link-budget-rg --tail 50`

---

**Ready to deploy?** Start with Step 1 above!
