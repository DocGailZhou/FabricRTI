**Prompt 1** 

My team has published a new solution accelerator as GitHub repo:  [microsoft/unified-data-foundation-with-fabric-solution-accelerator: Unified Data Foundation with Microsoft Fabric with Options to Integrate with Azure Databricks and Microsoft Purview](https://github.com/microsoft/unified-data-foundation-with-fabric-solution-accelerator)

We have a Fabric workspace set up for this solution. 

We have developed azd up deployment code that can be reused. 

Now we want to build on top of this solution. Not sure if I can leverage the medallion architecture which stores and processes data in these domain: customer, product, sales, and finance. And the data processing is more batch oriented and sequenced, table by table. 

Now we are going to develop a new solution accelerator using Microsoft Fabric RTI, EventStream, EventHouse, Activator, RTI dashboards. Some team members are new to Microsoft Fabric, some team members have Fabric experience but not RTI. We also need to generate some sample data

We are given some resources: 

[RTI-Hackathon/Data Simulators/Clickstream Simulator.ipynb at main · L400-RTI/RTI-Hackathon](https://github.com/L400-RTI/RTI-Hackathon/blob/main/Data Simulators/Clickstream Simulator.ipynb)

We will most likely use the code here to produce sample real time data (with some modifications to produce anomaly data faster and frequent so we can test our application quickly)

[Public Channels - ThingSpeak IoT](https://thingspeak.mathworks.com/channels/public)

Right now I need to develop some ideas and architecture for this solution accelerator. 

I do not need to think about writing code at this moment. I need to elaborate with you on a good architecture and what components I need and how things will be connected. We will use Python for Application Development and KQL for RTI data query. 

Can you help me get started and write a docs/architecture_design.md file to capture the design? 





## 📋 Summary of Your Key Questions

### 1. **Is EventHouse a KQL database? Must have tables created like a SQL DB?**

**YES** - EventHouse is exactly like a SQL database but uses KQL instead of SQL:

- **Tables must be created** with defined schemas using `.create table` commands
- **Data types** are defined (string, datetime, real, int, dynamic, bool)
- **Ingestion mappings** are required to map JSON fields to table columns
- **Indexes and partitions** are automatically managed (time-based partitioning)
- **The data WILL align** with sample data - I've provided exact schemas matching the RTI-Hackathon simulators

### 2. **Python-Based Advanced Analytics: What code do I need? What ML models?**

**Complete implementation provided** in the `implementation_examples.md`:

- **Statistical Anomaly Detection**: Rolling z-score analysis (simple to start)
- **ML Models**: Isolation Forest for multi-dimensional anomaly detection
- **Specific Classes**: `ManufacturingAnomalyDetector`, `ClickstreamAnalyzer`
- **Integration**: Functions to query EventHouse and insert results back
- **Visualization**: Matplotlib/Seaborn charts for investigation
- **All dependencies listed** in requirements.txt

### 3. **Where do I store Activator Rules? Is Activator self-contained?**

**Activator is a standalone Fabric service**:

- **Rules stored**: In the Fabric Portal UI, not in code files
- **Self-contained**: Yes, it's a managed service that monitors EventHouse
- **Configuration**: Through web interface (condition KQL + action definition)
- **Actions**: Email, Teams, webhooks, custom functions
- **State management**: Automatic (prevents spam, tracks rule execution)

### 4. **Do I need both RTI dashboard and Power BI dashboard?**

**YES, both serve different purposes**:

**RTI Dashboards**:

- ⚡ **Real-time** (sub-second latency)
- 🔧 **For operators** and technical teams
- 📊 **KQL-based** queries directly from EventHouse
- 🚨 **Operational monitoring** and alert investigation

**Power BI Dashboards**:

- 📈 **Business intelligence** (minutes/hours latency acceptable)
- 👔 **For executives** and business analysts
- 🏛️ **Combines** RTI + historical medallion architecture data
- 📋 **Strategic insights** and trend analysis

## 🚀 **Next Steps Recommended**

1. **Start with EventHouse setup** - Use the KQL commands in `implementation_examples.md`
2. **Deploy data simulators** - Modify RTI-Hackathon notebooks with your EventStream endpoints
3. **Test basic KQL queries** - Verify data is flowing correctly
4. **Build first Python notebook** - Use the anomaly detection example
5. **Create first Activator rule** - Start with simple temperature threshold
6. **Set up RTI dashboard** - Basic operational monitoring



