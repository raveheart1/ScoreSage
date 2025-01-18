terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.90.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "1.12.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.47.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "gmcw"
    storage_account_name = "gmcwtfsa"
    container_name       = "tfcontainer"
    key                  = "state.tfstate"
  }
}

# Provider configuration for Azure
provider "azurerm" {
  features {}
}
