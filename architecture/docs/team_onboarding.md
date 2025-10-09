# Team Onboarding Guide: Microsoft Fabric Real-Time Intelligence (RTI)

## Welcome to the RTI Solution Accelerator Project! 👋

This guide provides concept-focused educational materials to get your team up to speed with Microsoft Fabric Real-Time Intelligence. Whether you're new to Fabric or coming from Power BI, this guide will help you understand the key concepts and components we'll be working with.

---

## 🎯 What is Real-Time Intelligence?

**Real-Time Intelligence (RTI)** is Microsoft Fabric's end-to-end solution for event-driven scenarios, streaming data, and data logs. Think of it as a complete platform that handles everything from data ingestion to visualization and automated actions - all in real-time.

**Key Concept**: Unlike traditional batch processing (where you process data every hour/day), RTI processes data **as it flows** - enabling immediate insights and actions.

### 📚 Essential Reading
- [What is Real-Time Intelligence?](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview) - Complete overview and concepts
- [RTI vs Other Azure Solutions](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/real-time-intelligence-compare) - How RTI compares to other services

---

## 🏗 Core RTI Components (Our Architecture Building Blocks)

### 1. **EventStream** - The Data Pipeline
**What it is**: Captures, transforms, and routes high volumes of real-time events with no-code experience.
**Think of it as**: A smart conveyor belt that can clean, sort, and route your data as it flows.

**Key Features**:
- No-code data transformation
- Content-based routing (send different data to different places)
- Multiple source and destination connectors

📚 **Learn More**: [What is EventStream?](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)

### 2. **EventHouse** - The Fast Database
**What it is**: A high-performance analytics database optimized for time-based data.
**Think of it as**: A supercharged database that's built specifically for analyzing streaming data.

**Key Features**:
- **Multiple KQL Databases**: Our project uses `clickstream_db`, `manufacturing_db`, and `shipping_db`
- **Automatic indexing and partitioning** by time
- **Lightning-fast queries** using KQL (Kusto Query Language)

📚 **Learn More**: [EventHouse Overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse)

### 3. **Activator** - The Smart Alert System
**What it is**: Monitors data and automatically triggers actions when conditions are met.
**Think of it as**: A smart security system for your data - it watches for patterns and takes action.

**Examples**: Send email when temperature is too high, trigger a workflow when orders spike.

📚 **Learn More**: [What is Activator?](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction)

### 4. **RTI Dashboards** - Real-Time Visualization
**What it is**: Dashboards that update in real-time (sub-second refresh rates).
**Think of it as**: Like Power BI dashboards, but for data that's constantly changing.

### 5. **Fabric Data Agent** - Natural Language Queries
**What it is**: Chat interface that lets business users ask questions in plain English.
**Think of it as**: "Hey Siri" for your data - ask questions naturally and get instant answers.

---

## 🧠 Key Concepts to Understand

### Event-Driven vs Schedule-Driven
- **Schedule-Driven**: "Run this report every morning at 9 AM"
- **Event-Driven**: "Alert me the moment temperature exceeds 30°C"

### KQL (Kusto Query Language)
**What it is**: The query language for EventHouse - like SQL but optimized for time-series data.
**Good news**: If you know SQL, KQL concepts will feel familiar.

📚 **Get Started**: 
- [KQL Overview](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/index?context=/fabric/context/context&pivots=fabric)
- [Write Your First KQL Query - Training](https://learn.microsoft.com/en-us/training/modules/write-first-query-kusto-query-language/)

### Streaming Data
**What it is**: Data that flows continuously (like a river) vs batch data (like filling buckets).
**Examples**: Sensor readings, website clicks, transaction logs, IoT device data.

---

## 🎓 Learning Path & Training

### For Everyone (Start Here)
1. **[Get Started with RTI in Fabric - Training Module](https://learn.microsoft.com/en-us/training/modules/get-started-kusto-fabric/)**
   - 45 minutes
   - Covers all core concepts
   - Hands-on exercises

### For Technical Team Members
2. **[End-to-End RTI Tutorial](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/tutorial-introduction)**
   - Complete walkthrough with sample data
   - Shows how all components work together

3. **[KQL Training Path](https://learn.microsoft.com/en-us/training/modules/write-first-query-kusto-query-language/)**
   - Learn the query language we'll use daily

### For Power BI Users
**Good news**: Much of your Power BI knowledge applies! RTI integrates seamlessly with Power BI.
- [Create Power BI Reports from RTI Data](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-powerbi-report)

---

## 🏢 Our Project Context

### Our Business Domains
1. **E-commerce** (`clickstream_db`): Customer behavior, cart activities, product views
2. **Manufacturing** (`manufacturing_db`): Equipment telemetry, quality metrics, production data
3. **Shipping** (`shipping_db`): Logistics events, carrier performance, delivery tracking

### Our RTI Architecture
We're building a **pure RTI solution** that:
- Uses data simulators (no external dependencies)
- Stores everything in one EventHouse with three databases
- Provides both technical dashboards and business-friendly natural language queries
- Automatically detects anomalies and sends alerts

---

## 🛠 Practical Skills You'll Develop

### Week 1-2: Foundations
- Understanding RTI concepts and components
- Basic KQL query writing
- Navigating the Fabric RTI interface

### Week 3-4: Implementation
- Creating EventStream configurations
- Building EventHouse tables and schemas
- Setting up Activator rules

### Week 5-6: Analytics & Visualization  
- Advanced KQL for anomaly detection
- Building RTI dashboards
- Configuring cross-database queries

### Week 7-8: Integration & Testing
- End-to-end testing
- Performance optimization
- Documentation and deployment

---

## 🔗 Bookmark These Resources

### Daily Reference
- [RTI Documentation Hub](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/)
- [KQL Reference](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/index?context=/fabric/context/context&pivots=fabric)

### Troubleshooting & Support
- [RTI Monitoring and Logs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/monitor-eventhouse)
- [EventHouse Management](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/manage-monitor-eventhouse)

### Advanced Topics
- [Digital Twin Builder](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/digital-twin-builder/overview) (Preview)
- [RTI with Fabric Notebooks](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/notebooks)

---

## 💡 Success Tips

### For Fabric Beginners
- Start with the training modules - they provide hands-on experience
- Don't worry about memorizing KQL syntax - focus on understanding concepts
- Ask questions during team sessions - RTI concepts build on each other

### For Power BI Users
- RTI Dashboards work similarly to Power BI - many concepts transfer
- KQL is different from DAX, but the analytical thinking is the same
- You can still create Power BI reports on top of RTI data

### For Everyone
- **Think in streams**: Data is flowing, not static
- **Start simple**: Basic queries and dashboards first, then add complexity
- **Use the documentation**: Microsoft's RTI docs are excellent and frequently updated

---

## 🚀 Next Steps

1. **Complete the foundational training** (Week 1)
2. **Review our architecture design document** to understand our specific implementation
3. **Set up your development environment** (we'll do this together)
4. **Start with the RTI tutorial** using sample data before working with our simulators

---

## ❓ Questions & Support

- **Technical Questions**: Post in our team chat or bring to daily standups
- **Concept Clarification**: Microsoft Learn documentation and training modules
- **RTI-Specific Issues**: [Microsoft Fabric Community](https://community.fabric.microsoft.com/)

Remember: This is a learning journey for everyone. The RTI technology is relatively new, so we're all building expertise together! 

---

*Last Updated: October 9, 2025*
*Document Version: 1.0*