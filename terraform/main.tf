resource "azurerm_resource_group" "scoresage_rg" {
  name     = "scoresage-rg"
  location = "East US"
}

resource "azurerm_storage_account" "scoresage_sa01" {
  name                     = "scoresagedata01"
  resource_group_name      = azurerm_resource_group.scoresage_rg.name
  location                 = azurerm_resource_group.scoresage_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.scoresage_sa01.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "scripts" {
  name                  = "scripts"
  storage_account_name  = azurerm_storage_account.scoresage_sa01.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "api" {
  name                  = "api"
  storage_account_name  = azurerm_storage_account.scoresage_sa01.name
  container_access_type = "private"
}

resource "azurerm_service_plan" "scoresage_asp" {
  name                = "scoresage-asp"
  location            = azurerm_resource_group.scoresage_rg.location
  resource_group_name = azurerm_resource_group.scoresage_rg.name
  os_type             = "Linux"  # Specify the operating system type
  sku_name            = "P1v2"     # Specify the SKU name
}

resource "azurerm_linux_function_app" "example" {
  name                       = "example-linux-function-app"
  resource_group_name        = azurerm_resource_group.scoresage_rg.name
  location                   = azurerm_resource_group.scoresage_rg.location
  service_plan_id            = azurerm_service_plan.scoresage_asp.id
  storage_account_name       = azurerm_storage_account.scoresage_sa01.name
  storage_account_access_key = azurerm_storage_account.scoresage_sa01.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    AzureWebJobsStorage      = azurerm_storage_account.scoresage_sa01.primary_connection_string
    WEBSITE_RUN_FROM_PACKAGE = "1"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_function_app_function" "example" {
  name            = "example-function-app-function"
  function_app_id = azurerm_linux_function_app.example.id
  language        = "Python"

  # No file block yet, as main.py is not available
  config_json = jsonencode({
    "bindings" = [
      {
        "authLevel" = "function",
        "direction" = "in",
        "methods"   = ["get", "post"],
        "name"      = "req",
        "type"      = "httpTrigger"
      },
      {
        "direction" = "out",
        "name"      = "$return",
        "type"      = "http"
      }
    ]
  })
}
