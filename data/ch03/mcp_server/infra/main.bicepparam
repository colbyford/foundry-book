using './main.bicep'

param appName = readEnvironmentVariable('APP_NAME')

param cosmos_uri = readEnvironmentVariable('COSMOS_URI')
param cosmos_key = readEnvironmentVariable('COSMOS_KEY')
param cosmos_database = readEnvironmentVariable('COSMOS_DATABASE', 'RealEstateCatalog')
param cosmos_container = readEnvironmentVariable('COSMOS_CONTAINER', 'Properties')
