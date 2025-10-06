# Microsoft Fabric RTI Solution Accelerator - Architecture Design

## Executive Summary

This document outlines the architecture design for a Microsoft Fabric Real-Time Intelligence (RTI) solution accelerator that builds upon the existing [Unified Data Foundation with Fabric](https://github.com/microsoft/unified-data-foundation-with-fabric-solution-accelerator) solution. The new accelerator focuses on real-time data processing, anomaly detection, and intelligent alerting using Microsoft Fabric's RTI capabilities including EventStream, EventHouse, Activator, and RTI dashboards.

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Data Sources & Simulation Layer                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ ┌─────────────┐  │
│  │ Clickstream     │  │ Manufacturing   │  │ IoT Sensors     │ │ ThingSpeak  │  │
│  │ Simulator       │  │ Telemetry       │  │ (Custom)        │ │ Public Data │  │
│  │ (Modified)      │  │ Simulator       │  │                 │ │             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Real-Time Data Ingestion Layer                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                              ┌─────────────────┐                               │
│                              │   EventStream   │                               │
│                              │  ┌───────────┐  │                               │
│                              │  │Custom     │  │                               │
│                              │  │Endpoints  │  │                               │
│                              │  └───────────┘  │                               │
│                              │  ┌───────────┐  │                               │
│                              │  │Data       │  │                               │
│                              │  │Transform  │  │                               │
│                              │  └───────────┘  │                               │
│                              └─────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Real-Time Analytics & Storage Layer                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐     │
│  │           EventHouse            │    │          Lakehouse              │     │
│  │                                 │    │                                 │     │
│  │  ┌─────────────────────────────┐│    │  ┌─────────────────────────────┐│     │
│  │  │ Real-time KQL Database      ││    │  │ Historical Data Storage     ││     │
│  │  │                             ││    │  │                             ││     │
│  │  │ • Clickstream Events        ││    │  │ • Customer Master Data      ││     │
│  │  │ • Manufacturing Telemetry   ││    │  │ • Product Master Data       ││     │
│  │  │ • IoT Sensor Data           ││    │  │ • Sales Historical Data     ││     │
│  │  │ • Anomaly Detection Results ││    │  │ • Finance Data              ││     │
│  │  └─────────────────────────────┘│    │  └─────────────────────────────┘│     │
│  └─────────────────────────────────┘    └─────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     Real-Time Intelligence & Analytics Layer                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │   Activator     │  │ KQL Queries     │  │        Python Analytics        │  │
│  │                 │  │                 │  │                                 │  │
│  │ • Alert Rules   │  │ • Anomaly       │  │ • Advanced ML Models           │  │
│  │ • Trigger       │  │   Detection     │  │ • Custom Analytics Functions   │  │
│  │   Actions       │  │ • Real-time     │  │ • Statistical Analysis         │  │
│  │ • Notifications │  │   Aggregations  │  │ • Predictive Analytics         │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Visualization & Action Layer                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ RTI Dashboards  │  │ Power BI        │  │        Action Systems           │  │
│  │                 │  │ Real-time       │  │                                 │  │
│  │ • Real-time     │  │ Reports         │  │ • Email Notifications          │  │
│  │   Monitoring    │  │                 │  │ • Teams Alerts                 │  │
│  │ • KQL-based     │  │ • Executive     │  │ • Custom Webhooks              │  │
│  │   Charts        │  │   Dashboards    │  │ • Business Process Triggers    │  │
│  │ • Drill-down    │  │ • Historical    │  │                                 │  │
│  │   Capabilities  │  │   Analysis      │  │                                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Sources & Simulation Layer

#### 1.1 Clickstream Simulator (Enhanced)
- **Base**: Modified version of [RTI-Hackathon Clickstream Simulator](https://github.com/L400-RTI/RTI-Hackathon/blob/main/Data%20Simulators/Clickstream%20Simulator.ipynb)
- **Enhancements**:
  - Increased anomaly frequency (20% vs 5%) for faster testing
  - Configurable spike patterns
  - Integration with existing customer/product domains
  - Support for A/B testing scenarios

#### 1.2 Manufacturing Telemetry Simulator
- **Base**: RTI-Hackathon Manufacturing Simulator
- **Real-time Events**:
  - Production line metrics (temperature, vibration, defect probability)
  - Equipment status and alerts
  - Quality control measurements
  - Operator performance metrics

#### 1.3 IoT Sensor Simulation
- **Custom Sensors**:
  - Environmental monitoring (temperature, humidity, air quality)
  - Energy consumption tracking  
  - Security and access control events
  - Supply chain tracking

#### 1.4 Public Data Integration
- **ThingSpeak Channels**: Integration with public IoT data channels for enrichment
- **Weather Data**: Real-time weather information for correlation analysis
- **Market Data**: Economic indicators and market trends

### 2. Real-Time Data Ingestion Layer

#### 2.1 EventStream Configuration
- **Multiple Custom Endpoints**: Separate endpoints for different data types
- **Data Transformation**: 
  - Schema validation and normalization
  - Data enrichment with master data lookups
  - Real-time aggregations and windowing
- **Routing Logic**: Intelligent routing based on event types and priority levels

### 3. Real-Time Analytics & Storage Layer

#### 3.1 EventHouse (KQL Database) - DETAILED EXPLANATION

**What is EventHouse?**
- EventHouse is Microsoft Fabric's real-time analytics service built on Azure Data Explorer (Kusto)
- It's a KQL (Kusto Query Language) database optimized for time-series and streaming data
- Unlike traditional SQL databases, it's columnar and designed for fast ingestion and analytical queries

**Do you need to create tables?**
- YES, you must create tables with defined schemas (like SQL DDL)
- Tables are automatically partitioned by time and optimized for streaming ingestion
- Data is automatically indexed and compressed

**Database Design (Aligned with Sample Data)**:

Based on the RTI-Hackathon simulators, here are the exact table schemas:

```sql
-- 1. Clickstream Events Table (matches Clickstream Simulator output)
.create table ClickstreamEvents (
    event_id: string,                    -- UUID from simulator
    timestamp: datetime,                 -- ISO format from simulator
    event_type: string,                  -- page_view, product_click, add_to_cart, etc.
    user_id: string,                     -- UUID from simulator
    session_id: string,                  -- UUID from simulator
    sku: string,                         -- SKU4000-SKU4019 from simulator
    country: string,                     -- Germany, United States, etc.
    country_code: string,                -- DE, US, UK, etc.
    referral_source_type: string,        -- search, social, direct, affiliate
    referral_platform: string,           -- Google, Facebook, etc.
    product_id: string,                  -- PROD4000-PROD4019 from simulator
    spike_flag: bool,                    -- Anomaly indicator from simulator
    cart_spike_magnitude: int,           -- 0-100 from simulator
    client_info: dynamic,                -- Browser, OS, Device info
    payload: dynamic                     -- Event-specific data (price, cart_items, etc.)
)

-- 2. Manufacturing Telemetry Table (matches Manufacturing Simulator output)
.create table ManufacturingTelemetry (
    event_type: string,                  -- Always "production" from simulator
    timestamp: datetime,                 -- ISO format with Z suffix
    SiteId: string,                      -- SITE1000-SITE1009 from simulator
    City: string,                        -- Berlin, Shanghai, Amsterdam, etc.
    AssetId: string,                     -- ASSET2000-ASSET2049 from simulator
    OperatorId: string,                  -- OP3001-OP3030 from simulator
    OperatorName: string,                -- Generated names from Faker
    ProductId: string,                   -- PROD4000-PROD4019 from simulator
    SKU: string,                         -- SKU4000-SKU4019 from simulator
    BatchId: string,                     -- UUID from simulator
    DefectProbability: real,             -- 0.0-0.2 from simulator
    Vibration: real,                     -- 0.5-1.5 from simulator
    Temperature: real,                   -- 20.0-30.0 from simulator
    Humidity: int                        -- 30-80 from simulator
)

-- 3. Static Reference Tables (Generated by simulators into Lakehouse)
.create table Sites (
    SiteId: string,
    City: string,
    Country: string,
    Region: string,
    Latitude: real,
    Longitude: real
)

.create table Assets (
    AssetId: string,
    AssetName: string,
    AssetType: string,
    SiteId: string,
    InstallationDate: datetime,
    MaintenanceSchedule: string
)

.create table Operators (
    OperatorId: string,
    Name: string,
    Shift: string,
    Department: string,
    HireDate: datetime,
    CertificationLevel: string
)

-- 4. Anomaly Detection Results Table
.create table AnomalyDetectionResults (
    timestamp: datetime,
    anomaly_type: string,               -- clickstream_spike, manufacturing_outlier, etc.
    source_table: string,               -- ClickstreamEvents, ManufacturingTelemetry
    entity_id: string,                  -- ProductId, AssetId, etc.
    anomaly_score: real,                -- Calculated anomaly score
    baseline_value: real,               -- Historical baseline
    current_value: real,                -- Current observed value
    severity: string,                   -- Low, Medium, High, Critical
    description: string,                -- Human readable description
    metadata: dynamic                   -- Additional context
)
```

**Data Ingestion Policies**:
```sql
-- Set up streaming ingestion for real-time data
.create table ClickstreamEvents ingestion json mapping "ClickstreamMapping"
```[
    {"column":"event_id","path":"$.event_id"},
    {"column":"timestamp","path":"$.timestamp"},
    {"column":"event_type","path":"$.event_type"},
    {"column":"user_id","path":"$.user_id"},
    {"column":"session_id","path":"$.session_id"},
    {"column":"sku","path":"$.sku"},
    {"column":"country","path":"$.country"},
    {"column":"country_code","path":"$.country_code"},
    {"column":"referral_source_type","path":"$.referral_source_type"},
    {"column":"referral_platform","path":"$.referral_platform"},
    {"column":"product_id","path":"$.product_id"},
    {"column":"spike_flag","path":"$.spike_flag"},
    {"column":"cart_spike_magnitude","path":"$.cart_spike_magnitude"},
    {"column":"client_info","path":"$.client_info"},
    {"column":"payload","path":"$.payload"}
]```

-- Enable streaming ingestion
.alter table ClickstreamEvents policy streamingingestion enable
```

#### 3.2 Integration with Existing Medallion Architecture
- **Bronze Layer**: Raw real-time data ingestion
- **Silver Layer**: Validated and enriched real-time data
- **Gold Layer**: Enriched with historical context from existing domains
- **Data Shortcuts**: Seamless integration with existing customer, product, sales, and finance data

### 4. Real-Time Intelligence & Analytics Layer

#### 4.1 KQL-Based Analytics
```sql
-- Example: Real-time Anomaly Detection
let baselineWindow = 7d;
let detectionWindow = 5m;
let threshold = 3.0;

ClickstreamEvents
| where Timestamp >= ago(detectionWindow)
| summarize CurrentRate = count() by bin(Timestamp, 1m), ProductId
| join kind=inner (
    ClickstreamEvents
    | where Timestamp between (ago(baselineWindow + detectionWindow) .. ago(detectionWindow))
    | summarize HistoricalMean = avg(count()) by ProductId
) on ProductId
| extend AnomalyScore = abs(CurrentRate - HistoricalMean) / HistoricalMean
| where AnomalyScore > threshold
| project Timestamp, ProductId, CurrentRate, HistoricalMean, AnomalyScore
```

#### 4.2 Python-Based Advanced Analytics - DETAILED IMPLEMENTATION

**Where to implement**: Use Fabric Notebooks with Python (similar to your existing sample_data_generation notebooks)

**Required ML Models and Code**:

**A. Anomaly Detection Models**:
```python
# 1. Statistical Anomaly Detection (Simple to start)
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class StatisticalAnomalyDetector:
    def __init__(self, window_size='1H', threshold_std=3.0):
        self.window_size = window_size
        self.threshold_std = threshold_std
    
    def detect_anomalies(self, df, value_column, time_column='timestamp'):
        """Detect anomalies using rolling statistics"""
        df = df.sort_values(time_column)
        
        # Calculate rolling mean and std
        rolling_mean = df[value_column].rolling(window=self.window_size).mean()
        rolling_std = df[value_column].rolling(window=self.window_size).std()
        
        # Calculate z-scores
        z_scores = np.abs((df[value_column] - rolling_mean) / rolling_std)
        
        # Mark anomalies
        df['anomaly_score'] = z_scores
        df['is_anomaly'] = z_scores > self.threshold_std
        
        return df[df['is_anomaly']]

# 2. Time Series Anomaly Detection (More Advanced)
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class TimeSeriesAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
    
    def prepare_features(self, df, value_column, time_column='timestamp'):
        """Create time-based features"""
        df[time_column] = pd.to_datetime(df[time_column])
        
        features = pd.DataFrame({
            'value': df[value_column],
            'hour': df[time_column].dt.hour,
            'day_of_week': df[time_column].dt.dayofweek,
            'rolling_mean_1h': df[value_column].rolling('1H').mean(),
            'rolling_std_1h': df[value_column].rolling('1H').std(),
            'lag_1': df[value_column].shift(1),
            'lag_2': df[value_column].shift(2)
        })
        
        return features.dropna()
    
    def fit_predict(self, df, value_column, time_column='timestamp'):
        features = self.prepare_features(df, value_column, time_column)
        features_scaled = self.scaler.fit_transform(features)
        
        anomaly_labels = self.model.fit_predict(features_scaled)
        anomaly_scores = self.model.decision_function(features_scaled)
        
        results = df.copy()
        results['anomaly_label'] = anomaly_labels
        results['anomaly_score'] = anomaly_scores
        results['is_anomaly'] = anomaly_labels == -1
        
        return results[results['is_anomaly']]
```

**B. Clickstream Analytics**:
```python
class ClickstreamAnalyzer:
    def __init__(self):
        pass
    
    def detect_conversion_anomalies(self, clickstream_df):
        """Detect unusual conversion patterns"""
        # Calculate conversion rates by product
        conversions = clickstream_df.groupby(['product_id', 'event_type']).size().unstack(fill_value=0)
        
        if 'purchase_completed' in conversions.columns and 'page_view' in conversions.columns:
            conversions['conversion_rate'] = conversions['purchase_completed'] / conversions['page_view']
            
            # Detect products with unusual conversion rates
            mean_rate = conversions['conversion_rate'].mean()
            std_rate = conversions['conversion_rate'].std()
            
            anomalies = conversions[
                np.abs(conversions['conversion_rate'] - mean_rate) > 2 * std_rate
            ]
            
            return anomalies
    
    def detect_user_behavior_anomalies(self, clickstream_df):
        """Detect unusual user behavior patterns"""
        user_sessions = clickstream_df.groupby(['user_id', 'session_id']).agg({
            'event_type': 'count',  # Number of events per session
            'timestamp': ['min', 'max']  # Session duration
        }).reset_index()
        
        user_sessions.columns = ['user_id', 'session_id', 'event_count', 'session_start', 'session_end']
        user_sessions['session_duration'] = (
            user_sessions['session_end'] - user_sessions['session_start']
        ).dt.total_seconds() / 60  # Duration in minutes
        
        # Detect sessions with unusual patterns
        event_threshold = user_sessions['event_count'].quantile(0.95)
        duration_threshold = user_sessions['session_duration'].quantile(0.95)
        
        anomalous_sessions = user_sessions[
            (user_sessions['event_count'] > event_threshold) |
            (user_sessions['session_duration'] > duration_threshold)
        ]
        
        return anomalous_sessions
```

**C. Manufacturing Analytics**:
```python
class ManufacturingAnalyzer:
    def __init__(self):
        pass
    
    def detect_equipment_anomalies(self, manufacturing_df):
        """Detect equipment performance anomalies"""
        # Group by asset and calculate moving averages
        asset_metrics = manufacturing_df.groupby('AssetId').apply(
            lambda x: x.set_index('timestamp').resample('5min').agg({
                'Temperature': 'mean',
                'Vibration': 'mean',
                'DefectProbability': 'mean'
            }).rolling(window=12).mean()  # 1-hour rolling average
        ).reset_index()
        
        anomalies = []
        
        for asset_id in asset_metrics['AssetId'].unique():
            asset_data = asset_metrics[asset_metrics['AssetId'] == asset_id]
            
            # Temperature anomalies
            temp_mean = asset_data['Temperature'].mean()
            temp_std = asset_data['Temperature'].std()
            temp_anomalies = asset_data[
                np.abs(asset_data['Temperature'] - temp_mean) > 2 * temp_std
            ]
            
            if not temp_anomalies.empty:
                anomalies.append({
                    'asset_id': asset_id,
                    'anomaly_type': 'temperature',
                    'timestamps': temp_anomalies['timestamp'].tolist(),
                    'values': temp_anomalies['Temperature'].tolist()
                })
        
        return anomalies
    
    def predict_defect_probability(self, manufacturing_df):
        """Predict defect probability based on sensor readings"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        
        # Prepare features
        features = ['Temperature', 'Vibration', 'Humidity']
        target = 'DefectProbability'
        
        X = manufacturing_df[features]
        y = manufacturing_df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        predictions = model.predict(X_test)
        
        return model, predictions
```

**D. KQL Integration Functions**:
```python
import json
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError

class KQLAnalytics:
    def __init__(self, cluster_url, database_name):
        # Use Azure AD authentication
        kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster_url)
        self.client = KustoClient(kcsb)
        self.database = database_name
    
    def run_anomaly_detection_query(self):
        """Run KQL query for real-time anomaly detection"""
        query = """
        let lookback = 1h;
        let threshold = 3.0;
        
        ClickstreamEvents
        | where timestamp >= ago(lookback)
        | summarize EventCount = count() by bin(timestamp, 5m), product_id
        | join kind=inner (
            ClickstreamEvents
            | where timestamp between (ago(7d) .. ago(lookback))
            | summarize HistoricalMean = avg(count()), HistoricalStd = stdev(count()) 
              by product_id
        ) on product_id
        | extend ZScore = abs(EventCount - HistoricalMean) / HistoricalStd
        | where ZScore > threshold
        | project timestamp, product_id, EventCount, HistoricalMean, ZScore
        | order by ZScore desc
        """
        
        try:
            response = self.client.execute(self.database, query)
            return response.primary_results[0].to_dataframe()
        except KustoServiceError as error:
            print(f"Error executing query: {error}")
            return None
    
    def insert_anomaly_results(self, anomalies_df):
        """Insert anomaly detection results back into EventHouse"""
        # Convert DataFrame to JSON records for ingestion
        records = anomalies_df.to_json(orient='records')
        
        # Use EventHouse streaming ingestion API
        ingest_query = f"""
        .ingest inline into table AnomalyDetectionResults <|
        {records}
        """
        
        try:
            self.client.execute(self.database, ingest_query)
            print(f"Inserted {len(anomalies_df)} anomaly records")
        except KustoServiceError as error:
            print(f"Error inserting anomalies: {error}")
```

**Required Python Packages**:
```python
# Add to requirements.txt
pandas>=1.5.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.10.0
azure-kusto-data>=3.2.0
azure-identity>=1.14.0
```

#### 4.3 Activator Rules - DETAILED IMPLEMENTATION

**What is Activator?**
- Activator is a standalone component in Microsoft Fabric RTI
- It monitors your EventHouse data in real-time and triggers actions when conditions are met
- It's similar to Azure Logic Apps but specifically designed for real-time data scenarios
- Rules are stored within the Activator service itself (not in separate files)

**Where to Store Activator Rules?**
- Rules are configured directly in the Fabric portal under the Activator service
- Each rule contains: **Condition** (KQL query) + **Action** (what to do when triggered)
- Rules are managed through the Fabric UI, not through code files

**Activator Rule Examples**:

**1. Manufacturing Equipment Overheating Alert**:
```javascript
// Condition (KQL Query):
ManufacturingTelemetry
| where timestamp >= ago(5m)
| where Temperature > 28.0  // Alert threshold
| summarize AvgTemp = avg(Temperature), MaxTemp = max(Temperature) by AssetId
| where MaxTemp > 29.0 or AvgTemp > 28.5

// Action Configuration:
{
  "actionType": "email",
  "recipients": ["operations@company.com"],
  "subject": "Equipment Overheating Alert - Asset {AssetId}",
  "body": "Asset {AssetId} temperature exceeded threshold. Current: {MaxTemp}°C, Average: {AvgTemp}°C",
  "priority": "high"
}
```

**2. Clickstream Conversion Drop Alert**:
```javascript
// Condition (KQL Query):
let baseline = 
    ClickstreamEvents
    | where timestamp between (ago(7d) .. ago(1h))
    | where event_type == "purchase_completed"
    | summarize BaselineRate = count() / 24 / 7;  // Average per hour over 7 days

let current = 
    ClickstreamEvents
    | where timestamp >= ago(1h)
    | where event_type == "purchase_completed"
    | summarize CurrentCount = count();

current
| extend BaselineRate = toscalar(baseline)
| extend ExpectedCount = BaselineRate
| extend DropPercentage = (ExpectedCount - CurrentCount) / ExpectedCount * 100
| where DropPercentage > 30  // Alert if 30% drop

// Action Configuration:
{
  "actionType": "teams",
  "webhook": "https://outlook.office.com/webhook/...",
  "message": "🚨 Conversion Rate Alert: {DropPercentage}% drop in purchases detected in the last hour",
  "priority": "medium"
}
```

**3. Manufacturing Defect Spike Alert**:
```javascript
// Condition (KQL Query):
ManufacturingTelemetry
| where timestamp >= ago(15m)
| where DefectProbability > 0.15  // High defect probability
| summarize DefectiveItems = count(), AvgDefectProb = avg(DefectProbability) 
  by AssetId, ProductId
| where DefectiveItems >= 3  // At least 3 defective items

// Action Configuration:
{
  "actionType": "webhook",
  "url": "https://your-system.com/api/quality-alert",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}"
  },
  "body": {
    "alertType": "quality_issue",
    "assetId": "{AssetId}",
    "productId": "{ProductId}",
    "defectCount": "{DefectiveItems}",
    "avgDefectProbability": "{AvgDefectProb}",
    "timestamp": "{timestamp}"
  }
}
```

**4. User Behavior Anomaly Alert**:
```javascript
// Condition (KQL Query):
ClickstreamEvents
| where timestamp >= ago(10m)
| where spike_flag == true  // Using the spike flag from simulator
| summarize SpikeEvents = count(), UniqueUsers = dcount(user_id) 
  by product_id, country_code
| where SpikeEvents > 10 and UniqueUsers > 5  // Coordinated behavior

// Action Configuration:
{
  "actionType": "multiple",
  "actions": [
    {
      "actionType": "email",
      "recipients": ["security@company.com"],
      "subject": "Potential Bot Activity Detected",
      "body": "Suspicious spike in activity for product {product_id} from {country_code}. {SpikeEvents} events from {UniqueUsers} users."
    },
    {
      "actionType": "custom_function",
      "functionUrl": "https://your-function.azurewebsites.net/api/investigate-user-behavior",
      "parameters": {
        "productId": "{product_id}",
        "countryCode": "{country_code}",
        "eventCount": "{SpikeEvents}"
      }
    }
  ]
}
```

**Activator Architecture**:
```
┌─────────────────────────────────────────────────────────────┐
│                    Activator Service                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │   Rule Engine   │    │  Action Engine  │                 │
│  │                 │    │                 │                 │
│  │ • KQL Evaluator │    │ • Email Sender  │                 │
│  │ • Condition     │────▶│ • Teams Bot     │                 │
│  │   Monitoring    │    │ • Webhook Call  │                 │
│  │ • Scheduling    │    │ • Function Call │                 │
│  └─────────────────┘    └─────────────────┘                 │
│           │                       │                         │
│           ▼                       ▼                         │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │  EventHouse     │    │ External        │                 │
│  │  Data Source    │    │ Systems         │                 │
│  └─────────────────┘    └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

**Activator Management**:
- **Configuration**: Done through Fabric Portal UI
- **Monitoring**: Built-in dashboard shows rule execution history
- **Testing**: Test rules with historical data before deploying
- **Scaling**: Automatically scales based on data volume
- **State**: Maintains state between rule executions (important for rate limiting)

### 5. Visualization & Action Layer

#### 5.1 RTI Dashboards vs Power BI - WHEN TO USE WHICH?

**RTI Dashboards** (Built into Fabric RTI):
- **Purpose**: Real-time operational monitoring and alerting
- **Data Source**: Directly connected to EventHouse (KQL queries)
- **Refresh**: Sub-second to few seconds latency
- **Best For**: 
  - Live monitoring dashboards
  - Operational KPIs that need immediate updates
  - Drill-down investigation of alerts
  - Technical/operational teams

**RTI Dashboard Examples**:
```sql
-- Real-time Manufacturing Monitor
ManufacturingTelemetry
| where timestamp >= ago(1h)
| summarize 
    AvgTemp = avg(Temperature),
    MaxVibration = max(Vibration),
    DefectRate = avg(DefectProbability)
  by bin(timestamp, 1m), AssetId
| render timechart

-- Live Clickstream Funnel
ClickstreamEvents
| where timestamp >= ago(30m)
| summarize Count = count() by event_type, bin(timestamp, 1m)
| render columnchart
```

**Power BI Dashboards**:
- **Purpose**: Business intelligence and historical analysis
- **Data Source**: EventHouse + Lakehouse (medallion architecture data)
- **Refresh**: Minutes to hours (depending on dataset size)
- **Best For**:
  - Executive reporting
  - Historical trend analysis
  - Complex business calculations
  - Cross-domain analytics (combining RTI + historical data)

**Power BI Examples**:
- Monthly sales performance with real-time current day overlay
- Customer lifetime value analysis with real-time behavior scoring
- Manufacturing efficiency reports with predictive maintenance insights

**Recommendation: Use BOTH**
```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard Strategy                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Operational Teams          Executive Teams                 │
│  ┌─────────────────┐       ┌─────────────────┐             │
│  │ RTI Dashboards  │       │ Power BI        │             │
│  │                 │       │ Dashboards      │             │
│  │ • Live Alerts   │       │                 │             │
│  │ • System Health │       │ • Monthly KPIs  │             │
│  │ • Anomaly Drill │       │ • Trends        │             │
│  │ • <5 sec latency│       │ • Forecasts     │             │
│  └─────────────────┘       │ • Strategic     │             │
│                            │   Insights      │             │
│                            └─────────────────┘             │
│                                                             │
│  Data Engineers            Business Analysts               │
│  ┌─────────────────┐       ┌─────────────────┐             │
│  │ RTI Dashboards  │       │ Power BI +      │             │
│  │                 │       │ RTI Hybrid      │             │
│  │ • Data Quality  │       │                 │             │
│  │ • Pipeline      │       │ • Combined      │             │
│  │   Health        │       │   Historical +  │             │
│  │ • Performance   │       │   Real-time     │             │
│  │   Metrics       │       │ • Advanced      │             │
│  └─────────────────┘       │   Analytics     │             │
│                            └─────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

**Specific Dashboard Implementations**:

**1. RTI Operations Dashboard** (For your team):
```sql
-- Dashboard Title: "Real-Time Operations Monitor"

-- Panel 1: System Health (Auto-refresh every 5 seconds)
ManufacturingTelemetry
| where timestamp >= ago(5m)
| summarize 
    ActiveAssets = dcount(AssetId),
    AvgTemp = avg(Temperature),
    AlertCount = countif(Temperature > 28 or DefectProbability > 0.15)
| extend Status = case(
    AlertCount == 0, "🟢 Healthy",
    AlertCount <= 5, "🟡 Warning", 
    "🔴 Critical"
)

-- Panel 2: Live Event Stream (Auto-refresh every 2 seconds)
union ClickstreamEvents, ManufacturingTelemetry
| where timestamp >= ago(1m)
| project timestamp, EventType = case(
    isnotempty(event_type), event_type,
    "manufacturing"
), Source = case(
    isnotempty(product_id), product_id,
    AssetId
)
| order by timestamp desc
| take 20

-- Panel 3: Anomaly Alerts (Auto-refresh every 10 seconds)
AnomalyDetectionResults
| where timestamp >= ago(1h)
| where severity in ("High", "Critical")
| summarize Count = count() by bin(timestamp, 5m), severity
| render columnchart
```

**2. Power BI Executive Dashboard** (For business leaders):
- **Data Sources**: 
  - Historical sales data (from existing medallion architecture)
  - Real-time EventHouse data (for current day/hour metrics)
  - Master data (customers, products from existing lakehouse)

- **Key Visuals**:
  - Monthly revenue trend with real-time current month progress
  - Product performance ranking with live conversion rates
  - Geographic sales distribution with real-time activity heat map
  - Customer satisfaction scores with real-time sentiment analysis

**3. Hybrid Analytics Dashboard** (For analysts):
```sql
-- Example: Combining Historical + Real-time
-- Historical context from Lakehouse via shortcuts
let historical_sales = 
    lakehouse('SalesGold').sales_summary
    | where sale_date >= ago(30d)
    | summarize HistoricalDailyAvg = avg(daily_sales) by product_id;

-- Real-time data from EventHouse
let realtime_activity = 
    ClickstreamEvents
    | where timestamp >= ago(1d) and event_type == "purchase_completed"
    | summarize TodaySales = count() by product_id;

historical_sales
| join kind=inner realtime_activity on product_id
| extend PerformanceRatio = TodaySales / HistoricalDailyAvg
| where PerformanceRatio < 0.7 or PerformanceRatio > 1.5  // Significant deviation
| project product_id, HistoricalDailyAvg, TodaySales, PerformanceRatio
| order by PerformanceRatio desc
```

## Data Domains & Use Cases

### Primary Domains (Building on Existing Foundation)
1. **Customer**: Real-time customer behavior analysis
2. **Product**: Dynamic product performance monitoring
3. **Sales**: Live sales tracking and anomaly detection
4. **Finance**: Real-time financial metrics and alerts

### New RTI-Specific Domains
1. **Operations**: Manufacturing and supply chain monitoring
2. **Quality**: Real-time quality control and defect detection
3. **Security**: Fraud detection and security monitoring
4. **Performance**: System and application performance monitoring

## Key Use Cases

### 1. Real-Time Customer Experience Optimization
- **Clickstream Analysis**: Identify drop-off points and conversion bottlenecks
- **Personalization**: Real-time product recommendations
- **A/B Testing**: Dynamic experiment management and results

### 2. Manufacturing Excellence
- **Predictive Maintenance**: Early warning system for equipment failures
- **Quality Control**: Real-time defect detection and prevention
- **Production Optimization**: Dynamic line balancing and efficiency improvements

### 3. Supply Chain Intelligence
- **Demand Forecasting**: Real-time demand sensing and prediction
- **Inventory Optimization**: Dynamic inventory level adjustments
- **Logistics Tracking**: Real-time shipment monitoring and route optimization

### 4. Security and Fraud Detection
- **Anomaly Detection**: Unusual patterns in customer behavior or system access
- **Real-time Alerts**: Immediate notification of potential security threats
- **Investigation Tools**: Detailed drill-down capabilities for security incidents

## Technical Implementation Considerations

### Performance & Scalability
- **EventStream**: Configure for high-throughput scenarios (10,000+ events/second)
- **EventHouse**: Optimize ingestion policies and retention settings
- **Query Optimization**: Materialized views for frequently accessed aggregations
- **Caching Strategy**: Strategic use of query result caching

### Data Quality & Governance
- **Schema Registry**: Centralized schema management for all event types
- **Data Lineage**: Track data flow from source to consumption
- **Quality Monitoring**: Automated data quality checks and alerts
- **GDPR Compliance**: Data retention and deletion policies

### Security & Compliance
- **Azure Active Directory**: Unified authentication and authorization
- **Network Security**: Private endpoints and network isolation
- **Encryption**: End-to-end encryption for sensitive data
- **Audit Logging**: Comprehensive audit trail for all operations

### Deployment & DevOps
- **Infrastructure as Code**: Bicep templates for consistent deployments
- **CI/CD Pipelines**: Automated testing and deployment processes
- **Monitoring**: Comprehensive health monitoring and alerting
- **Disaster Recovery**: Backup and recovery procedures

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
- Set up EventStream and EventHouse infrastructure
- Deploy enhanced data simulators
- Implement basic KQL queries and dashboards
- Establish monitoring and alerting

### Phase 2: Analytics Engine (Weeks 3-4)
- Develop anomaly detection algorithms
- Implement Activator rules and actions
- Create advanced RTI dashboards
- Integrate with existing Power BI reports

### Phase 3: Advanced Intelligence (Weeks 5-6)
- Deploy machine learning models
- Implement predictive analytics
- Create custom Python functions
- Optimize performance and scalability

### Phase 4: Integration & Testing (Weeks 7-8)
- Full integration with medallion architecture
- End-to-end testing scenarios
- Performance optimization
- Documentation and training materials

## Success Metrics

### Technical Metrics
- **Latency**: End-to-end latency < 5 seconds for 95% of events
- **Throughput**: Handle 10,000+ events per second sustained
- **Availability**: 99.9% uptime for critical components
- **Data Quality**: <0.1% data loss or corruption

### Business Metrics
- **Mean Time to Detection (MTTD)**: <2 minutes for critical anomalies
- **Mean Time to Resolution (MTTR)**: <15 minutes for operational issues
- **Customer Experience**: 20% improvement in conversion rates
- **Operational Efficiency**: 15% reduction in false positives

## Conclusion

This Microsoft Fabric RTI solution accelerator provides a comprehensive foundation for real-time intelligence applications. By building upon the existing unified data foundation and focusing on RTI-specific capabilities, organizations can rapidly deploy sophisticated real-time analytics and alerting systems. The architecture is designed to be extensible, scalable, and maintainable, providing a solid foundation for future enhancements and customizations.

The combination of EventStream for ingestion, EventHouse for storage and analytics, Activator for alerting, and RTI dashboards for visualization creates a powerful platform for real-time business intelligence and operational monitoring. The integration with existing medallion architecture ensures consistency with established data governance and quality standards while enabling new real-time capabilities.