# Microsoft Fabric RTI - Practical Implementation Examples

This document provides concrete code examples for implementing the RTI solution accelerator components.

## 1. EventHouse Setup and Data Ingestion

### A. Create EventHouse Database and Tables

```sql
-- Connect to your EventHouse via Fabric Portal or KQL Tools

-- 1. Create the main tables (run these commands in EventHouse Query Editor)
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

.create table ManufacturingTelemetry (
    event_type: string,
    timestamp: datetime,
    SiteId: string,
    City: string,
    AssetId: string,
    OperatorId: string,
    OperatorName: string,
    ProductId: string,
    SKU: string,
    BatchId: string,
    DefectProbability: real,
    Vibration: real,
    Temperature: real,
    Humidity: int
)

.create table AnomalyDetectionResults (
    timestamp: datetime,
    anomaly_type: string,
    source_table: string,
    entity_id: string,
    anomaly_score: real,
    baseline_value: real,
    current_value: real,
    severity: string,
    description: string,
    metadata: dynamic
)

-- 2. Create data mappings for EventStream ingestion
.create table ClickstreamEvents ingestion json mapping "ClickstreamMapping"
'['
'    {"column":"event_id","path":"$.event_id"},'
'    {"column":"timestamp","path":"$.timestamp"},'
'    {"column":"event_type","path":"$.event_type"},'
'    {"column":"user_id","path":"$.user_id"},'
'    {"column":"session_id","path":"$.session_id"},'
'    {"column":"sku","path":"$.sku"},'
'    {"column":"country","path":"$.country"},'
'    {"column":"country_code","path":"$.country_code"},'
'    {"column":"referral_source_type","path":"$.referral_source_type"},'
'    {"column":"referral_platform","path":"$.referral_platform"},'
'    {"column":"product_id","path":"$.product_id"},'
'    {"column":"spike_flag","path":"$.spike_flag"},'
'    {"column":"cart_spike_magnitude","path":"$.cart_spike_magnitude"},'
'    {"column":"client_info","path":"$.client_info"},'
'    {"column":"payload","path":"$.payload"}'
']'

.create table ManufacturingTelemetry ingestion json mapping "ManufacturingMapping"
'['
'    {"column":"event_type","path":"$.event_type"},'
'    {"column":"timestamp","path":"$.timestamp"},'
'    {"column":"SiteId","path":"$.SiteId"},'
'    {"column":"City","path":"$.City"},'
'    {"column":"AssetId","path":"$.AssetId"},'
'    {"column":"OperatorId","path":"$.OperatorId"},'
'    {"column":"OperatorName","path":"$.OperatorName"},'
'    {"column":"ProductId","path":"$.ProductId"},'
'    {"column":"SKU","path":"$.SKU"},'
'    {"column":"BatchId","path":"$.BatchId"},'
'    {"column":"DefectProbability","path":"$.DefectProbability"},'
'    {"column":"Vibration","path":"$.Vibration"},'
'    {"column":"Temperature","path":"$.Temperature"},'
'    {"column":"Humidity","path":"$.Humidity"}'
']'

-- 3. Enable streaming ingestion
.alter table ClickstreamEvents policy streamingingestion enable
.alter table ManufacturingTelemetry policy streamingingestion enable

-- 4. Set retention policies (adjust based on your needs)
.alter table ClickstreamEvents policy retention softdelete = 90d recoverability = disabled
.alter table ManufacturingTelemetry policy retention softdelete = 90d recoverability = disabled
```

### B. Sample KQL Queries for Testing

```sql
-- Test data ingestion
ClickstreamEvents
| count

ManufacturingTelemetry
| count

-- Check latest events
ClickstreamEvents
| top 10 by timestamp desc

-- Basic analytics queries
-- 1. Clickstream events by type over time
ClickstreamEvents
| where timestamp >= ago(1h)
| summarize count() by event_type, bin(timestamp, 5m)
| render timechart

-- 2. Manufacturing temperature trends
ManufacturingTelemetry
| where timestamp >= ago(1h)
| summarize avg(Temperature), max(Temperature) by bin(timestamp, 5m), AssetId
| render timechart

-- 3. Detect temperature anomalies
ManufacturingTelemetry
| where timestamp >= ago(1h)
| extend TempAnomaly = case(
    Temperature > 28.0, "High",
    Temperature < 21.0, "Low",
    "Normal"
)
| where TempAnomaly != "Normal"
| project timestamp, AssetId, Temperature, TempAnomaly
```

## 2. Python Analytics Implementation

### A. Setup Python Environment (requirements.txt)

```text
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.10.0
azure-kusto-data>=4.0.0
azure-identity>=1.14.0
azure-eventhub>=5.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

### B. Anomaly Detection Notebook Example

```python
# Cell 1: Import libraries and setup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.identity import DefaultAzureCredential
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
EVENTHOUSE_URI = "https://your-eventhouse.kusto.fabric.microsoft.com"
DATABASE_NAME = "YourRTIDatabase"

# Cell 2: Connect to EventHouse
def connect_to_eventhouse():
    """Connect to EventHouse using Azure AD authentication"""
    kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(EVENTHOUSE_URI)
    client = KustoClient(kcsb)
    return client

client = connect_to_eventhouse()
print("✅ Connected to EventHouse")

# Cell 3: Data retrieval function
def get_manufacturing_data(hours_back=24):
    """Retrieve manufacturing data from EventHouse"""
    query = f"""
    ManufacturingTelemetry
    | where timestamp >= ago({hours_back}h)
    | project timestamp, AssetId, Temperature, Vibration, DefectProbability
    | order by timestamp desc
    """
    
    try:
        response = client.execute(DATABASE_NAME, query)
        df = response.primary_results[0].to_dataframe()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

# Get data
manufacturing_df = get_manufacturing_data()
print(f"Retrieved {len(manufacturing_df)} records")
manufacturing_df.head()

# Cell 4: Statistical Anomaly Detection
class ManufacturingAnomalyDetector:
    def __init__(self, window_hours=2, threshold_std=2.5):
        self.window_hours = window_hours
        self.threshold_std = threshold_std
    
    def detect_temperature_anomalies(self, df):
        """Detect temperature anomalies using rolling statistics"""
        results = []
        
        for asset_id in df['AssetId'].unique():
            asset_data = df[df['AssetId'] == asset_id].copy()
            asset_data = asset_data.sort_values('timestamp')
            
            # Calculate rolling statistics
            window_size = f"{self.window_hours}H"
            asset_data['rolling_mean'] = asset_data['Temperature'].rolling(window_size).mean()
            asset_data['rolling_std'] = asset_data['Temperature'].rolling(window_size).std()
            
            # Calculate z-scores
            asset_data['z_score'] = np.abs(
                (asset_data['Temperature'] - asset_data['rolling_mean']) / asset_data['rolling_std']
            )
            
            # Identify anomalies
            anomalies = asset_data[asset_data['z_score'] > self.threshold_std]
            
            if not anomalies.empty:
                for _, row in anomalies.iterrows():
                    results.append({
                        'timestamp': row['timestamp'],
                        'asset_id': asset_id,
                        'anomaly_type': 'temperature',
                        'value': row['Temperature'],
                        'z_score': row['z_score'],
                        'severity': 'High' if row['z_score'] > 3.0 else 'Medium'
                    })
        
        return pd.DataFrame(results)
    
    def detect_vibration_anomalies(self, df):
        """Detect vibration anomalies using IsolationForest"""
        results = []
        
        for asset_id in df['AssetId'].unique():
            asset_data = df[df['AssetId'] == asset_id].copy()
            
            if len(asset_data) < 10:  # Need minimum data points
                continue
            
            # Prepare features
            features = asset_data[['Vibration', 'Temperature']].values
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Train isolation forest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(features_scaled)
            anomaly_scores = iso_forest.decision_function(features_scaled)
            
            # Get anomalies
            anomaly_indices = np.where(anomaly_labels == -1)[0]
            
            for idx in anomaly_indices:
                results.append({
                    'timestamp': asset_data.iloc[idx]['timestamp'],
                    'asset_id': asset_id,
                    'anomaly_type': 'vibration',
                    'value': asset_data.iloc[idx]['Vibration'],
                    'anomaly_score': anomaly_scores[idx],
                    'severity': 'High' if anomaly_scores[idx] < -0.5 else 'Medium'
                })
        
        return pd.DataFrame(results)

# Cell 5: Run anomaly detection
detector = ManufacturingAnomalyDetector()

# Detect temperature anomalies
temp_anomalies = detector.detect_temperature_anomalies(manufacturing_df)
print(f"Found {len(temp_anomalies)} temperature anomalies")

# Detect vibration anomalies
vibration_anomalies = detector.detect_vibration_anomalies(manufacturing_df)
print(f"Found {len(vibration_anomalies)} vibration anomalies")

# Combine results
all_anomalies = pd.concat([temp_anomalies, vibration_anomalies], ignore_index=True)
print(f"Total anomalies detected: {len(all_anomalies)}")

# Cell 6: Visualize anomalies
if not all_anomalies.empty:
    plt.figure(figsize=(15, 8))
    
    # Plot 1: Anomalies by type over time
    plt.subplot(2, 2, 1)
    anomaly_counts = all_anomalies.groupby([
        pd.Grouper(key='timestamp', freq='1H'), 
        'anomaly_type'
    ]).size().unstack(fill_value=0)
    anomaly_counts.plot(kind='bar', stacked=True)
    plt.title('Anomalies by Type Over Time')
    plt.xticks(rotation=45)
    
    # Plot 2: Severity distribution
    plt.subplot(2, 2, 2)
    all_anomalies['severity'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Anomaly Severity Distribution')
    
    # Plot 3: Anomalies by asset
    plt.subplot(2, 2, 3)
    asset_anomalies = all_anomalies['asset_id'].value_counts().head(10)
    asset_anomalies.plot(kind='bar')
    plt.title('Top 10 Assets with Most Anomalies')
    plt.xticks(rotation=45)
    
    # Plot 4: Temperature trend with anomalies
    plt.subplot(2, 2, 4)
    sample_asset = manufacturing_df['AssetId'].iloc[0]
    asset_data = manufacturing_df[manufacturing_df['AssetId'] == sample_asset]
    asset_anomalies = temp_anomalies[temp_anomalies['asset_id'] == sample_asset]
    
    plt.plot(asset_data['timestamp'], asset_data['Temperature'], 'b-', alpha=0.7, label='Temperature')
    if not asset_anomalies.empty:
        plt.scatter(asset_anomalies['timestamp'], asset_anomalies['value'], 
                   color='red', s=50, label='Anomalies', zorder=5)
    plt.title(f'Temperature Trend for {sample_asset}')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Cell 7: Insert anomalies back into EventHouse
def insert_anomalies_to_eventhouse(anomalies_df):
    """Insert anomaly results back into EventHouse"""
    if anomalies_df.empty:
        print("No anomalies to insert")
        return
    
    # Prepare data for insertion
    records = []
    for _, row in anomalies_df.iterrows():
        record = {
            'timestamp': row['timestamp'].isoformat(),
            'anomaly_type': row['anomaly_type'],
            'source_table': 'ManufacturingTelemetry',
            'entity_id': row['asset_id'],
            'anomaly_score': float(row.get('z_score', row.get('anomaly_score', 0))),
            'baseline_value': 0.0,  # Would calculate this in production
            'current_value': float(row['value']),
            'severity': row['severity'],
            'description': f"{row['anomaly_type']} anomaly detected for asset {row['asset_id']}",
            'metadata': json.dumps({
                'detection_method': 'statistical' if 'z_score' in row else 'isolation_forest',
                'threshold': 2.5
            })
        }
        records.append(record)
    
    # Create batch insert command
    records_json = json.dumps(records)
    
    insert_command = f"""
    .ingest inline into table AnomalyDetectionResults <|
    {records_json}
    """
    
    try:
        client.execute(DATABASE_NAME, insert_command)
        print(f"✅ Inserted {len(records)} anomaly records into EventHouse")
    except Exception as e:
        print(f"❌ Error inserting anomalies: {e}")

# Insert anomalies
insert_anomalies_to_eventhouse(all_anomalies)

# Cell 8: Create summary report
def create_anomaly_report():
    """Create a summary report of detected anomalies"""
    if all_anomalies.empty:
        return "No anomalies detected in the analysis period."
    
    report = f"""
    🔍 ANOMALY DETECTION REPORT
    ═══════════════════════════════════════
    
    Analysis Period: {manufacturing_df['timestamp'].min()} to {manufacturing_df['timestamp'].max()}
    Total Records Analyzed: {len(manufacturing_df):,}
    
    📊 SUMMARY STATISTICS:
    ─────────────────────────────────────────
    • Total Anomalies Detected: {len(all_anomalies)}
    • Temperature Anomalies: {len(temp_anomalies)}
    • Vibration Anomalies: {len(vibration_anomalies)}
    
    🎯 SEVERITY BREAKDOWN:
    ─────────────────────────────────────────
    """
    
    for severity in all_anomalies['severity'].value_counts().index:
        count = all_anomalies['severity'].value_counts()[severity]
        percentage = (count / len(all_anomalies)) * 100
        report += f"• {severity}: {count} ({percentage:.1f}%)\n    "
    
    report += f"""
    
    🏭 TOP AFFECTED ASSETS:
    ─────────────────────────────────────────
    """
    
    top_assets = all_anomalies['asset_id'].value_counts().head(5)
    for asset, count in top_assets.items():
        report += f"• {asset}: {count} anomalies\n    "
    
    report += f"""
    
    ⚠️  RECOMMENDATIONS:
    ─────────────────────────────────────────
    • Investigate assets with high anomaly counts
    • Review maintenance schedules for affected equipment
    • Consider adjusting operational parameters
    • Set up real-time alerts for critical thresholds
    
    """
    
    return report

# Generate and display report
report = create_anomaly_report()
print(report)
```

## 3. Activator Configuration Examples

### Temperature Alert Rule
```javascript
// Condition KQL Query:
ManufacturingTelemetry
| where timestamp >= ago(5m)
| where Temperature > 28.0
| summarize AvgTemp = avg(Temperature), MaxTemp = max(Temperature) by AssetId
| where MaxTemp > 29.0

// Action: Email Alert
{
  "actionType": "email",
  "recipients": ["operations@company.com"],
  "subject": "🚨 Equipment Overheating - Asset {AssetId}",
  "body": "Asset {AssetId} temperature: {MaxTemp}°C (Avg: {AvgTemp}°C)"
}
```

### Clickstream Anomaly Rule  
```javascript
// Condition KQL Query:
ClickstreamEvents
| where timestamp >= ago(10m)
| where spike_flag == true
| summarize SpikeCount = count() by product_id
| where SpikeCount > 20

// Action: Teams Notification
{
  "actionType": "teams",
  "webhook": "https://outlook.office.com/webhook/...",
  "message": "🔥 Product spike detected: {product_id} ({SpikeCount} events)"
}
```

## 4. RTI Dashboard Queries

### Operations Dashboard
```sql
-- Real-time system health
union 
(ManufacturingTelemetry | where timestamp >= ago(5m) | summarize Type="Manufacturing", Count=count()),
(ClickstreamEvents | where timestamp >= ago(5m) | summarize Type="Clickstream", Count=count())
| render piechart

-- Live alerts
AnomalyDetectionResults
| where timestamp >= ago(1h)
| summarize count() by severity, bin(timestamp, 5m)
| render columnchart
```

### Business Dashboard  
```sql
-- Conversion funnel (real-time)
ClickstreamEvents
| where timestamp >= ago(1h)
| summarize count() by event_type
| order by count_ desc
| render funnel
```

This implementation guide provides you with:

1. **Exact KQL commands** to set up EventHouse tables
2. **Complete Python code** for anomaly detection with ML models
3. **Specific Activator rule examples** with actions  
4. **Ready-to-use dashboard queries** for monitoring

All the code aligns with the sample data from the RTI-Hackathon simulators and can be used immediately in your Fabric environment.