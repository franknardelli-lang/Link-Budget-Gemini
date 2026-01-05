# Google Cloud Run Deployment Guide

This document details the step-by-step process used to configure this Streamlit application for automated deployment to Google Cloud Run using GitHub Actions.

## Prerequisites

*   A Google Cloud Platform (GCP) Account.
*   Access to this GitHub repository.
*   Google Cloud CLI (optional, for local testing) or access to the [Google Cloud Console](https://console.cloud.google.com/).

---

## Step 1: Google Cloud Project Setup

1.  **Create a Project:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Click the project dropdown (top left) > **New Project**.
    *   Name it (e.g., `link-budget-project`).
    *   **Note the Project ID** (e.g., `link-budget-project-12345`). You will need this for GitHub Secrets.

2.  **Enable Required APIs:**
    *   Navigate to **APIs & Services** > **Library**.
    *   Search for and **Enable** the following APIs:
        *   **Cloud Run Admin API** (To run the service)
        *   **Artifact Registry API** (To store Docker images)
        *   **Google Container Registry API** (Legacy support for `gcr.io` paths used in the workflow)

---

## Step 2: Service Account & Permissions

We create a specific "robot" account that GitHub uses to talk to Google Cloud securely.

1.  **Create Service Account:**
    *   Go to **IAM & Admin** > **Service Accounts**.
    *   Click **+ CREATE SERVICE ACCOUNT**.
    *   **Name:** `github-deployer` (or similar).
    *   Click **Create and Continue**.

2.  **Assign Roles (Crucial Step):**
    Grant the following **4 roles** to allow building, storing, and deploying containers:

    *   **Cloud Run Admin**: Allows deploying and updating the Cloud Run service.
    *   **Service Account User**: Allows the service account to act as the identity for the running service.
    *   **Artifact Registry Administrator**: Allows reading/writing to the image registry.
    *   **Artifact Registry Create-on-Push Writer**: Specifically allows creating *new* repositories automatically if they don't exist during the first push.

3.  **Generate Key:**
    *   Click on the newly created service account email in the list.
    *   Go to the **Keys** tab.
    *   Click **Add Key** > **Create new key**.
    *   Select **JSON** and download the file.
    *   *Security Warning:* Keep this file safe. It grants admin access to your project.

---

## Step 3: GitHub Repository Configuration

1.  Go to your GitHub Repository.
2.  Navigate to **Settings** > **Secrets and variables** > **Actions**.
3.  Click **New repository secret** to add the following:

    | Secret Name | Value |
    | :--- | :--- |
    | `GCP_PROJECT_ID` | The Project ID from Step 1 (e.g., `link-budget-project-12345`). |
    | `GCP_CREDENTIALS` | The **entire content** of the JSON key file downloaded in Step 2. |

---

## Step 4: Application Configuration

### 1. Dockerfile Update
Cloud Run requires applications to listen on the port defined by the `$PORT` environment variable (defaulting to 8080), whereas Streamlit defaults to 8501.

The `CMD` in the `Dockerfile` was updated to:
```dockerfile
CMD sh -c "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"
```
This allows the app to work locally (using 8501) and on Cloud Run (using the dynamic `$PORT`).

### 2. GitHub Actions Workflow
A workflow file was created at `.github/workflows/deploy-google.yml`. It performs the following steps on every push to `main`:
1.  Authenticates with Google using `GCP_CREDENTIALS`.
2.  Builds the Docker container.
3.  Pushes the container to Google Container Registry (`gcr.io`).
4.  Deploys the container to Cloud Run.

---

## Step 5: Deployment & Verification

### Triggering a Deploy
Simply push changes to the `main` branch:
```bash
git add .
git commit -m "Update app"
git push
```

### Verifying Success
1.  Go to the **Actions** tab in GitHub.
2.  Click the **Build and Deploy to Google Cloud Run** workflow.
3.  Wait for the status to turn **Green**.

### Finding the URL
1.  Go to the Google Cloud Console.
2.  Search for **Cloud Run**.
3.  Click on the service named `link-budget-app`.
4.  The live URL is displayed at the top of the dashboard (e.g., `https://link-budget-app-xyz.a.run.app`).

---

## Troubleshooting
*   **"Permission Denied" on push:** Ensure the Service Account has `Artifact Registry Create-on-Push Writer`.
*   **"API not enabled":** Check Step 1 and ensure both Cloud Run and Container Registry APIs are enabled.