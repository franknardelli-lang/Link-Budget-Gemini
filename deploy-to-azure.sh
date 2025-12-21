#!/bin/bash

# Configuration - CUSTOMIZE THESE VALUES
DOCKER_USERNAME="franknardelli"  # Your Docker Hub username
IMAGE_NAME="link-budget-calculator"  # Name for your Docker image
RESOURCE_GROUP="link-budget-rg"  # Azure resource group name
LOCATION="eastus"  # Azure region
CONTAINER_APP_NAME="link-budget-app"  # Name for your container app
CONTAINER_ENV_NAME="antenna-env"  # Container Apps environment name (using existing)
CONTAINER_ENV_RESOURCE_GROUP="antenna-tools-rg"  # Resource group where environment exists
TAG="latest"  # Docker image tag

# Derived variables
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "========================================"
echo "Azure Container Apps Deployment Script"
echo "========================================"
echo "Image: ${FULL_IMAGE_NAME}"
echo "Resource Group: ${RESOURCE_GROUP}"
echo "Container App: ${CONTAINER_APP_NAME}"
echo "Location: ${LOCATION}"
echo "========================================"

# Check if logged into Azure
echo ""
echo "Checking Azure CLI authentication..."
az account show &> /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Not logged into Azure CLI"
    echo "Please run: az login"
    exit 1
fi
echo "✓ Azure CLI authenticated"

# Check if logged into Docker Hub
echo ""
echo "Checking Docker Hub authentication..."
docker info | grep -q "Username"
if [ $? -ne 0 ]; then
    echo "WARNING: Not logged into Docker Hub"
    echo "Please run: docker login"
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Docker Hub authenticated"
fi

# Build Docker image
echo ""
echo "Building Docker image..."
docker build -t ${FULL_IMAGE_NAME} .
if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi
echo "✓ Docker image built successfully"

# Push to Docker Hub
echo ""
echo "Pushing image to Docker Hub..."
docker push ${FULL_IMAGE_NAME}
if [ $? -ne 0 ]; then
    echo "ERROR: Docker push failed"
    echo "Make sure you're logged in with: docker login"
    exit 1
fi
echo "✓ Image pushed to Docker Hub"

# Create resource group if it doesn't exist
echo ""
echo "Checking resource group..."
az group show --name ${RESOURCE_GROUP} &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating resource group: ${RESOURCE_GROUP}"
    az group create --name ${RESOURCE_GROUP} --location ${LOCATION}
    echo "✓ Resource group created"
else
    echo "✓ Resource group already exists"
fi

# Check if Container Apps environment exists (in its resource group)
echo ""
echo "Checking Container Apps environment..."
az containerapp env show --name ${CONTAINER_ENV_NAME} --resource-group ${CONTAINER_ENV_RESOURCE_GROUP} &> /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Container Apps environment '${CONTAINER_ENV_NAME}' not found in resource group '${CONTAINER_ENV_RESOURCE_GROUP}'"
    echo "Please verify the environment name and resource group"
    exit 1
else
    echo "✓ Using existing Container Apps environment: ${CONTAINER_ENV_NAME}"
fi

# Check if container app exists
echo ""
echo "Checking if container app exists..."
az containerapp show --name ${CONTAINER_APP_NAME} --resource-group ${RESOURCE_GROUP} &> /dev/null

if [ $? -eq 0 ]; then
    # Update existing container app
    echo "Updating existing container app: ${CONTAINER_APP_NAME}"
    az containerapp update \
        --name ${CONTAINER_APP_NAME} \
        --resource-group ${RESOURCE_GROUP} \
        --image ${FULL_IMAGE_NAME}
    echo "✓ Container app updated"
else
    # Create new container app
    echo "Creating new container app: ${CONTAINER_APP_NAME}"
    # Get the environment resource ID since it's in a different resource group
    ENV_ID=$(az containerapp env show \
        --name ${CONTAINER_ENV_NAME} \
        --resource-group ${CONTAINER_ENV_RESOURCE_GROUP} \
        --query id \
        --output tsv)

    az containerapp create \
        --name ${CONTAINER_APP_NAME} \
        --resource-group ${RESOURCE_GROUP} \
        --environment ${ENV_ID} \
        --image ${FULL_IMAGE_NAME} \
        --target-port 8501 \
        --ingress external \
        --cpu 0.5 \
        --memory 1.0Gi \
        --min-replicas 0 \
        --max-replicas 2
    echo "✓ Container app created"
fi

# Get the application URL
echo ""
echo "Getting application URL..."
FQDN=$(az containerapp show \
    --name ${CONTAINER_APP_NAME} \
    --resource-group ${RESOURCE_GROUP} \
    --query properties.configuration.ingress.fqdn \
    --output tsv)

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo "Your Link Budget Calculator is available at:"
echo "https://${FQDN}"
echo "========================================"
