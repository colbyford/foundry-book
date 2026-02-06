param location string = resourceGroup().location
param appName string
param pythonVersion string = '3.11'

param cosmos_uri string
param cosmos_key string
param cosmos_database string
param cosmos_container string


resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      appCommandLine: 'python app.py'
      appSettings: [
        {
          name: 'PORT'
          value: '8000'
        }
        {
          name: 'COSMOS_URI'
          value: cosmos_uri
        }
        {
          name: 'COSMOS_KEY'
          value: cosmos_key
        }
        {
          name: 'COSMOS_DATABASE'
          value: cosmos_database
        }
        {
          name: 'COSMOS_CONTAINER'
          value: cosmos_container
        }
      ]
    }
    httpsOnly: true
  }
}

output endpoint string = 'https://${webApp.properties.defaultHostName}'
