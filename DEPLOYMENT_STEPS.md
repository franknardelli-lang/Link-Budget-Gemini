# Azure Static Web Apps Deployment - Step by Step

Follow these steps exactly to deploy your documentation to Azure.

## Prerequisites Checklist

- [ ] Azure account (free tier is fine - sign up at https://azure.microsoft.com/free/)
- [ ] Logged into Azure Portal (https://portal.azure.com)
- [ ] This repository is on GitHub
- [ ] You have admin access to your GitHub repository

---

## Step 1: Create the Static Web App in Azure

### 1.1 Navigate to Create Resource

1. Open [Azure Portal](https://portal.azure.com)
2. Click the **"+ Create a resource"** button (top left, or in the center of the home page)
3. In the search box, type: **Static Web App**
4. Click on **"Static Web App"** from the results (published by Microsoft)
5. Click the blue **"Create"** button

### 1.2 Fill Out the Basics Tab

**Project Details:**
- **Subscription**: Select your subscription (likely "Free Trial" or "Pay-As-You-Go")
- **Resource Group**:
  - Click "Create new"
  - Name it: `link-budget-resources` (or any name you prefer)

**Static Web App Details:**
- **Name**: `link-budget-docs` (or your preferred name - must be globally unique)
  - This will become part of your URL: `https://link-budget-docs.azurestaticapps.net`
- **Plan type**: Select **"Free"** from the dropdown
- **Region**: Choose the closest region to you (e.g., "East US 2", "West Europe", etc.)

**Deployment Details:**
- **Source**: Select **"GitHub"**
- Click **"Sign in with GitHub"** if not already connected
- Authorize Azure to access your GitHub account (if prompted)

After GitHub connection:
- **Organization**: Select your GitHub username
- **Repository**: Select **"Link-Budget-Gemini"**
- **Branch**: Select **"main"**

### 1.3 Build Details (IMPORTANT!)

This section is critical - enter exactly as shown:

- **Build Presets**: Select **"Custom"** from dropdown
- **App location**: Enter **`/docs`** (must include the leading slash)
- **Api location**: Leave **empty** (just clear it if anything is there)
- **Output location**: Leave **empty**

### 1.4 Review and Create

1. Click **"Review + create"** button at the bottom
2. Wait for validation to complete (should show "Validation passed")
3. Review your settings:
   - Name: link-budget-docs
   - Plan: Free
   - App location: /docs
4. Click **"Create"**

### 1.5 Wait for Deployment

- You'll see "Deployment is in progress"
- This takes about 2-3 minutes
- Wait for "Your deployment is complete"
- Click **"Go to resource"**

---

## Step 2: Get Your URL

### 2.1 Find Your URL

1. You should now be on your Static Web App's **Overview** page
2. Look for the **"URL"** field near the top
3. It will look like: `https://[something].azurestaticapps.net`
   - Example: `https://nice-ocean-0a1b2c3d4.azurestaticapps.net`
4. **Copy this URL** - you'll need it in the next step

### 2.2 First Deployment Check

The first deployment happens automatically:

1. On the Overview page, find **"GitHub Action runs"** section
2. Click on the workflow run (should show "In progress" or "Succeeded")
3. This opens GitHub Actions - you'll see the build process
4. Wait for it to complete (green checkmark) - takes 1-2 minutes

---

## Step 3: Verify GitHub Secret

Azure should have automatically created a secret in your GitHub repository.

### 3.1 Check the Secret Exists

1. Go to your GitHub repository: https://github.com/franknardelli-lang/Link-Budget-Gemini
2. Click **"Settings"** tab (top right)
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**
4. You should see a secret named: **`AZURE_STATIC_WEB_APPS_API_TOKEN`**

✅ If you see it: Great! Continue to Step 4
❌ If you don't see it: Contact me and we'll troubleshoot

---

## Step 4: Update app.py with Your URL

Now we'll update the Streamlit app to point to your Azure-hosted documentation.

### 4.1 Get Your Exact URL

From Step 2.1, you should have copied your URL. It looks like:
```
https://[something].azurestaticapps.net
```

### 4.2 Tell Me Your URL

**Please provide your Azure Static Web Apps URL**, and I'll update the app.py file for you.

Example: "My URL is https://nice-ocean-0a1b2c3d4.azurestaticapps.net"

---

## Step 5: Test the Documentation

After I update the app.py:

### 5.1 Test the Documentation URL Directly

1. Open your Azure URL in a browser
2. You should see the **"Link Budget Calculator - Documentation"** page
3. Verify the content loads correctly

### 5.2 Test from Streamlit App

1. Run your Streamlit app locally or on Azure Container Apps
2. Click the **"📚 Documentation"** button
3. It should open your Azure-hosted docs in a new tab

---

## Troubleshooting

### Problem: GitHub Actions workflow fails

**Solution:**
1. Go to GitHub → Actions tab
2. Click on the failed workflow
3. Look at the error message
4. Common fixes:
   - Check that `app_location: "/docs"` in the workflow file
   - Verify `docs/index.html` exists in your repo
   - Make sure the secret exists (Step 3)

### Problem: URL shows "404 Not Found"

**Solution:**
1. Wait 2-3 minutes (initial deployment takes time)
2. Check GitHub Actions to ensure deployment succeeded
3. Check Azure Portal → Your Static Web App → "Deployment History"
4. Look for a successful deployment (green checkmark)

### Problem: Changes to docs don't update

**Solution:**
1. Changes only deploy when you push to the `main` branch
2. The workflow only triggers on changes to `docs/**` folder
3. Check GitHub Actions tab to see if a workflow ran
4. Clear your browser cache and try again

---

## What Happens Next?

Once you provide your URL:

1. ✅ I'll update app.py with your Azure URL
2. ✅ We'll commit the changes
3. ✅ Future updates to docs/ will auto-deploy via GitHub Actions
4. ✅ Your documentation will be on Azure's global CDN with free SSL

---

## Ready to Proceed?

👉 **Please tell me when you've completed Steps 1-3, and provide your Azure Static Web Apps URL from Step 2.1**

I'll then update app.py for you and we'll test everything together!
