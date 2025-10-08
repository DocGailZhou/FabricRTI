# Manufacturing Simulator Configuration - Updated for manufacturing_db

## Database Connection
- **EventHouse**: fabrikam_eventhouse  
- **Database**: manufacturing_db
- **Tables**: ManufacturingTelemetry, Sites, Assets

## EventStream Configuration
When setting up EventStream, connect to:
- **Source**: Your Event Hub
- **Destination**: fabrikam_eventhouse.manufacturing_db.ManufacturingTelemetry
- **Mapping**: Use "ManufacturingMapping"

## Connection String Format
```
EventHouse URI: https://trd-hvsyx3h9ej7989gfw7.z6.kusto.fabric.microsoft.com
Database: manufacturing_db
```

## Quick Test Query
```kql
// Test data ingestion in manufacturing_db
ManufacturingTelemetry 
| take 10
| order by timestamp desc
```