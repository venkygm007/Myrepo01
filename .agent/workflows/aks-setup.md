---
description: Set up Azure Kubernetes Service (AKS) and deploy the application
---

# Azure AKS Setup Workflow

This workflow guides you through setting up an AKS cluster and deploying your application.

## Prerequisites
1.  **Azure CLI**: Installed and logged in (`az login`).
2.  **Kubectl**: Installed (`az aks install-cli`).

## Steps

### 1. Log in to Azure
```powershell
az login
```

### 2. Create a Resource Group
Replace `<RESOURCE_GROUP>` and `<LOCATION>` (e.g., `eastus`).
```powershell
az group create --name <RESOURCE_GROUP> --location <LOCATION>
```

### 3. Create an Azure Container Registry (ACR)
Replace `<ACR_NAME>` (must be unique).
```powershell
az acr create --resource-group <RESOURCE_GROUP> --name <ACR_NAME> --sku Basic
```

### 4. Build and Push Image to ACR
```powershell
az acr build --registry <ACR_NAME> --image flask-app:latest .
```

### 5. Create the AKS Cluster
This will link the ACR to your AKS cluster so it can pull images.
```powershell
az aks create --resource-group <RESOURCE_GROUP> --name <AKS_CLUSTER_NAME> --node-count 2 --generate-ssh-keys --attach-acr <ACR_NAME>
```

### 6. Get AKS Credentials
```powershell
az aks get-credentials --resource-group <RESOURCE_GROUP> --name <AKS_CLUSTER_NAME>
```

### 7. Deploy to AKS
Update `k8s/deployment.yaml` with your `<ACR_NAME>` before running this.
```powershell
kubectl apply -f k8s/deployment.yaml
```

### 8. Verify Deployment
```powershell
kubectl get pods
kubectl get service flask-app-service
```
Once the `EXTERNAL-IP` is assigned, you can visit it in your browser.
