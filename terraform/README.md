# ScoreSage Terraform Setup

This README outlines the Terraform configuration and workflow created for the `ScoreSage` project. The infrastructure includes Azure resources such as a resource group, storage account, storage containers, app service plan, and a Linux Function App to host Python functions.

## Purpose
The purpose of this setup is to deploy infrastructure for the ScoreSage project, which involves:
- Storing and organizing data related to sports analytics.
- Hosting Python scripts and APIs in Azure Functions for data processing and prediction.
- Using Terraform for Infrastructure-as-Code (IaC) to ensure repeatable and version-controlled deployments.



## Files Created

### 1. **`main.tf`**
Defines all the core Azure resources:
- **Resource Group**: `scoresage-rg`
- **Storage Account**: `scoresagedata01` (Standard LRS)
- **Storage Containers**:
  - `data`
  - `scripts`
  - `api`
- **App Service Plan**: `scoresage-asp` (Dynamic SKU)
- **Linux Function App**: `example-linux-function-app`
  - Uses Python 3.9 runtime.
  - Includes system-assigned managed identity.
  - Configures `FUNCTIONS_WORKER_RUNTIME` and `WEBSITE_RUN_FROM_PACKAGE`.
- **Python Script Blob**: Deploys `main.py` to the `scripts` storage container.
- **Function App Function**: Sets up an HTTP-triggered Azure Function using the uploaded Python script.

### 2. **`outputs.tf`**
Captures and exports important resource details, such as:
- Resource Group name and location.
- Storage account name and ID.
- Names of the storage containers (`data`, `scripts`, `api`).
- App Service Plan name.
- Function App name and its system-assigned identity principal ID.
- URL of the uploaded Python script blob.
- Name of the deployed Azure Function.

### 3. **`variables.tf`**
Defines configurable variables with default values, including:
- Resource group name and location.
- Storage account name.
- App Service Plan name.
- Function App name.
- Python version.
- Names of the storage containers (`data`, `scripts`, `api`).



## Workflow Highlights

1. **Resource Group**:
   - Centralized group to manage all related resources.
   
2. **Storage Account and Containers**:
   - A storage account (`scoresagedata01`) with three containers:
     - `data`: Stores raw and processed data.
     - `scripts`: Stores Python scripts and utilities.
     - `api`: Stores backend API-related files.

3. **App Service Plan**:
   - Dynamic consumption-based plan (`Y1` SKU) to minimize costs.

4. **Linux Function App**:
   - Deployed with Python 3.9 runtime.
   - Managed identity enabled for secure authentication.
   - Application settings configured for Azure Functions runtime.

5. **Terraform State Management**:
   - Backend state stored in an Azure Blob container (`tfcontainer`) within a storage account.



## Next Steps

1. **GitHub Actions for CI/CD**:
   - Set up workflows to deploy updated Python scripts and APIs to the storage account and Function App.

2. **Data Pipeline Development**:
   - Add data collection, processing, and analytics pipelines to automate workflows.

3. **Model Integration**:
   - Deploy trained machine learning models in the `models` directory and integrate them into the API.

4. **Documentation Expansion**:
   - Extend this README with instructions for team members and contributors.



## How to Use

1. **Trigger the GitHub Action**:
   - A GitHub Actions workflow named **Terraform Deployment** is used to deploy the infrastructure.
   - Push your changes to the `main` branch or manually trigger the workflow via the **Actions** tab in your GitHub repository.

2. **Review Workflow Execution**:
   - Monitor the progress of the deployment in the **Actions** tab.
   - Ensure all steps complete successfully.

3. **Verify Deployment**:
   - Log in to the Azure Portal and confirm that the resources were created as expected.



## Notes
- Ensure the Azure CLI is installed and authenticated before running Terraform.
- All resource names are configurable via `variables.tf`.
- Make sure to securely manage sensitive information such as access keys and secrets.
