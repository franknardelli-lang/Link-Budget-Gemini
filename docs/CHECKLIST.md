# Azure Deployment Checklist

Use this checklist to track your progress.

## Pre-Deployment
- [ ] Have Azure account (sign up at https://azure.microsoft.com/free/ if needed)
- [ ] Logged into Azure Portal (https://portal.azure.com)
- [ ] Have admin access to GitHub repository

## Azure Portal Setup

### Create Static Web App
- [ ] Click "Create a resource" in Azure Portal
- [ ] Search for "Static Web App"
- [ ] Click "Create"

### Configuration
- [ ] **Subscription**: Selected
- [ ] **Resource Group**: Created new (e.g., `link-budget-resources`)
- [ ] **Name**: Entered (e.g., `link-budget-docs`)
- [ ] **Plan type**: Selected "Free"
- [ ] **Region**: Selected closest region
- [ ] **Source**: Selected "GitHub"
- [ ] **Signed in**: Authorized GitHub access
- [ ] **Organization**: Selected your GitHub username
- [ ] **Repository**: Selected "Link-Budget-Gemini"
- [ ] **Branch**: Selected "main"

### Build Details (Critical!)
- [ ] **Build Presets**: Selected "Custom"
- [ ] **App location**: Entered `/docs` (with leading slash)
- [ ] **Api location**: Left empty
- [ ] **Output location**: Left empty

### Deploy
- [ ] Clicked "Review + create"
- [ ] Validation passed
- [ ] Clicked "Create"
- [ ] Waited for "Deployment complete" message
- [ ] Clicked "Go to resource"

## Get Your URL
- [ ] Copied URL from Overview page (format: `https://[name].azurestaticapps.net`)
- [ ] My URL is: ___________________________________

## Verify Deployment
- [ ] Checked GitHub Action run status (should show "Succeeded")
- [ ] Verified GitHub secret exists: Settings → Secrets → Actions → `AZURE_STATIC_WEB_APPS_API_TOKEN`
- [ ] Opened URL in browser and saw documentation page

## Update Code
- [ ] Provided Azure URL to Claude
- [ ] Claude updated app.py with real URL
- [ ] Changes committed and pushed to GitHub

## Test Everything
- [ ] Documentation URL loads correctly
- [ ] Streamlit app "Documentation" button opens Azure-hosted docs
- [ ] Content displays properly
- [ ] Links work correctly

## Done! 🎉

Your documentation is now hosted on Azure with:
- ✅ Free SSL certificate
- ✅ Global CDN
- ✅ 100 GB bandwidth/month
- ✅ Automatic deployments on push to main branch
