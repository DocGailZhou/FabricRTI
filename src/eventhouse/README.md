# EventHouse KQL Scripts

This folder contains KQL scripts for setting up and managing the EventHouse database.

## Scripts

### 📋 table_creation.kql
- Creates all required tables for the RTI solution
- Sets up JSON ingestion mappings for streaming data
- Configures data retention policies (30d/90d/12m)
- Enables streaming ingestion policies

### 🔍 anomaly_detection.kql
- KQL queries for real-time anomaly detection
- 60-day moving window baseline calculations
- Statistical analysis (Z-scores, percentiles)
- Multi-level severity classification

### ✅ data_validation.kql
- Data quality validation queries
- Ingestion monitoring and health checks
- Table statistics and row counts
- Schema validation queries

## Usage

1. Open your `fabrikam_eventhouse` in Microsoft Fabric
2. Navigate to the Query tab (KQL query interface)
3. Copy and paste the content from each .kql file
4. Execute the scripts in order: table_creation → data_validation → anomaly_detection

## EventHouse Details

- **EventHouse Name**: fabrikam_eventhouse
- **Database Name**: fabrikam_eventhouse
- **Tables Created**: 7 tables (3 main + 3 reference + 1 anomaly results)