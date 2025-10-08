# RTI Solution - Three Database Testing Guide

## 🎯 **Quick Testing Strategy**

Test each database independently to validate connectivity faster:

### **Phase 1: Database Setup**
1. **Manufacturing Database**
   ```bash
   # Navigate to: fabrikam_eventhouse → manufacturing_db → Query
   # Run: manufacturing_db_tables.kql
   ```

2. **Shipping Database**
   ```bash
   # Navigate to: fabrikam_eventhouse → shipping_db → Query  
   # Run: shipping_db_tables.kql
   ```

3. **Clickstream Database**
   ```bash
   # Navigate to: fabrikam_eventhouse → clickstream_db → Query
   # Run: clickstream_db_tables.kql
   ```

### **Phase 2: EventStream Setup**
Set up one EventStream per database:

#### Manufacturing EventStream
- **Source**: Manufacturing Event Hub
- **Destination**: `fabrikam_eventhouse.manufacturing_db.ManufacturingTelemetry`
- **Data format**: JSON
- **Mapping**: ManufacturingMapping

#### Shipping EventStream  
- **Source**: Shipping Event Hub
- **Destination**: `fabrikam_eventhouse.shipping_db.ShippingEvents`
- **Data format**: JSON
- **Mapping**: ShippingMapping

#### Clickstream EventStream
- **Source**: Clickstream Event Hub  
- **Destination**: `fabrikam_eventhouse.clickstream_db.ClickstreamEvents`
- **Data format**: JSON
- **Mapping**: ClickstreamMapping

### **Phase 3: Simulator Testing**
Test each simulator independently:

1. **Start Manufacturing Simulator**
   - Check data arrives in `manufacturing_db.ManufacturingTelemetry`
   - Verify reference data in `Sites` and `Assets` tables

2. **Start Shipping Simulator**
   - Check data arrives in `shipping_db.ShippingEvents`
   - Verify reference data in `Carriers` table

3. **Start Clickstream Simulator**
   - Check data arrives in `clickstream_db.ClickstreamEvents`
   - Monitor anomaly detection in `AnomalyDetectionResults`

### **Phase 4: Dashboard Creation**
Create dashboard with three sections:

```
📊 RTI Executive Dashboard
├── 🏭 Manufacturing KPIs (manufacturing_db)
├── 🚚 Shipping Metrics (shipping_db)  
└── 🛒 E-commerce Analytics (clickstream_db)
```

## 🔍 **Quick Validation Queries**

### Manufacturing Database
```kql
// Check manufacturing data flow
ManufacturingTelemetry 
| summarize count() by bin(timestamp, 1m)
| order by timestamp desc
| take 10

// Check sites and assets
Sites | count
Assets | count
```

### Shipping Database  
```kql
// Check shipping data flow
ShippingEvents
| summarize count() by bin(timestamp, 1m) 
| order by timestamp desc
| take 10

// Check carriers
Carriers | count
```

### Clickstream Database
```kql
// Check clickstream data flow
ClickstreamEvents
| summarize count() by bin(timestamp, 1m)
| order by timestamp desc  
| take 10

// Check anomaly detection
AnomalyDetectionResults
| summarize count() by severity
```

## 🚀 **Benefits of This Approach**

✅ **Independent Testing**: Test each data stream separately
✅ **Faster Debugging**: Isolate connectivity issues per database
✅ **Team Ownership**: Each team manages their own database
✅ **Scalable**: Each database scales independently
✅ **Clear Separation**: No cross-database dependencies for basic functionality

## 📋 **Next Steps**

1. Run the three KQL scripts to create tables
2. Set up EventStreams (one per database)
3. Test simulators individually  
4. Create dashboard with separate sections
5. Add Activator rules per database as needed