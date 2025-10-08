# Clickstream Simulator Configuration - Updated for clickstream_db

## Database Connection
- **EventHouse**: fabrikam_eventhouse  
- **Database**: clickstream_db
- **Tables**: ClickstreamEvents, AnomalyDetectionResults

## EventStream Configuration
When setting up EventStream, connect to:
- **Source**: Your Event Hub
- **Destination**: fabrikam_eventhouse.clickstream_db.ClickstreamEvents
- **Mapping**: Use "ClickstreamMapping"

## Connection String Format
```
EventHouse URI: https://trd-hvsyx3h9ej7989gfw7.z6.kusto.fabric.microsoft.com
Database: clickstream_db
```

## Quick Test Query
```kql
// Test data ingestion in clickstream_db
ClickstreamEvents 
| take 10
| order by timestamp desc
```