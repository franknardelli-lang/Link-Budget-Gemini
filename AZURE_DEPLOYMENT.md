# Azure Static Web Apps Deployment Guide

This guide will help you deploy the Link Budget Calculator documentation to Azure Static Web Apps (free tier).

## Quick Start (5 minutes)

### 1. Create Azure Static Web App

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "**Create a resource**" → Search "**Static Web App**"
3. Fill in the form:
   - **Name**: `link-budget-docs` (or your choice)
   - **Plan**: **Free**
   - **Region**: Choose closest to you
   - **Source**: **GitHub**
   - **Repository**: `Link-Budget-Gemini`
   - **Branch**: `main`
   - **App location**: `/docs`
   - **Api location**: *(leave empty)*
   - **Output location**: *(leave empty)*
4. Click "**Review + create**" → "**Create**"

### 2. Get Your URL

After 2-3 minutes:
1. Open your Static Web App in Azure Portal
2. Copy the URL from Overview page (e.g., `https://nice-ocean-123abc.azurestaticapps.net`)

### 3. Update app.py

Edit [app.py](app.py) line 110:

```python
# Change this:
doc_url = "https://your-app-name.azurestaticapps.net"

# To your actual URL:
doc_url = "https://nice-ocean-123abc.azurestaticapps.net"
```

### 4. Commit and Push

```bash
git add app.py
git commit -m "Update documentation URL to Azure Static Web Apps"
git push
```

## What Was Created

```
Link-Budget-Gemini/
├── docs/
│   ├── index.html                   # Full documentation page
│   ├── staticwebapp.config.json     # Azure configuration
│   └── README.md                    # Detailed deployment guide
├── .github/workflows/
│   └── azure-static-web-apps.yml   # Auto-deployment workflow
└── AZURE_DEPLOYMENT.md             # This file
```

## How It Works

1. **Documentation**: The [docs/index.html](docs/index.html) contains a complete, professional documentation page with all the link budget theory, equations, and examples.

2. **Auto-Deployment**: The GitHub Actions workflow automatically deploys any changes to the `docs/` folder when you push to the `main` branch.

3. **Free Hosting**: Azure Static Web Apps free tier includes:
   - 100 GB bandwidth/month
   - Custom domain support
   - Free SSL certificate
   - Global CDN

## Testing Locally

To preview the documentation locally:

```bash
cd docs
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Troubleshooting

### GitHub Actions workflow not running

Check if the secret exists:
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Verify `AZURE_STATIC_WEB_APPS_API_TOKEN` exists
3. If missing, Azure should have created it automatically during setup

### Deployment fails

1. Check GitHub Actions tab for error details
2. Verify `app_location: "/docs"` in `.github/workflows/azure-static-web-apps.yml`
3. Make sure `docs/index.html` exists

### URL returns 404

1. Wait 2-3 minutes for initial deployment
2. Check Azure Portal → Your Static Web App → Deployment History
3. Look for a successful deployment

## Next Steps

After deployment:

1. ✅ Test the documentation URL works
2. ✅ Update `app.py` with the real URL
3. ✅ Push changes to GitHub
4. ✅ Verify the Streamlit app's documentation button works
5. (Optional) Set up a custom domain in Azure Portal

## Resources

- [Azure Static Web Apps Documentation](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- [Full deployment instructions](docs/README.md)
- [GitHub Actions workflow](.github/workflows/azure-static-web-apps.yml)
