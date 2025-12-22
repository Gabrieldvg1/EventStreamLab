resource "azurerm_eventhub_namespace" "eh_ns" {
  name                = "eventstreamlab-ns"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  capacity            = 1
}

resource "azurerm_eventhub" "eh" {
  name              = "demo-events"
  namespace_id      = azurerm_eventhub_namespace.eh_ns.id
  partition_count   = 1
  message_retention = 1
}

resource "azurerm_eventhub_authorization_rule" "eh_auth" {
  name                = "sendlisten"
  namespace_name      = azurerm_eventhub_namespace.eh_ns.name
  eventhub_name       = azurerm_eventhub.eh.name
  resource_group_name = azurerm_resource_group.rg.name

  listen = true
  send   = true
  manage = false
}