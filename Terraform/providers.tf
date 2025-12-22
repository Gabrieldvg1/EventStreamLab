terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "eventstreamlab-tfstate-rg"
    storage_account_name = "eventstreamlabtfstate"
    container_name       = "tfstate"
    key                  = "eventstreamlab.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "21327150-ec4c-4db3-ae03-7d5cef898b9c"
}

provider "databricks" {
  host = azurerm_databricks_workspace.dbw.workspace_url
}