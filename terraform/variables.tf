variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
  default     = "scoresage-rg"
}

variable "resource_group_location" {
  description = "The location of the resource group."
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "The name of the storage account."
  type        = string
  default     = "scoresagedata01"
}

variable "app_service_plan_name" {
  description = "The name of the app service plan."
  type        = string
  default     = "scoresage-asp"
}

variable "function_app_name" {
  description = "The name of the Linux Function App."
  type        = string
  default     = "example-linux-function-app"
}

variable "python_version" {
  description = "The version of Python to use in the Function App."
  type        = string
  default     = "3.9"
}

variable "storage_container_data_name" {
  description = "The name of the data storage container."
  type        = string
  default     = "data"
}

variable "storage_container_scripts_name" {
  description = "The name of the scripts storage container."
  type        = string
  default     = "scripts"
}

variable "storage_container_api_name" {
  description = "The name of the API storage container."
  type        = string
  default     = "api"
}
