resource "azurerm_databricks_workspace" "dbw" {
  name                = "eventstreamlab-dbw"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "trial"
}