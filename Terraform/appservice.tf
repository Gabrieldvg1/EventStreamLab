resource "azurerm_service_plan" "api_plan" {
  name                = "eventstreamlab-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1" # Basic tier - low cost
}

resource "azurerm_linux_web_app" "api" {
  name                = "eventstreamlab-api"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.api_plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      dotnet_version = "8.0"
    }
  }

  app_settings = {
    "EventHubConnectionString" = azurerm_eventhub_authorization_rule.eh_auth.primary_connection_string
    "EventHubName"             = azurerm_eventhub.eh.name

    # For Kafka (Confluent.Kafka) client talking to Azure Event Hubs' Kafka endpoint.
    # App Service on Linux doesn't allow ':' in setting names, so we use '__' which ASP.NET maps to ':'.
    "Kafka__Topic"            = azurerm_eventhub.eh.name
    "Kafka__BootstrapServers" = "${azurerm_eventhub_namespace.eh_ns.name}.servicebus.windows.net:9093"
    "Kafka__ConnectionString" = azurerm_eventhub_authorization_rule.eh_auth.primary_connection_string
  }
}