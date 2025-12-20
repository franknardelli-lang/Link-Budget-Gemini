# Link Budget Calculator Documentation

This directory contains the static HTML documentation for the Link Budget Calculator, designed to be hosted on Azure Static Web Apps.

## Deployment Instructions

### Prerequisites
- An Azure account with an active subscription (free tier works)
- Your GitHub repository connected to Azure

### Step 1: Create Azure Static Web App

1. Log in to the [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Static Web App" and select it
4. Click "Create"

### Step 2: Configure the Static Web App

Fill in the following details:

- **Subscription**: Select your subscription
- **Resource Group**: Create new or select existing
- **Name**: Choose a unique name (e.g., `link-budget-docs`)
- **Plan type**: Select "Free"
- **Region**: Choose the closest region to your users
- **Source**: Select "GitHub"
- **Organization**: Your GitHub username
- **Repository**: `Link-Budget-Gemini`
- **Branch**: `main`

### Step 3: Build Configuration

In the build details section:

- **Build Presets**: Select "Custom"
- **App location**: `/docs`
- **Api location**: (leave empty)
- **Output location**: (leave empty)

Click "Review + create" then "Create"

### Step 4: Get Your URL

After deployment completes (takes 2-3 minutes):

1. Go to your Static Web App resource in Azure Portal
2. Click "Overview"
3. Copy the URL (format: `https://<your-app-name>.azurestaticapps.net`)

### Step 5: Update app.py

1. Open `app.py` in your project
2. Find line 110 where it says:
   ```python
   doc_url = "https://your-app-name.azurestaticapps.net"
   ```
3. Replace with your actual Azure Static Web Apps URL
4. Commit and push the change

### Step 6: Add GitHub Secret (Automatic)

Azure automatically creates a GitHub secret `AZURE_STATIC_WEB_APPS_API_TOKEN` in your repository when you connect it. This allows the GitHub Actions workflow to deploy updates automatically.

## Automatic Deployments

Once configured, any changes to the `docs/` folder pushed to the `main` branch will automatically trigger a deployment via GitHub Actions.

### Manual Deployment

You can also trigger a manual deployment:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Azure Static Web Apps CI/CD"
4. Click "Run workflow"

## File Structure

```
docs/
├── index.html                    # Main documentation page
├── staticwebapp.config.json      # Azure Static Web Apps configuration
└── README.md                     # This file
```

## Monitoring

View deployment status:
- **GitHub Actions**: Check the "Actions" tab in your repository
- **Azure Portal**: Go to your Static Web App resource > "Deployment history"

## Troubleshooting

### Deployment fails
- Check GitHub Actions logs for errors
- Verify the `app_location` in the workflow file is set to `/docs`
- Ensure the GitHub secret `AZURE_STATIC_WEB_APPS_API_TOKEN` exists

### 404 errors
- The `staticwebapp.config.json` file handles routing
- All routes fall back to `index.html`

### Updates not showing
- Check deployment status in Azure Portal
- Clear browser cache
- Wait 1-2 minutes for CDN propagation

## Cost

Azure Static Web Apps Free tier includes:
- 100 GB bandwidth per month
- Custom domains
- Automatic SSL certificates
- Global CDN distribution

This is more than sufficient for documentation hosting.
