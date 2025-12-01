InvoiceShield – Multi-Agent AI System .
An automated AI workflow that detects invoice fraud, analyzes anomalies, and generates investigation reports using a coordinated team.

The Google Agent Development Kit (ADK) was used to create the multiagent AI system known as InvoiceShield.  
Invoice processing processes like ingestion, research, anomaly identification, reconciliation, investigation, and communication are all automated.

This project shows how ADK agents, LoopAgents, and validation logic may be used to represent enterprise-style financial procedures.



 Features

 uses AI and a vendor watchlist tool to normalize and ingest invoice data and investigate fraud trends.  
 uses a LoopAgent with validation to find anomalies  
 compares payments to invoices  
 produces reports from investigations  
 generates summary of notifications  
 Completely coordinated by a single primary agent  



 The Architecture of Agents

 1. data_ingest_agent
creates a uniform structure for vendor, bank, ERP, and invoice data.

 2. Research Agent
uses the vendor watchlist tool to collect trends about invoice fraud, compliance, vendor risk, and anomaly heuristics.

Third. anomaly_detector (LoopAgent)
iteratively scores anomalies until the results are approved by the `AnomalyValidationChecker`.

Four. reconciliation_agent
finds exceptions and simulates linking invoices to payments.

Fifth. investigation_agent
generates Markdown investigation case files that include suggested actions and risk assessments.

Sixth. communications_agent
produces audit-style communication outputs and final alarms.

Seven. interactive_finops_agent
the primary orchestrator that manages the entire six-step workflow.



🛠️ Utilized Technology

Agent Development Kit (ADK) from Google
Models of Gemini (2.5 Flash Lite)
ValidationChecker + LoopAgent
Python
