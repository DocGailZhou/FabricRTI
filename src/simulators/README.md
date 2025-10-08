# Data Simulators

This folder contains Jupyter notebooks that generate realistic data for the RTI solution accelerator.

## Simulators

### 📱 clickstream_simulator.ipynb
- **Source**: Based on RTI-Hackathon Clickstream Simulator
- **Data Generated**: E-commerce user interactions, page views, cart activities
- **Event Types**: Product clicks, add to cart, purchases, session tracking, anomaly spikes
- **Output**: JSON events streamed to EventStream endpoints

### 🏭 manufacturing_simulator.ipynb  
- **Source**: Based on RTI-Hackathon Manufacturing Simulator
- **Data Generated**: Production line telemetry, equipment metrics, quality measurements
- **Event Types**: Temperature readings, vibration data, defect probabilities, operator activities
- **Output**: JSON telemetry streamed to EventStream endpoints

### 🚚 shipping_simulator.ipynb
- **Source**: Based on RTI-Hackathon Shipping Simulator  
- **Data Generated**: Logistics events, shipment tracking, delivery status updates
- **Event Types**: Package movements, delivery confirmations, transit delays, location updates
- **Output**: JSON events streamed to EventStream endpoints

## Usage

1. Open each `.ipynb` file in your preferred Jupyter environment
2. Configure the EventStream endpoint URLs in each notebook
3. Run the simulators to generate continuous data streams
4. Monitor the data ingestion in your `fabrikam_eventhouse` EventHouse

## Requirements

- Python 3.8+
- Jupyter Notebook or VS Code with Jupyter extension
- Required packages: requests, pandas, numpy, datetime, json, time