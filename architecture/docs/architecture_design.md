# Microsoft Fabric RTI Solution Accelerator - Architecture Design - Draft V1.0

## Executive Summary

This document outlines the architecture design for a **standalone** Microsoft Fabric Real-Time Intelligence (RTI) solution accelerator. This is a pure RTI solution focusing entirely on real-time data processing, anomaly detection, and intelligent alerting using Microsoft Fabric's RTI capabilities including EventStream, EventHouse, Activator, and RTI dashboards. 

**Note**: This solution is completely self-contained and does not require integration with existing data lakehouses or the Unified Data Foundation solution accelerator.

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Data Sources & Simulation Layer                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Clickstream     │  │ Manufacturing   │  │ Shipping        │                  │
│  │ Simulator.ipynb │  │ Simulator.ipynb │  │ Simulator.ipynb │                  │
│  │ (RTI-Hackathon) │  │ (RTI-Hackathon) │  │ (RTI-Hackathon) │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
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
│                           Pure RTI Storage & Analytics Layer                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                    EventHouse: fabrikam_eventhouse                          │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────────┐│ │
│  │  │  clickstream_db │ │manufacturing_db │ │         shipping_db             ││ │
│  │  │                 │ │                 │ │                                 ││ │
│  │  │• User Events    │ │• Equipment Data │ │• Logistics Events               ││ │
│  │  │• Cart Activity  │ │• Telemetry      │ │• Carrier Performance            ││ │
│  │  │• Product Views  │ │• Quality Metrics│ │• Delivery Tracking              ││ │_____________________
│  │  │• E-commerce     │ │• Asset Health   │ │• Route Optimization             ││ │                    |
│  │  │  Anomalies      │ │• Production     │ │• Shipping Anomalies             ││ │                    │
│  │  │                 │ │  Anomalies      │ │                                 ││ │                    │
│  │  └─────────────────┘ └─────────────────┘ └─────────────────────────────────┘│ │                    │
│  └─────────────────────────────────────────────────────────────────────────────┘ │                    │
└─────────────────────────────────────────────────────────────────────────────────┘                     │
                                    │                                                                   │
                                    ▼                                                                   │
┌─────────────────────────────────────────────────────────────────────────────────┐                     │
│                  Simplified Real-Time Intelligence & Analytics Layer            │                     │
├─────────────────────────────────────────────────────────────────────────────────┤                     │
│  ┌─────────────────┐  ┌────────────────────────────────────────────────────────┐ │                    │
│  │   Activator     │  │            KQL Analytics (All-in-One)                  │ │                    │
│  │                 │  │                                                        │ │                    │
│  │ • Alert Rules   │  │ • Statistical Anomaly Detection (Z-scores, percentiles)│ │                    │
│  │ • Trigger       │  │ • 60-day Moving Window Baselines                       │ │                    │
│  │   Actions       │  │ • Real-time Aggregations & Calculations                │ │                    │
│  │ • Notifications │  │ • Cross-Domain Analytics (E-commerce → Mfg → Shipping) │ │                    │
│  │ • Email/Teams   │  │ • Multi-level Severity Classification                  │ │                    │
│  │ • Webhooks      │  │ • Seasonal Pattern Recognition (hour/day aware)        │ │                    │
│  └─────────────────┘  └────────────────────────────────────────────────────────┘ │                    │
└─────────────────────────────────────────────────────────────────────────────────┘                     │
                                    │                                                                   │
                                    ▼                                                                   │
┌─────────────────────────────────────────────────────────────────────────────────┐                     │
│                           Visualization & Action Layer                          │ ◄───────────────────┘
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────────────┐ │
│  │      RTI Dashboards             │  │        Fabric Data Agent               │ │
│  │      (All-in-One)               │  │        (Natural Language)              │ │
│  │                                 │  │                                        │ │
│  │ • Real-time Monitoring          │  │ • Natural Language Queries             │ │ 
│  │ • Historical Analysis (60+ days)│  │ • EventHouse Direct Access             │ │
│  │ • Executive KPIs                │  │ • Conversational Interface             │ │
│  │ • Analyst Deep-Dive             │  │ • Auto KQL Generation                  │ │
│  │ • Native Anomaly Integration    │  │ • Cross-Domain Analysis                │ │
│  │ • KQL-based Charts & Tables     │  │ • Business User Self-Service           │ │
│  │ • Sub-second Performance        │  │ • Ad-hoc Exploration                   │ │
│  │ • Multi-Stakeholder Views       │  │ • Contextual Follow-ups                │ │
│  └─────────────────────────────────┘  └─────────────────────────────────────────┘ │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            Action Systems                                   │ │
│  │                                                                             │ │
│  │  • Email Notifications            • Teams Alerts                           │ │
│  │  • Service Order Payload          • Triggers to invoke next steps          │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Sources & Simulation Layer

#### 1.1 Clickstream Simulator
- **Source**: [Clickstream Simulator.ipynb](https://github.com/L400-RTI/RTI-Hackathon/tree/main/Data%20Simulators/Clickstream%20Simulator.ipynb)
- **Data Generated**: E-commerce user interactions, page views, cart activities
- **Event Types**: Product clicks, add to cart, purchases, session tracking, anomaly spikes

#### 1.2 Manufacturing Simulator
- **Source**: [Manufacturing Simulator.ipynb](https://github.com/L400-RTI/RTI-Hackathon/tree/main/Data%20Simulators/Manufacturing%20Simulator.ipynb)
- **Data Generated**: Production line telemetry, equipment metrics, quality measurements
- **Event Types**: Temperature readings, vibration data, defect probabilities, operator activities

#### 1.3 Shipping Simulator  
- **Source**: [Shipping Simulator.ipynb](https://github.com/L400-RTI/RTI-Hackathon/tree/main/Data%20Simulators/Shipping%20Simulator.ipynb)
- **Data Generated**: Logistics events, shipment tracking, delivery status updates
- **Event Types**: Package movements, delivery confirmations, transit delays, location updates

### 2. Real-Time Data Ingestion Layer

#### 2.1 EventStream Configuration
- **Multiple Custom Endpoints**: Separate endpoints for different data types
- **Data Transformation**: 
  - Schema validation and normalization
  - Data enrichment with master data lookups
  - Real-time aggregations and windowing
- **Routing Logic**: Intelligent routing based on event types and priority levels

### 3. Real-Time Analytics & Storage Layer

#### 3.1 EventHouse Architecture - DETAILED EXPLANATION

**What is EventHouse?**

- EventHouse is Microsoft Fabric's real-time analytics service built on Azure Data Explorer (Kusto)
- It's a KQL (Kusto Query Language) database optimized for time-series and streaming data
- Unlike traditional SQL databases, it's columnar and designed for fast ingestion and analytical queries

**EventHouse Structure:**

Our solution uses one EventHouse named **`fabrikam_eventhouse`** containing three separate KQL databases for domain separation:

```
fabrikam_eventhouse/
├── clickstream_db          # E-commerce and user behavior data
├── manufacturing_db        # Production and equipment telemetry
└── shipping_db            # Logistics and delivery tracking
```

**Benefits of Multiple Databases:**
- **Domain Separation**: Clear data boundaries for different business areas
- **Security Isolation**: Fine-grained access control per business domain
- **Performance Optimization**: Dedicated resources and tuning per workload
- **Team Ownership**: Different teams can manage their respective domains
- **Cross-Database Analytics**: KQL supports queries across multiple databases
- **Scalability**: Each database can scale independently based on data volume
- **Data Governance**: Separate retention policies and compliance controls per domain

**Usage Patterns:**

**Single Database Queries (within domain):**
```sql
-- Query within clickstream_db only
ClickstreamEvents
| where timestamp >= ago(1h)
| summarize EventCount = count() by event_type

-- Query within manufacturing_db only  
ManufacturingTelemetry
| where timestamp >= ago(1h)
| summarize AvgTemp = avg(Temperature) by AssetId
```

**Cross-Database Queries (correlation analysis):**
```sql
-- Correlate e-commerce activity with manufacturing output
let ecommerce_orders = cluster('fabrikam_eventhouse').database('clickstream_db').ClickstreamEvents
    | where event_type == "purchase" and timestamp >= ago(1d)
    | summarize OrderCount = count() by bin(timestamp, 1h), product_id;

let production_output = cluster('fabrikam_eventhouse').database('manufacturing_db').ManufacturingTelemetry  
    | where timestamp >= ago(1d)
    | summarize ProductionCount = count() by bin(timestamp, 1h), ProductId;

ecommerce_orders
| join kind=inner production_output on $left.timestamp == $right.timestamp and $left.product_id == $right.ProductId
| extend DemandSupplyRatio = OrderCount * 1.0 / ProductionCount
| where DemandSupplyRatio > 1.5  // Demand exceeding supply
```

**Do you need to create tables?**
- YES, you must create tables with defined schemas (like SQL DDL) in each database
- Tables are automatically partitioned by time and optimized for streaming ingestion
- Data is automatically indexed and compressed

**Database Design (Aligned with Sample Data)**:

Based on the RTI-Hackathon simulators, here are the exact table schemas for each database:

```sql
-- =============================================================================
-- DATABASE 1: clickstream_db (E-commerce and User Behavior Data)
-- =============================================================================

-- 1. Clickstream Events Table (from Clickstream Simulator.ipynb)
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

-- Clickstream Anomaly Detection Results
.create table ClickstreamAnomalies (
    timestamp: datetime,
    anomaly_type: string,               -- cart_spike, conversion_drop, traffic_anomaly, etc.
    product_id: string,                 -- PROD4000-PROD4019
    user_id: string,                    -- User identifier
    anomaly_score: real,                -- Calculated anomaly score
    baseline_value: real,               -- Historical baseline
    current_value: real,                -- Current observed value
    severity: string,                   -- Low, Medium, High, Critical
    description: string,                -- Human readable description
    metadata: dynamic                   -- Additional context
)

-- =============================================================================
-- DATABASE 2: manufacturing_db (Production and Equipment Telemetry)
-- =============================================================================

-- 2. Manufacturing Telemetry Table (from Manufacturing Simulator.ipynb)
.create table ManufacturingTelemetry (
    event_type: string,                  -- "production" event type
    timestamp: datetime,                 -- ISO format timestamp
    SiteId: string,                      -- Manufacturing site identifier
    City: string,                        -- Production facility city
    AssetId: string,                     -- Equipment/machine identifier
    OperatorId: string,                  -- Operator identifier
    OperatorName: string,                -- Operator name
    ProductId: string,                   -- Product being manufactured
    SKU: string,                         -- Stock keeping unit
    BatchId: string,                     -- Production batch identifier
    DefectProbability: real,             -- Quality metric (0.0-1.0)
    Vibration: real,                     -- Equipment vibration reading
    Temperature: real,                   -- Operating temperature
    Humidity: int                        -- Environmental humidity
)

-- Manufacturing Sites Reference Table
.create table Sites (
    SiteId: string,
    City: string,
    Country: string,
    Region: string,
    Latitude: real,
    Longitude: real
)

-- Manufacturing Assets Reference Table
.create table Assets (
    AssetId: string,
    AssetName: string,
    AssetType: string,
    SiteId: string,
    InstallationDate: datetime,
    MaintenanceSchedule: string
)

-- Manufacturing Anomaly Detection Results
.create table ManufacturingAnomalies (
    timestamp: datetime,
    anomaly_type: string,               -- temperature_spike, vibration_anomaly, defect_rate_high, etc.
    AssetId: string,                    -- Equipment identifier
    SiteId: string,                     -- Site identifier
    anomaly_score: real,                -- Calculated anomaly score
    baseline_value: real,               -- Historical baseline
    current_value: real,                -- Current observed value
    severity: string,                   -- Low, Medium, High, Critical
    description: string,                -- Human readable description
    metadata: dynamic                   -- Additional context
)

-- =============================================================================
-- DATABASE 3: shipping_db (Logistics and Delivery Tracking)
-- =============================================================================

-- 3. Shipping Events Table (from Shipping Simulator.ipynb)
.create table ShippingEvents (
    event_id: string,                    -- Unique event identifier
    timestamp: datetime,                 -- Event timestamp
    event_type: string,                  -- shipment_created, in_transit, delivered, etc.
    tracking_number: string,             -- Package tracking identifier
    shipment_id: string,                 -- Shipment batch identifier
    origin_location: string,             -- Shipping origin
    destination_location: string,        -- Delivery destination
    carrier: string,                     -- Shipping carrier (UPS, FedEx, etc.)
    package_weight: real,                -- Package weight in kg
    estimated_delivery: datetime,        -- Estimated delivery time
    actual_delivery: datetime,           -- Actual delivery time (if delivered)
    delay_minutes: int,                  -- Delivery delay in minutes
    status: string,                      -- Current status
    location_coordinates: dynamic       -- Current GPS coordinates
)

-- Shipping Carriers Reference Table
.create table Carriers (
    CarrierId: string,
    CarrierName: string,
    ServiceLevel: string,
    Coverage_Area: string,
    AvgDeliveryTime: int
)

-- Shipping Anomaly Detection Results
.create table ShippingAnomalies (
    timestamp: datetime,
    anomaly_type: string,               -- delivery_delay, route_deviation, carrier_performance, etc.
    tracking_number: string,            -- Package identifier
    carrier: string,                    -- Shipping carrier
    anomaly_score: real,                -- Calculated anomaly score
    baseline_value: real,               -- Historical baseline
    current_value: real,                -- Current observed value
    severity: string,                   -- Low, Medium, High, Critical
    description: string,                -- Human readable description
    metadata: dynamic                   -- Additional context
)
```

**Cross-Database Query Examples:**

```sql
-- Example: Correlate manufacturing issues with shipping delays
-- Query across manufacturing_db and shipping_db
let manufacturing_issues = cluster('fabrikam_eventhouse').database('manufacturing_db').ManufacturingAnomalies
    | where timestamp >= ago(1d) and severity in ("High", "Critical")
    | project timestamp, ProductId = AssetId, anomaly_type;

let shipping_delays = cluster('fabrikam_eventhouse').database('shipping_db').ShippingAnomalies  
    | where timestamp >= ago(1d)  
    | project timestamp, tracking_number, delay_minutes;

manufacturing_issues
| join kind=inner shipping_delays on $left.timestamp == $right.timestamp  
| where delay_minutes > 60
| summarize ImpactedShipments = count() by bin(timestamp, 1h), ProductId
```

**Data Ingestion Policies**:
```sql
-- =============================================================================
-- CLICKSTREAM_DB - Ingestion Mappings
-- =============================================================================
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

-- =============================================================================
-- MANUFACTURING_DB - Ingestion Mappings  
-- =============================================================================
.create table ManufacturingTelemetry ingestion json mapping "ManufacturingMapping"
```[
    {"column":"event_type","path":"$.event_type"},
    {"column":"timestamp","path":"$.timestamp"},
    {"column":"SiteId","path":"$.SiteId"},
    {"column":"City","path":"$.City"},
    {"column":"AssetId","path":"$.AssetId"},
    {"column":"OperatorId","path":"$.OperatorId"},  
    {"column":"OperatorName","path":"$.OperatorName"},
    {"column":"ProductId","path":"$.ProductId"},
    {"column":"SKU","path":"$.SKU"},
    {"column":"BatchId","path":"$.BatchId"},
    {"column":"DefectProbability","path":"$.DefectProbability"},
    {"column":"Vibration","path":"$.Vibration"},
    {"column":"Temperature","path":"$.Temperature"},
    {"column":"Humidity","path":"$.Humidity"}
]```

-- =============================================================================
-- SHIPPING_DB - Ingestion Mappings
-- =============================================================================
.create table ShippingEvents ingestion json mapping "ShippingMapping"
```[
    {"column":"event_id","path":"$.event_id"},
    {"column":"timestamp","path":"$.timestamp"},
    {"column":"event_type","path":"$.event_type"},
    {"column":"tracking_number","path":"$.tracking_number"},
    {"column":"shipment_id","path":"$.shipment_id"},
    {"column":"origin_location","path":"$.origin_location"},
    {"column":"destination_location","path":"$.destination_location"},
    {"column":"carrier","path":"$.carrier"},
    {"column":"package_weight","path":"$.package_weight"},
    {"column":"estimated_delivery","path":"$.estimated_delivery"},
    {"column":"actual_delivery","path":"$.actual_delivery"},
    {"column":"delay_minutes","path":"$.delay_minutes"},
    {"column":"status","path":"$.status"},
    {"column":"location_coordinates","path":"$.location_coordinates"}
]```

-- =============================================================================
-- Enable streaming ingestion for all databases
-- =============================================================================
-- For clickstream_db
.alter table ClickstreamEvents policy streamingingestion enable

-- For manufacturing_db  
.alter table ManufacturingTelemetry policy streamingingestion enable

-- For shipping_db
.alter table ShippingEvents policy streamingingestion enable
```

### 4. Real-Time Intelligence & Analytics Layer

#### 4.1 KQL-Only Statistics

**KQL Capabilities:**

- **Built-in statistical functions**: avg(), stdev(), percentile(), series_* functions
- **60-day historical context**: EventHouse retention provides baseline data
- **Real-time performance**: Sub-second anomaly detection
- **Single technology stack**: Simplified architecture with KQL-only approach
- **Direct Activator integration**: No data movement between systems

**Complete KQL-Only Anomaly Detection:**

```sql
-- =============================================================================
-- CROSS-DATABASE ANOMALY DETECTION QUERIES
-- =============================================================================

-- Clickstream Anomaly Detection (using clickstream_db)
let baselineWindow = 60d;  -- Use full EventHouse retention
let detectionWindow = 5m;
let threshold = 3.0;

-- ADVANCED KQL-ONLY BASELINE CALCULATION (All statistics in pure KQL)
let current_data = cluster('fabrikam_eventhouse').database('clickstream_db').ClickstreamEvents 
    | where timestamp >= ago(detectionWindow);

// 🔄 MOVING WINDOW EXPLANATION:
// This creates a 60-day sliding window that automatically updates:
// - Hour 1: Uses data from 60 days ago to 5 minutes ago  
// - Hour 2: Uses data from (60 days - 1 hour) ago to 5 minutes ago
// - The baseline automatically adapts as your business evolves!

let statistical_baselines = cluster('fabrikam_eventhouse').database('clickstream_db').ClickstreamEvents
    | where timestamp between (ago(baselineWindow) .. ago(detectionWindow))  // 60-day moving window
    | summarize 
        baseline_mean = avg(cart_value),            // Rolling average
        baseline_stdev = stdev(cart_value),         // Rolling standard deviation  
        baseline_p50 = percentile(cart_value, 50),  // Rolling median
        baseline_p90 = percentile(cart_value, 90),  // Rolling 90th percentile
        baseline_p95 = percentile(cart_value, 95),  // Rolling 95th percentile
        baseline_p99 = percentile(cart_value, 99),  // Rolling 99th percentile
        baseline_count = count()                    // Sample size for confidence
    by product_id, hour_of_day = hourofday(timestamp);  -- Seasonal baselines

current_data
| extend hour_of_day = hourofday(timestamp)
| join kind=inner statistical_baselines on product_id, hour_of_day
| extend 
    // Z-score calculation (pure KQL)
    z_score = (cart_value - baseline_mean) / baseline_stdev,
    
    // Percentile-based anomaly detection  
    is_p95_anomaly = cart_value > baseline_p95,
    is_p99_anomaly = cart_value > baseline_p99,
    
    // Multi-level severity classification
    severity = case(
        abs(z_score) > 4.0 or is_p99_anomaly, "Critical",
        abs(z_score) > 3.0 or is_p95_anomaly, "High", 
        abs(z_score) > 2.0, "Medium",
        "Normal"
    ),
    
    // Confidence based on sample size
    confidence = case(
        baseline_count > 1000, 0.95,
        baseline_count > 100, 0.85, 
        0.70
    )
| where severity != "Normal" and confidence > 0.8
| project timestamp, product_id, cart_value, z_score, severity, confidence, 
          baseline_mean, baseline_stdev

-- Manufacturing Equipment (Pure KQL with Statistical Baselines - using manufacturing_db)
let equipment_baselines = cluster('fabrikam_eventhouse').database('manufacturing_db').ManufacturingTelemetry
    | where timestamp between (ago(60d) .. ago(1h))
    | summarize
        temp_mean = avg(Temperature),
        temp_stdev = stdev(Temperature),
        temp_p95 = percentile(Temperature, 95),
        vibration_mean = avg(Vibration), 
        vibration_p90 = percentile(Vibration, 90),
        defect_p95 = percentile(DefectProbability, 95)
    by AssetId;

cluster('fabrikam_eventhouse').database('manufacturing_db').ManufacturingTelemetry
| where timestamp >= ago(5m)
| join kind=inner equipment_baselines on AssetId
| extend
    // Statistical anomaly detection (all in KQL)
    temp_z_score = (Temperature - temp_mean) / temp_stdev,
    temp_anomaly = abs(temp_z_score) > 3.0 or Temperature > temp_p95,
    
    vibration_anomaly = Vibration > (vibration_p90 * 1.5),  -- 50% above 90th percentile
    
    defect_anomaly = DefectProbability > max_of(0.15, defect_p95 * 1.2),
    
    equipment_health = case(
        temp_anomaly and vibration_anomaly, "Critical",
        defect_anomaly, "High", 
        temp_anomaly or vibration_anomaly, "Medium",
        "Normal"  
    )
| where equipment_health != "Normal"
| project timestamp, AssetId, Temperature, Vibration, DefectProbability, 
          temp_z_score, equipment_health

-- Shipping Delay Detection (using shipping_db)
cluster('fabrikam_eventhouse').database('shipping_db').ShippingEvents  
| where timestamp >= ago(1h)
| where event_type == "delivered" and delay_minutes > 60
| summarize AvgDelay = avg(delay_minutes), DelayedShipments = count() 
  by carrier, bin(timestamp, 10m)
| where DelayedShipments > 5
| project timestamp, carrier, AvgDelay, DelayedShipments
```

### **✅ BENEFITS OF KQL-ONLY APPROACH:**

- **Simplicity**: Single technology stack reduces complexity
- **Performance**: Sub-second anomaly detection and analytics
- **Maintenance**: Unified KQL-based solution
- **Team Skills**: Single skill requirement (KQL)
- **Deployment**: EventHouse-only deployment model
- **Statistics Coverage**: Comprehensive statistical functions available in KQL

**KQL-Only Approach**

**KQL-Only Implementation:**
1. **Solution Accelerator Goal**: Get 80-90% value with minimal complexity
2. **KQL Statistical Functions**: Sufficient for most anomaly detection patterns
3. **Single Technology Stack**: Easier deployment, maintenance, and team training
4. **Real-time Performance**: No data movement or scheduling overhead
5. **GitHub Copilot Friendly**: KQL generation is excellent with Copilot

**KQL Analytics Features:**
- ✅ **Moving window baselines** (automatically adapt as business changes)
- ✅ Z-score based anomaly detection
- ✅ Percentile-based thresholds (P90, P95, P99)
- ✅ Seasonal baselines (hour-of-day, day-of-week)
- ✅ Multi-level severity classification
- ✅ Confidence scoring
- ✅ Real-time alerting via Activator
- ✅ Sub-second query performance

### **🔄 Moving Window Deep Dive:**

**How the 60-Day Moving Window Adapts Your Baselines:**

```sql
-- Example: E-commerce cart values over time

-- Week 1 (New Product Launch):
-- ago(60d) covers mostly pre-launch period
-- baseline_mean = $45, baseline_stdev = $12
-- Anomaly threshold: |z-score| > 3.0 means values outside $9-$81

-- Week 4 (Product Gaining Popularity):  
-- ago(60d) now includes 3 weeks of higher activity
-- baseline_mean = $52, baseline_stdev = $15  
-- Anomaly threshold: |z-score| > 3.0 means values outside $7-$97

-- Week 12 (Holiday Season):
-- ago(60d) includes holiday shopping patterns
-- baseline_mean = $67, baseline_stdev = $22
-- Anomaly threshold: |z-score| > 3.0 means values outside $1-$133

-- The baseline AUTOMATICALLY adjusts to your business evolution!
```

**Real-World Example with Timestamps:**

```sql
-- Query run on 2025-10-06 at 2:00 PM:
let today_baselines = ClickstreamEvents
    | where timestamp between (ago(60d) .. ago(5m))  
    // Analyzes: 2025-08-07 2:00 PM to 2025-10-06 1:55 PM
    | summarize baseline_mean = avg(cart_value) by product_id;

-- Same query run on 2025-10-07 at 2:00 PM (24 hours later):
let tomorrow_baselines = ClickstreamEvents  
    | where timestamp between (ago(60d) .. ago(5m))
    // Analyzes: 2025-08-08 2:00 PM to 2025-10-07 1:55 PM  
    // Window moved forward 24 hours automatically!
    | summarize baseline_mean = avg(cart_value) by product_id;
```

**Key Benefits:**
- **Self-adjusting**: No manual recalibration needed
- **Business-aware**: Adapts to seasonal changes, product launches, market shifts
- **Always current**: Uses the most recent 60 days of behavior
- **Handles growth**: As your business scales, thresholds scale with it

#### 4.2 Statistical Anomaly Detection Rules

**How Normal vs Abnormal is Determined Using 60 Days of EventHouse Data:**

**1. Statistical Baselines (Calculated from Historical Data)**:
```sql
-- Example: Calculate 60-day baseline for clickstream activity
let lookback_period = 60d;
let current_period = 5m;

-- Step 1: Calculate historical baseline metrics
let baselines = ClickstreamEvents
    | where timestamp between(ago(lookback_period)..ago(current_period))
    | summarize 
        Mean = avg(cart_value),
        StdDev = stdev(cart_value),
        P95 = percentile(cart_value, 95),
        P99 = percentile(cart_value, 99),
        HourlyMean = avg(events_per_hour)
    by product_id, hour_of_day = bin(timestamp, 1h) % 24;

-- Step 2: Compare current data against baselines
ClickstreamEvents
| where timestamp >= ago(current_period)
| join kind=inner baselines on product_id
| extend 
    Z_Score = (cart_value - Mean) / StdDev,
    IsAnomalous = Z_Score > 3.0 or Z_Score < -3.0,
    SeverityLevel = case(
        abs(Z_Score) > 4.0, "Critical",
        abs(Z_Score) > 3.0, "High", 
        abs(Z_Score) > 2.0, "Medium",
        "Normal"
    )
| where IsAnomalous
```

**2. Business Rule-Based Detection**:
```sql
-- Manufacturing Equipment Thresholds (Domain-Specific Rules)
ManufacturingTelemetry
| where timestamp >= ago(5m)
| extend
    -- Temperature: Normal = 22-28°C, Abnormal = outside ±3 standard deviations
    TempZ = (Temperature - 25.0) / 2.0,  -- 25°C mean, 2°C std dev
    TempAnomaly = abs(TempZ) > 3.0,
    
    -- Vibration: Normal < 1.0, Warning = 1.0-1.2, Critical > 1.2
    VibrationLevel = case(
        Vibration > 1.2, "Critical",
        Vibration > 1.0, "Warning", 
        "Normal"
    ),
    
    -- Defect Rate: Normal < 5%, Warning = 5-15%, Critical > 15%
    DefectLevel = case(
        DefectProbability > 0.15, "Critical",
        DefectProbability > 0.05, "Warning",
        "Normal"
    )
| where TempAnomaly or VibrationLevel != "Normal" or DefectLevel != "Normal"
```

**3. Time-Series Pattern Detection**:
```sql
-- Detect unusual patterns over time (seasonal, trend, spike detection)
let pattern_detection = ClickstreamEvents
    | where timestamp >= ago(7d)
    | make-series EventCount = count() on timestamp step 1h
    | extend
        -- Detect spikes: 3x higher than previous 6-hour average
        Baseline = series_moving_avg(EventCount, 6),
        SpikeThreshold = series_multiply(Baseline, 3),
        IsSpike = series_greater(EventCount, SpikeThreshold),
        
        -- Detect drops: < 50% of previous 6-hour average  
        DropThreshold = series_multiply(Baseline, 0.5),
        IsDrop = series_less(EventCount, DropThreshold)
```



#### 4.4 KQL Analytics Implementation (EventHouse Native)

**Where All Analytics Run**: Directly within EventHouse using native KQL functions

**Solution Accelerator Benefits:**
- ✅ **Zero external dependencies** - everything runs in EventHouse
- ✅ **Sub-second performance** - no data movement or scheduling overhead
- ✅ **Auto-scaling** - EventHouse handles performance optimization
- ✅ **GitHub Copilot friendly** - excellent KQL code generation
- ✅ **Single skill requirement** - team only needs to learn KQL

#### 4.5 Anomaly Detection Architecture Flow

**60-Day Baseline Analysis Flow**

```
1. HISTORICAL BASELINE CALCULATION (Every Hour)
   ↓
   EventHouse (60 days) → KQL Statistical Queries → Baseline Metrics
   ↓
   Store: Mean, StdDev, Percentiles, Seasonal Patterns
   
2. REAL-TIME COMPARISON (Every 1-5 minutes)  
   ↓
   New Events → EventHouse → KQL Anomaly Detection → Compare vs Baselines
   ↓
   Calculate: Z-Scores, Deviation %, Pattern Breaks
   
3. ANOMALY CLASSIFICATION
   ↓
   Statistical Rules + Business Rules → Severity Level (Normal/Medium/High/Critical)
   ↓
   Store Results in AnomalyDetectionResults table
   
4. REAL-TIME ALERTING
   ↓
   Activator Rules Monitor AnomalyDetectionResults → Trigger Alerts/Actions
```

**📋 Anomaly Detection Rules by Domain:**

**A. E-Commerce Clickstream Rules**:
- **Normal**: Within 2 standard deviations of 30-day historical mean
- **Medium**: 2-3 standard deviations from mean (unusual but not critical)
- **High**: 3-4 standard deviations (significant anomaly)
- **Critical**: >4 standard deviations OR sudden 10x spike in cart abandonment

**B. Manufacturing Equipment Rules**:
- **Normal**: Temperature 22-28°C, Vibration <1.0, Defect Rate <5%
- **Medium**: Temperature 28-30°C, Vibration 1.0-1.2, Defect Rate 5-10%
- **High**: Temperature 30-32°C, Vibration 1.2-1.5, Defect Rate 10-15%  
- **Critical**: Temperature >32°C, Vibration >1.5, Defect Rate >15%

**C. Shipping Performance Rules**:
- **Normal**: Delivery delays within 95th percentile of historical data
- **Medium**: Delays exceed 95th percentile but <99th percentile  
- **High**: Delays exceed 99th percentile
- **Critical**: Delays >2x worst historical performance OR >50% shipments delayed

#### 4.4 Activator Rules Configuration

Activator monitors the anomaly detection results and triggers actions when thresholds are exceeded. Rules are configured in the Fabric portal with KQL query conditions and corresponding actions.

**Example Activator Rules**:

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
// Condition: Detect conversion rate drops
let baseline = 
    ClickstreamEvents
    | where timestamp between (ago(7d) .. ago(1h))
    | where event_type == "purchase_completed"
    | summarize BaselineRate = count() / 24 / 7;

let current = 
    ClickstreamEvents
    | where timestamp >= ago(1h)
    | where event_type == "purchase_completed"
    | summarize CurrentCount = count();

current
| extend BaselineRate = toscalar(baseline)
| extend DropPercentage = (BaselineRate - CurrentCount) / BaselineRate * 100
| where DropPercentage > 30

// Action: Alert marketing team
{
  "actionType": "teams",
  "webhook": "https://outlook.office.com/webhook/...",
  "message": "🚨 Conversion Alert: {DropPercentage}% drop detected in last hour"
}
```

**3. Shipping Delay Alert**:
```javascript
// Condition: Detect high shipping delays
ShippingEvents
| where timestamp >= ago(30m)
| where event_type == "delivered" and delay_minutes > 120
| summarize DelayedShipments = count(), AvgDelay = avg(delay_minutes)
  by carrier
| where DelayedShipments >= 5

// Action: Notify logistics team
{
  "actionType": "email",
  "recipients": ["logistics@company.com"],
  "subject": "Shipping Delay Alert - {carrier}",
  "body": "High delays detected: {DelayedShipments} shipments with avg delay {AvgDelay} minutes."
}
```

**4. Manufacturing Defect Spike Alert**:
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

**5. Asset Performance Degradation Alert**:
```javascript
// Condition: Detect equipment performance issues
ManufacturingTelemetry
| where timestamp >= ago(20m)
| summarize AvgTemp = avg(Temperature), AvgVibration = avg(Vibration)
  by AssetId
| where AvgTemp > 27.5 or AvgVibration > 1.1

// Action: Alert maintenance team
{
  "actionType": "email", 
  "recipients": ["maintenance@company.com"],
  "subject": "Asset Performance Alert - {AssetId}",
  "body": "Performance degradation detected. Temp: {AvgTemp}°C, Vibration: {AvgVibration}"
}
```

### 4.5 Complete Anomaly Detection Workflow (60-Day Baseline System)

**🔄 Continuous Monitoring Queries That Run Every 1-5 Minutes:**

```sql
-- QUERY 1: Update Statistical Baselines (Runs every hour)
.create-or-alter function UpdateBaselines() {
    let baseline_period = 60d;
    let exclude_recent = 1h;  -- Exclude recent data to avoid skewing baselines
    
    // Calculate rolling statistics for each metric
    ClickstreamEvents
    | where timestamp between(ago(baseline_period + exclude_recent)..ago(exclude_recent))
    | summarize 
        Mean_CartValue = avg(cart_value),
        StdDev_CartValue = stdev(cart_value),
        P50_CartValue = percentile(cart_value, 50),
        P90_CartValue = percentile(cart_value, 90),
        P95_CartValue = percentile(cart_value, 95),
        P99_CartValue = percentile(cart_value, 99),
        Mean_EventsPerHour = avg(events_per_hour),
        StdDev_EventsPerHour = stdev(events_per_hour)
    by product_id, day_of_week = dayofweek(timestamp), hour_of_day = hourofday(timestamp)
    | extend 
        baseline_timestamp = now(),
        baseline_period_days = 60
}

-- QUERY 2: Real-Time Anomaly Detection (Runs every 5 minutes)
.create-or-alter function DetectAnomalies() {
    let detection_window = 5m;
    let current_time = now();
    
    // Get current events and join with baselines
    let current_events = ClickstreamEvents
        | where timestamp >= ago(detection_window)
        | extend 
            day_of_week = dayofweek(timestamp),
            hour_of_day = hourofday(timestamp);
    
    let baselines = BaselineMetrics  -- Updated by UpdateBaselines()
        | where baseline_timestamp >= ago(2h);  -- Use recent baselines
    
    current_events
    | join kind=inner baselines on product_id, day_of_week, hour_of_day
    | extend
        // Calculate Z-scores
        CartValue_ZScore = (cart_value - Mean_CartValue) / StdDev_CartValue,
        EventRate_ZScore = (events_per_hour - Mean_EventsPerHour) / StdDev_EventsPerHour,
        
        // Classify anomaly severity
        CartValue_Severity = case(
            abs(CartValue_ZScore) > 4.0, "Critical",
            abs(CartValue_ZScore) > 3.0, "High", 
            abs(CartValue_ZScore) > 2.0, "Medium",
            "Normal"
        ),
        
        EventRate_Severity = case(
            abs(EventRate_ZScore) > 4.0, "Critical",
            abs(EventRate_ZScore) > 3.0, "High",
            abs(EventRate_ZScore) > 2.0, "Medium", 
            "Normal"
        ),
        
        // Overall anomaly flag
        IsAnomalous = CartValue_Severity != "Normal" or EventRate_Severity != "Normal",
        
        // Calculate confidence based on historical variance
        Confidence = case(
            StdDev_CartValue > 0, min_of(1.0, 1.0 / StdDev_CartValue),
            0.5
        )
    
    | where IsAnomalous
    | project 
        detection_timestamp = current_time,
        timestamp,
        product_id,
        cart_value,
        events_per_hour,
        CartValue_ZScore,
        EventRate_ZScore, 
        CartValue_Severity,
        EventRate_Severity,
        Confidence,
        baseline_mean = Mean_CartValue,
        baseline_stddev = StdDev_CartValue
}

-- QUERY 3: Manufacturing Equipment Monitoring (Runs every 1 minute)
.create-or-alter function MonitorEquipment() {
    let monitoring_window = 1m;
    let equipment_baselines = 60d;
    
    // Get equipment baselines
    let baselines = ManufacturingTelemetry
        | where timestamp between(ago(equipment_baselines + 1h)..ago(1h))
        | summarize
            Mean_Temp = avg(Temperature),
            StdDev_Temp = stdev(Temperature), 
            Mean_Vibration = avg(Vibration),
            P95_Vibration = percentile(Vibration, 95),
            Mean_DefectRate = avg(DefectProbability),
            P90_DefectRate = percentile(DefectProbability, 90)
        by AssetId;
    
    // Monitor current equipment performance
    ManufacturingTelemetry
    | where timestamp >= ago(monitoring_window)
    | join kind=inner baselines on AssetId
    | extend
        // Temperature anomaly (Z-score based)
        Temp_ZScore = (Temperature - Mean_Temp) / StdDev_Temp,
        Temp_Anomaly = abs(Temp_ZScore) > 3.0,
        
        // Vibration anomaly (percentile based)
        Vibration_Anomaly = Vibration > P95_Vibration * 1.5,
        
        // Defect rate anomaly (threshold + percentile based)
        DefectRate_Anomaly = DefectProbability > max_of(0.15, P90_DefectRate * 1.2),
        
        // Overall equipment health
        Equipment_Status = case(
            Temp_Anomaly and Vibration_Anomaly, "Critical",
            DefectRate_Anomaly, "High",
            Temp_Anomaly or Vibration_Anomaly, "Medium", 
            "Normal"
        )
    
    | where Equipment_Status != "Normal"
    | project
        timestamp,
        AssetId,
        Temperature,
        Vibration, 
        DefectProbability,
        Temp_ZScore,
        Equipment_Status,
        baseline_temp_mean = Mean_Temp,
        baseline_vibration_p95 = P95_Vibration
}
```

**🚨 How Activator Uses These Results:**

The anomaly detection queries populate the `AnomalyDetectionResults` table, which Activator monitors with these rules:

```sql
-- Activator Rule 1: Critical E-commerce Anomalies
AnomalyDetectionResults 
| where detection_timestamp >= ago(1m)
| where CartValue_Severity == "Critical" or EventRate_Severity == "Critical"
| where Confidence > 0.8  -- High confidence threshold
| project product_id, CartValue_ZScore, EventRate_ZScore, Confidence

-- Activator Rule 2: Manufacturing Equipment Failures  
AnomalyDetectionResults
| where detection_timestamp >= ago(30s) 
| where Equipment_Status == "Critical"
| project AssetId, Temperature, Vibration, Equipment_Status

-- Activator Rule 3: Pattern-Based Shipping Delays
ShippingEvents
| where timestamp >= ago(10m)
| where delay_minutes > 120  -- 2+ hour delays
| summarize DelayedCount = count(), AvgDelay = avg(delay_minutes) by carrier
| where DelayedCount > 5  -- Multiple delayed shipments
```

### 5. Visualization & Action Layer

#### 5.1 RTI Dashboards

RTI Dashboards provide real-time visualization with sub-second refresh rates, supporting both operational monitoring and executive reporting through KQL-based analytics.

**Key Capabilities:**

**Historical Analysis Examples:**
```sql
-- RTI Dashboard can show 60-day trends just fine:
ClickstreamEvents
| where timestamp >= ago(60d)
| summarize DailyEvents = count() by bin(timestamp, 1d)
| render timechart 

-- Executive KPIs in RTI Dashboard:
ManufacturingTelemetry
| where timestamp >= ago(30d)
| summarize 
    AvgEfficiency = avg(efficiency_percent),
    DefectRate = avg(DefectProbability),
    UptimePercent = countif(status == "Running") * 100.0 / count()
| render columnchart
```

**RTI Dashboard Features:**
- Real-time + Historical visualization in single interface
- Direct EventHouse access for optimal performance  
- Native anomaly detection integration
- KQL-based analytics and visualization
- Sub-second refresh capabilities



**Dashboard Types:**

**1. Operations Dashboard** (Technical Teams):
```sql
-- Real-time system health with sub-second refresh
ManufacturingTelemetry
| where timestamp >= ago(5m)
| summarize Count = count(), AvgTemp = avg(Temperature) by bin(timestamp, 30s)
| render timechart
```

**2. Executive Dashboard** (Business Leaders):
```sql
-- Historical trends and KPIs (updated every minute)
ClickstreamEvents
| where timestamp >= ago(30d)
| summarize 
    DailyRevenue = sum(cart_value),
    ConversionRate = countif(event_type == "purchase") * 100.0 / count(),
    AnomalyCount = countif(severity == "Critical")
by bin(timestamp, 1d)
| render linechart
```

**3. Analyst Dashboard** (Data Teams):
```sql
-- Deep-dive analytics with anomaly correlation
AnomalyDetectionResults
| where detection_timestamp >= ago(7d)
| join kind=inner ClickstreamEvents on product_id
| summarize 
    AnomalyEvents = count(),
    ImpactedRevenue = sum(cart_value),
    RecoveryTime = avg(resolution_minutes)
by severity, product_category
| render piechart
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
union ClickstreamEvents, ManufacturingTelemetry, ShippingEvents
| where timestamp >= ago(1m)
| project timestamp, EventType = case(
    isnotempty(user_id), "clickstream",
    isnotempty(tracking_number), "shipping",
    "manufacturing"  
), Source = case(
    isnotempty(user_id), product_id,
    isnotempty(tracking_number), tracking_number,
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

**2. RTI Executive Dashboard** (For business leaders - all in RTI):
```sql
-- Executive KPIs using RTI Dashboard (no Power BI needed)
-- 30-day business performance metrics
ClickstreamEvents
| where timestamp >= ago(30d)
| summarize 
    "Daily Revenue" = sum(cart_value),
    "Conversion Rate %" = countif(event_type == "purchase") * 100.0 / count(),
    "Anomaly Events" = countif(severity == "Critical")
by bin(timestamp, 1d)
| render linechart

-- Manufacturing efficiency trends (90-day history)  
ManufacturingTelemetry
| where timestamp >= ago(90d)
| summarize 
    "Equipment Uptime %" = countif(status == "Running") * 100.0 / count(),
    "Average Efficiency" = avg(efficiency_percent),
    "Defect Rate %" = avg(DefectProbability) * 100
by bin(timestamp, 1d)
| render areachart
```

**3. RTI Analytics Dashboard** (For analysts - deep dive):
```sql
-- Example: Historical baselines from EventHouse retention
let historical_baselines = 
    ClickstreamEvents
    | where timestamp between(ago(30d)..ago(1d))
    | summarize HistoricalDailyAvg = avg(cart_value) by product_id;

-- Real-time anomaly detection from EventHouse
let realtime_production = 
    ManufacturingTelemetry
    | where timestamp >= ago(1d)
    | summarize TodayProduction = count(), AvgDefectRate = avg(DefectProbability) 
      by ProductId;

historical_production
| join kind=inner realtime_production on ProductId
| extend ProductionRatio = TodayProduction / HistoricalDailyAvg
| extend QualityDelta = AvgDefectRate - HistoricalDefectRate
| where ProductionRatio < 0.8 or QualityDelta > 0.05  // Production or quality issues
| project ProductId, HistoricalDailyAvg, TodayProduction, ProductionRatio, QualityDelta
| order by ProductionRatio asc
```

#### 5.2 Fabric Data Agent - Natural Language Query Interface

The Fabric Data Agent provides users with a conversational interface to query data from the EventHouse using natural language, making real-time analytics accessible to business users without requiring KQL expertise.

**Key Capabilities:**

**Natural Language Processing:**
- **Intent Recognition**: Understands business questions like "Show me anomalies in manufacturing data today"
- **Contextual Awareness**: Maintains conversation context for follow-up questions
- **Auto-completion**: Suggests relevant queries based on available data schemas
- **Query Translation**: Converts natural language to optimized KQL queries automatically

**EventHouse Integration:**
- **Direct Access**: Queries EventHouse data in real-time without data movement
- **Schema Awareness**: Understands table structures and relationships automatically
- **Security Compliance**: Respects user permissions and data access policies
- **Performance Optimization**: Generates efficient KQL queries for fast response times

**Example User Interactions:**

```
User: "What are the top 5 products with anomalies in the last hour?"
Data Agent: Executing query on ClickstreamEvents...

Generated KQL:
ClickstreamEvents
| where timestamp >= ago(1h) and spike_flag == true
| summarize AnomalyCount = count() by product_id
| top 5 by AnomalyCount desc
| project ProductID = product_id, Anomalies = AnomalyCount

Results:
ProductID    | Anomalies
PROD4015     | 23
PROD4008     | 18
PROD4012     | 15
PROD4003     | 12
PROD4019     | 9
```

```
User: "Show me manufacturing equipment with high temperatures"
Data Agent: Querying ManufacturingTelemetry for temperature anomalies...

Generated KQL:
ManufacturingTelemetry
| where timestamp >= ago(1h)
| where Temperature > 30.0  // Above normal operating range
| summarize AvgTemp = avg(Temperature), MaxTemp = max(Temperature), 
           EventCount = count() by AssetId, City
| order by MaxTemp desc

Results:
AssetId      | City        | AvgTemp | MaxTemp | EventCount
ASSET_Berlin_3| Berlin     | 32.5    | 35.2    | 45
ASSET_Munich_1| Munich     | 31.8    | 33.7    | 38
ASSET_Hamburg_2| Hamburg   | 30.9    | 32.1    | 29
```

```
User: "Compare shipping delays between carriers this week"
Data Agent: Analyzing ShippingEvents for carrier performance...

Generated KQL:
ShippingEvents
| where timestamp >= ago(7d) and event_type == "delivered"
| where delay_minutes > 0
| summarize 
    TotalShipments = count(),
    DelayedShipments = countif(delay_minutes > 60),
    AvgDelayMinutes = avg(delay_minutes),
    DelayRate = round(countif(delay_minutes > 60) * 100.0 / count(), 1)
by carrier
| order by DelayRate desc

Results:
Carrier   | TotalShipments | DelayedShipments | AvgDelayMinutes | DelayRate%
FedEx     | 1,245         | 89               | 15.3            | 7.1
UPS       | 2,156         | 108              | 12.8            | 5.0
DHL       | 987           | 35               | 8.9             | 3.5
```

**Advanced Features:**

**1. Contextual Follow-up Questions:**
```
User: "Show me the equipment with high defect rates"
Data Agent: [Shows results for ManufacturingTelemetry with DefectProbability > 0.15]

User: "What about their temperature readings?"
Data Agent: [Automatically includes Temperature data for the same equipment from previous query]

User: "When did this start?"
Data Agent: [Shows time-series analysis of when defect rates began increasing]
```

**2. Cross-Domain Analysis:**
```
User: "Are there any correlations between manufacturing delays and shipping problems?"
Data Agent: Analyzing relationships between ManufacturingTelemetry and ShippingEvents...

Generated KQL:
let manufacturing_delays = ManufacturingTelemetry
    | where timestamp >= ago(7d) and DefectProbability > 0.1
    | summarize DefectEvents = count() by bin(timestamp, 1h), ProductId;
    
let shipping_delays = ShippingEvents  
    | where timestamp >= ago(7d) and delay_minutes > 60
    | summarize DelayEvents = count() by bin(timestamp, 1h);
    
manufacturing_delays
| join kind=inner shipping_delays on timestamp
| where DefectEvents > 5 and DelayEvents > 3
| project timestamp, ProductId, DefectEvents, DelayEvents
```

**3. Anomaly Explanation:**
```
User: "Why is PROD4015 showing so many anomalies?"
Data Agent: Analyzing anomaly patterns for PROD4015...

Generated Analysis:
- Anomaly started at 2:30 PM today
- Cart spike magnitude increased from normal 5-10 to 85-95
- Coincides with social media referral traffic spike
- Similar pattern seen during previous product launches
- Recommended action: Monitor conversion rates for next 2 hours
```



## Accelerated Development Timeline (8 Weeks Total)

**Timeline Reduction Factors**:
- **GitHub Copilot**: 40-50% faster code development across all languages
- **Multi-skilled Team**: DevOps + Application development capabilities per person
- **Solution Accelerator Focus**: Prototype/demo quality, not production-hardened
- **Pure RTI Solution**: No complex lakehouse integration or master data dependencies
- **Self-Contained Architecture**: EventHouse handles both real-time and historical data needs

### **Phase 1: Rapid Foundation Setup (Weeks 1-2)**

**Week 1: Environment & Core Implementation**

- **Team**: Technical Lead + Full-Stack RTI Developer
- **GitHub Copilot Acceleration**: Bicep templates, automation scripts, KQL schemas
- **Deliverables**:
  - Complete Azure environment + Fabric workspace setup
  - EventHouse schema implementation (all 3 simulators)
  - Enhanced RTI-Hackathon simulators deployment
  - EventStream configuration with data ingestion
  - Basic KQL analytics queries

**Week 2: Analytics & Detection Foundation**
- **Team**: Technical Lead + 2 Full-Stack RTI Developers (parallel development)
- **GitHub Copilot Acceleration**: KQL statistical patterns, anomaly detection algorithms
- **Deliverables**:
  - **Pure KQL statistical anomaly detection** (simplified approach)
  - Real-time KQL analytics for all domains (Z-scores, percentiles)
  - 60-day baseline calculations in native KQL
  - Basic Activator rules configuration
  - Initial dashboard queries

### **Phase 2: RTI Platform Integration (Weeks 3-5)**

**Week 3: Dashboards & Comprehensive Alerting**
- **Team**: 2 Full-Stack RTI Developers + Technical Lead (review)
- **GitHub Copilot Acceleration**: Dashboard KQL, alert configurations, webhook APIs
- **Deliverables**:
  - **RTI dashboards for all stakeholders** (operations, executive, analyst views)
  - Comprehensive Activator rules (manufacturing, shipping, e-commerce)
  - Alert integrations (email, Teams, webhook endpoints)
  - **Multi-purpose RTI dashboards** (real-time + historical in single interface)
  - Real-time monitoring configuration

**Week 4: Cross-Domain Analytics & Self-Contained Integration**
- **Team**: Technical Lead + Full-Stack RTI Developer + RTI Specialist (if needed)
- **GitHub Copilot Acceleration**: Complex KQL joins, pure RTI analytics patterns
- **Deliverables**:
  - Cross-domain analytics within EventHouse (E-commerce → Manufacturing → Shipping flow)
  - Historical baseline calculations using EventHouse retention data
  - Advanced KQL analytics patterns for pure RTI solution
  - Performance optimization and monitoring
  - Self-contained reference data management in EventHouse

**Week 5: Advanced Features & Validation**
- **Team**: 2 Full-Stack RTI Developers (parallel feature work)
- **GitHub Copilot Acceleration**: Advanced KQL development, testing frameworks, validation scripts
- **Deliverables**:
  - **Advanced KQL statistical functions** (complex anomaly detection patterns)
  - Integration testing automation
  - Performance benchmarking
  - Security configuration implementation
  - End-to-end validation testing

### **Phase 3: Solution Accelerator Packaging (Weeks 6-8)**
  **Week 6: Infrastructure as Code & Automation**
- **Team**: Technical Lead + Full-Stack RTI Developer
- **GitHub Copilot Acceleration**: Bicep templates, automation scripts, deployment pipelines
- **Deliverables**:
  - Complete azd template with one-command deployment
  - CI/CD pipelines for solution accelerator
  - Infrastructure automation and environment setup
  - Deployment validation and testing scripts
  - Security configuration and compliance validation

**Week 7: Documentation & Testing**
- **Team**: All Team Members (parallel documentation work)
- **GitHub Copilot Acceleration**: Documentation generation, test automation, code comments
- **Deliverables**:
  - Comprehensive deployment guides and README
  - User documentation and tutorials
  - API documentation and code comments
  - Automated testing suite
  - Performance benchmarking and validation

**Week 8: Final Integration & Release Preparation**
- **Team**: All Team Members (final polish and integration)
- **GitHub Copilot Acceleration**: Integration testing, bug fixes, optimization
- **Deliverables**:
  - End-to-end integration testing
  - GitHub repository publication ready
  - Solution accelerator marketplace preparation
  - Demo videos and presentation materials
  - Launch communication and community engagement setup

### **Critical Dependencies & Risks**

**Dependencies**:
- Microsoft Fabric RTI service availability
- Azure DevOps/GitHub Actions setup
- Team member availability and onboarding
- RTI-Hackathon simulator repositories access

**Risk Mitigation**:
- **Skill gaps**: Plan for 2-week overlap/training period
- **Technology changes**: Maintain close contact with Microsoft Fabric product team
- **Timeline risks**: Build 20% buffer into each phase
- **Quality risks**: Implement automated testing from Week 2

### **Success Metrics for Team**

**Technical Metrics**:
- **Code Quality**: >90% test coverage, <5% critical bugs
- **Performance**: <5 seconds end-to-end latency for 95% of scenarios
- **Deployment**: <30 minutes automated deployment time
- **Documentation**: 100% API/component documentation coverage

**Business Metrics**:
- **Adoption**: >100 GitHub stars within 3 months of release
- **Usage**: >50 successful azd deployments within 6 months
- **Community**: >20 community contributions/issues within 6 months
- **Feedback**: >4.5/5 user satisfaction score

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

## Solution Accelerator Publishing Strategy

### GitHub Repository Structure

```
microsoft/fabric-rti-solution-accelerator/
├── README.md                           # Main documentation
├── azure.yaml                          # azd configuration
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Continuous integration
│       └── deploy.yml                  # Deployment validation
├── infra/                              # Infrastructure as Code
│   ├── main.bicep                      # Main Bicep template
│   ├── modules/
│   │   ├── eventhouse.bicep            # EventHouse resources
│   │   ├── eventstream.bicep           # EventStream resources
│   │   ├── fabric-workspace.bicep      # Fabric workspace setup
│   │   └── security.bicep              # Security configurations
│   └── parameters/
│       ├── main.parameters.json        # Default parameters
│       └── main.parameters.dev.json    # Development parameters
├── src/
│   ├── simulators/                     # Enhanced data simulators  
│   │   ├── clickstream_simulator.ipynb
│   │   ├── manufacturing_simulator.ipynb
│   │   └── shipping_simulator.ipynb
│   ├── kql/                           # KQL queries and statistical functions (ALL analytics)
│   │   ├── schema_setup.kql
│   │   ├── anomaly_queries.kql
│   │   └── dashboard_queries.kql
│   └── activator/                     # Activator rule templates
│       ├── manufacturing_alerts.json
│       ├── clickstream_alerts.json
│       └── security_alerts.json
├── docs/                              # Documentation
│   ├── architecture_design.md
│   ├── implementation_examples.md
│   ├── deployment_guide.md
│   ├── user_guide.md
│   └── troubleshooting.md
├── scripts/                           # Deployment and utility scripts
│   ├── deploy.ps1                     # PowerShell deployment script
│   ├── setup_data.ps1                 # Data setup automation
│   └── validate_deployment.ps1        # Post-deployment validation
└── samples/                           # Sample configurations
    ├── sample_data/
    └── sample_configs/
```

### azd Integration Strategy

#### azure.yaml Configuration
```yaml
# azure.yaml
name: fabric-rti-accelerator
metadata:
  template: fabric-rti-solution-accelerator@0.1.0
  
services:
  fabric-workspace:
    project: ./src
    host: fabric
    
  data-simulators:
    project: ./src/simulators  
    host: fabric

infra:
  path: ./infra
  
pipeline:
  provider: azdo
  
hooks:
  postdeploy:
    windows:
      - pwsh: ./scripts/setup_data.ps1
    posix:
      - bash: ./scripts/setup_data.sh
```

#### Bicep Template Integration (Reusing Existing Assets)
```bicep
// main.bicep - Building on existing unified data foundation
param environmentName string
param location string = resourceGroup().location
param fabricWorkspaceName string = '${environmentName}-fabric-rti'

// Import existing modules from unified data foundation
module fabricWorkspace 'modules/fabric-workspace.bicep' = {
  name: 'fabric-workspace'
  params: {
    workspaceName: fabricWorkspaceName
    location: location
    enableRTI: true
  }
}

module eventHouse 'modules/eventhouse.bicep' = {
  name: 'eventhouse'
  params: {
    eventHouseName: '${environmentName}-eventhouse'
    workspaceId: fabricWorkspace.outputs.workspaceId
    location: location
  }
}

module eventStream 'modules/eventstream.bicep' = {
  name: 'eventstream'
  params: {
    eventStreamName: '${environmentName}-eventstream'
    eventHouseConnectionString: eventHouse.outputs.connectionString
    workspaceId: fabricWorkspace.outputs.workspaceId
  }
}

// Reuse existing security and monitoring modules
module security '../existing-foundation/modules/security.bicep' = {
  name: 'security'
  params: {
    workspaceId: fabricWorkspace.outputs.workspaceId
    enableRTIAccess: true
  }
}
```

### Deployment Automation Strategy

#### One-Command Deployment Experience
```bash
# For new users - complete setup
azd up

# For developers - incremental updates  
azd deploy

# For testing - clean environment
azd down --purge
```

#### Post-Deployment Automation
```powershell
# scripts/setup_data.ps1
param(
    [string]$EnvironmentName,
    [string]$SubscriptionId,
    [string]$ResourceGroupName
)

Write-Host "🚀 Setting up Fabric RTI Solution Accelerator..." -ForegroundColor Green

# 1. Deploy EventHouse schema
Write-Host "📊 Creating EventHouse tables and mappings..."
& ./scripts/setup_eventhouse_schema.ps1 -env $EnvironmentName

# 2. Configure EventStream endpoints
Write-Host "🔄 Configuring EventStream endpoints..."
& ./scripts/setup_eventstream.ps1 -env $EnvironmentName

# 3. Deploy analytics queries
Write-Host "� Deploying analytics queries..."
& ./scripts/deploy_queries.ps1 -env $EnvironmentName

# 4. Start data simulators
Write-Host "⚡ Starting data simulators..."
& ./scripts/start_simulators.ps1 -env $EnvironmentName -duration 300

# 5. Validate deployment
Write-Host "✅ Validating deployment..."
& ./scripts/validate_deployment.ps1 -env $EnvironmentName

Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host "📈 Access your RTI dashboards at: https://fabric.microsoft.com/workspace/$workspaceId" -ForegroundColor Blue
```

#### 
## Team Recommendations

### **Key Changes Made Based on Your Feedback:**

#### **1. Removed Technical Writer Role** ✅
- **Why**: Your team already excels at documentation from previous solution accelerators
- **How**: Documentation responsibilities distributed across all team members
- **Result**: Reduced team size from 6-8 to 5-6 people
- **Cost Savings**: ~$150K-200K in salary costs

#### **2. ML Component Assessment**

ML is not required for initial implementation success.

**KQL-Only Approach Benefits:**

- **80-90% of anomaly detection value** using KQL statistical functions
- **Faster development** (3-4 weeks saved with simplified integration)
- **Simpler architecture** (single technology stack)
- **Better performance** (sub-second detection, no data movement)
- **Easier maintenance** (no complex notebooks, scheduling, or dependencies)
- **Better explainability** (business users understand z-scores and percentiles)
- **Reduced skill requirements** (KQL-only approach)

**KQL Can Handle Most Use Cases:**
```sql
-- This simple query catches most anomalies effectively
ManufacturingTelemetry
| extend Rolling24HourAvg = avg(Temperature) over (partition by AssetId order by timestamp range between 24h preceding and current row)
| extend IsAnomaly = abs(Temperature - Rolling24HourAvg) > 3.0
| where IsAnomaly
```

**When to Add ML Later (Optional Phase 2):**
- **Predictive maintenance**: "This equipment will fail in 2 weeks"
- **Demand forecasting**: Multi-variate predictions
- **Advanced fraud detection**: Complex pattern recognition
- **Customer lifetime value**: Behavioral clustering

#### **3. Technical Team Structure (5-6 People):**

| Role | Priority | Focus | Can Handle Documentation |
|------|----------|-------|-------------------------|
| **Technical Lead** | Critical | Architecture, KQL, Leadership, GitHub Copilot Expert | ✅ High-level docs |
| **Full-Stack RTI Developers (3)** | Critical | EventStream, EventHouse, Activator, DevOps | ✅ All documentation |
| **QA** | Critical | Quality Check | ✅ QA |

#### **4. Timeline:**
**Estimate**: 8 weeks 

