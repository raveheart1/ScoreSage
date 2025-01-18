output "resource_group_name" {
  description = "The name of the resource group."
  value       = azurerm_resource_group.scoresage_rg.name
}

output "resource_group_location" {
  description = "The location of the resource group."
  value       = azurerm_resource_group.scoresage_rg.location
}

output "storage_account_name" {
  description = "The name of the storage account."
  value       = azurerm_storage_account.scoresage_sa01.name
}

output "storage_account_id" {
  description = "The ID of the storage account."
  value       = azurerm_storage_account.scoresage_sa01.id
}

output "storage_container_data" {
  description = "The name of the data storage container."
  value       = azurerm_storage_container.data.name
}

output "storage_container_scripts" {
  description = "The name of the scripts storage container."
  value       = azurerm_storage_container.scripts.name
}

output "storage_container_api" {
  description = "The name of the API storage container."
  value       = azurerm_storage_container.api.name
}

output "app_service_plan_name" {
  description = "The name of the app service plan."
  value       = azurerm_service_plan.scoresage_asp.name
}

output "function_app_name" {
  description = "The name of the Linux Function App."
  value       = azurerm_linux_function_app.example.name
}

output "function_app_identity_principal_id" {
  description = "The Principal ID of the Function App's system-assigned identity."
  value       = azurerm_linux_function_app.example.identity[0].principal_id
}

output "function_app_function_name" {
  description = "The name of the deployed function in the Function App."
  value       = azurerm_function_app_function.example.name
}
