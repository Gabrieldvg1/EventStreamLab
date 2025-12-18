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

  # Remote backend in Azure Storage for Terraform state.
  # The storage account & container are created by the
  # 'Terraform backend - Create Azure Storage' GitHub Action.
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
  # Use the Databricks workspace that Terraform creates in databricks.tf
  host = azurerm_databricks_workspace.dbw.workspace_url

  # Authentication is still provided via environment (for example, a PAT or AAD):
  # - DATABRICKS_TOKEN for a PAT, or Azure AD settings (see Databricks docs)
}