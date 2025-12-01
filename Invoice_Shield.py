from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.agents import BaseAgent, LoopAgent
from google.adk.tools import Tool
from google.genai.types import EventActions



RETRY_CONFIG = {"max_retries": 2, "backoff_seconds": 1}

# Tools (Interfaces / Stubs)
db_connector = Tool(name="db_connector")
bank_api_tool = Tool(name="bank_api_tool")
vendor_watchlist = Tool(name="vendor_watchlist")
save_report_to_file = Tool(name="save_report_to_file")
send_notification = Tool(name="send_notification")

# Research Agent
research_agent = Agent(
    name="research_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="""
    Research Agent that gathers information related to:
    - invoice fraud patterns
    - regulatory compliance
    - vendor risk behaviors
    - anomaly heuristics and ML feature recommendations
    """,
    instruction="""
    Produce structured intelligence for fraud detection:
    - Key fraud indicators
    - Deterministic rules
    - ML features
    - Vendor risk signals
    Provide all output as JSON including citations.
    """,
    tools=[vendor_watchlist]
)

# Data Ingestion Agent
data_ingest_agent = Agent(
    name="data_ingest_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Normalizes ERP, invoice, vendor and bank data into a canonical format.",
    instruction="""
    Ingest all provided invoice feeds, sanitize formats, unify fields, and export canonical JSON entries.
    """,
    tools=[db_connector, bank_api_tool]
)

# Validation Checker
class AnomalyValidationChecker(BaseAgent):
    def __init__(self, threshold=0.75):
        super().__init__(name="AnomalyValidationChecker")
        self.threshold = threshold

    def run(self, context):
        score = context.get("anomaly_score", 0.0)
        if score >= self.threshold:
            return EventActions(escalate=True, message="Validated")
        return None

# Anomaly Detector (LoopAgent)
anomaly_detector = LoopAgent(
    name="anomaly_detector",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Detects anomalies using heuristics + ML and validates confidence via LoopAgent.",
    loop_body_agent=Agent(
        name="anomaly_detector_iteration",
        model=Gemini(model="gemini-2.5-flash-lite"),
        description="Single iteration of scoring and anomaly detection."
    ),
    validation_checker=AnomalyValidationChecker(threshold=0.75),
    tools=[research_agent, db_connector]
)

# Reconciliation Agent
reconciliation_agent = Agent(
    name="reconciliation_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Matches invoices to payments and creates exception cases.",
    instruction="""
    Perform exact and fuzzy invoice-payment matches. Produce:
    - match_confidence 
    - matched/unmatched status
    - evidence summary
    """,
    tools=[db_connector, bank_api_tool]
)

# Investigation Agent 
investigation_agent = Agent(
    name="investigation_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Creates human-friendly case files for suspicious invoices.",
    instruction="""
    Produce a Markdown case report including:
    - summary of issue
    - evidence list
    - risk rating
    - recommended actions
    Save report and notify reviewers.
    """,
    tools=[save_report_to_file, send_notification]
)

# Communications Agent
comms_agent = Agent(
    name="comms_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Generates notifications and audit reports.",
    instruction="Create short alerts for teams and long-form audit reports."
)

#  Main Orchestrator 
interactive_finops_agent = Agent(
    name="interactive_finops_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Coordinates the entire InvoiceShield workflow end-to-end.",
    instruction="""
    Run full pipeline:
    1. Ingest data
    2. Conduct research
    3. Perform anomaly detection (LoopAgent)
    4. Reconcile payments
    5. Create investigation case
    6. Send audit reports & notifications
    Always include evidence bundles and ensure auditability.
    """,
    sub_agents=[
        data_ingest_agent,
        research_agent,
        anomaly_detector,
        reconciliation_agent,
        investigation_agent,
        comms_agent
    ],
    tools=[db_connector, bank_api_tool, save_report_to_file, send_notification]
)
