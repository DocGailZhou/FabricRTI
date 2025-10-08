# RTI Solution Accelerator - Source Code Structure

This folder contains all source code for the Microsoft Fabric RTI Solution Accelerator.

## Folder Structure

```
src/
├── simulators/          # Data simulation notebooks (.ipynb)
│   ├── clickstream_simulator.ipynb
│   ├── manufacturing_simulator.ipynb
│   └── shipping_simulator.ipynb
├── eventhouse/          # EventHouse KQL scripts
│   ├── table_creation.kql
│   ├── anomaly_detection.kql
│   └── data_validation.kql
├── analytics/           # KQL analytics queries
│   ├── clickstream_analytics.kql
│   ├── manufacturing_analytics.kql
│   ├── shipping_analytics.kql
│   └── cross_domain_analytics.kql
├── eventstream/         # EventStream configuration
│   ├── clickstream_config.json
│   ├── manufacturing_config.json
│   └── shipping_config.json
├── activator/           # Activator alert rules
│   ├── manufacturing_alerts.json
│   ├── clickstream_alerts.json
│   └── shipping_alerts.json
└── dashboards/          # Dashboard configurations
    ├── operations_dashboard.json
    ├── executive_dashboard.json
    └── analyst_dashboard.json
```

## Components Overview

### 🔄 simulators/
Contains Jupyter notebooks (.ipynb) that generate realistic data for:
- **Clickstream**: E-commerce user interactions, cart activities, purchase events
- **Manufacturing**: Equipment telemetry, temperature, vibration, defect rates
- **Shipping**: Package tracking, delivery status, location updates

### 🏛️ eventhouse/
KQL scripts for EventHouse database setup and management:
- Table creation with proper schemas and ingestion mappings
- Anomaly detection queries using 60-day moving baselines
- Data validation and monitoring queries

### 📊 analytics/
Advanced KQL analytics queries for:
- Real-time anomaly detection with statistical baselines
- Cross-domain correlation analysis
- Business intelligence and reporting queries

### 🌊 eventstream/
Configuration files for EventStream data ingestion:
- Custom endpoint configurations for each data simulator
- Data transformation and routing logic
- Real-time streaming setup parameters

### 🚨 activator/
Alert rule configurations for real-time monitoring:
- Manufacturing equipment overheating alerts
- E-commerce conversion drop notifications
- Shipping delay escalation rules

### 📈 dashboards/
Dashboard configuration files for:
- **Operations Dashboard**: Real-time monitoring for operations teams
- **Executive Dashboard**: High-level KPIs for business leaders
- **Analyst Dashboard**: Deep-dive analytics for data teams