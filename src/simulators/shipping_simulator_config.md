# Shipping Simulator Configuration - Updated for shipping_db

## Database Connection
- **EventHouse**: fabrikam_eventhouse  
- **Database**: shipping_db
- **Tables**: ShippingEvents, Carriers

## EventStream Configuration
When setting up EventStream, connect to:
- **Source**: Your Event Hub
- **Destination**: fabrikam_eventhouse.shipping_db.ShippingEvents
- **Mapping**: Use "ShippingMapping"

## Connection String Format
```
EventHouse URI: https://trd-hvsyx3h9ej7989gfw7.z6.kusto.fabric.microsoft.com
Database: shipping_db
```

## Quick Test Query
```kql
// Test data ingestion in shipping_db
ShippingEvents 
| take 10
| order by timestamp desc
```