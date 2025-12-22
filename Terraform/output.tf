output "eventhub_connection_string" {
  value     = azurerm_eventhub_authorization_rule.eh_auth.primary_connection_string
  sensitive = true
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.dbw.workspace_url
}