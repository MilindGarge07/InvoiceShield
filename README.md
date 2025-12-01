InvoiceShield: Google ADK + Gemini MultiAgent AI System

The Google Agent Development Kit (ADK) and Gemini 2.5 Flash Lite were used to create the simple, modular multiagent system known as InvoiceShield.  
Within a coordinated agent pipeline, it automates invoice analysis via ingestion, research, anomaly identification, reconciliation, investigation, and communication.

This approach collects research ideas for fraud and anomaly investigation using a single external tool: google_search.



 Overview of the Project

Businesses deal with thousands of invoices. Manual verification is laborious and prone to mistakes.  
Using a fully orchestrated pipeline, InvoiceShield shows how several AI agents may work together to handle these tedious financial validation chores.

The system is easy to use, scalable, and perfect for instructional demos or Kaggle ADK submissions.


The Architecture of Agents

 1. data_ingest_agent
 cleans and normalizes any incoming ERP-like or invoicing data.
 creates a single JSON structure from all inputs.

 2. Research Agent  
 uses the ONLY tool, google_search.  
 gathers information about: tendencies of invoicing fraud  
   expectations for compliance  
   signs of vendor risk  
   Heuristics for anomalies  

 3. LoopAgent's anomaly_detector
 rates bills for potential irregularities on a regular basis.
 For every loop cycle, a helper agent (`anomaly_detector_iteration`) is used.

 4. Only anomaly scores ≥ 0.75 are approved by AnomalyValidationChecker.
 Reruns are required until a high level of confidence is reached.

 5. reconciliation_agent
 compares payment information with invoice amounts, vendors, dates, and references.
 generates explanations and match confidence.

 6. Investigation Agent
 generates a Markdown-style synopsis of the following: problem, risk, anomalous evidence, suggested actions  

 7. communications_agent
 produces long-form communication messages and summaries in the notification style.

 8. The Main Orchestrator, interactive_finops_agent
oversees the entire pipeline:

1. Consume 2. Investigate  
3. The loop for anomaly detection  
4. Making amends  
5. Summary of the investigation 6. Communication results  



 🔧 Utilized Tools

In the entire project, there is only one tool:

Google Search
used just by research_agent to collect signals and trends in the real world.

No databases.  
No third-party APIs.  
No connectors.  
One tidy research instrument.



 📦 Google ADK (Agent Development Kit) Technologies Employed
 Workflow for Gemini 2.5 Flash Lite Python LoopAgent Validation

