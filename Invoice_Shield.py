from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.agents import BaseAgent, LoopAgent
from google.adk.tools import Tool
from google.genai.types import EventActions

RETRY_CONFIG = {"max_retries": 2, "backoff_seconds": 1}

google_search = Tool(name="google_search")

research_agent = Agent(
    name="research_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Researches invoice fraud patterns, compliance rules, vendor behaviors, and anomaly heuristics using google_search.",
    instruction="""
    Use google_search to gather intelligence on:
    - invoice fraud indicators
    - regulatory compliance expectations
    - vendor risk signals
    - common anomaly patterns
    Output should be structured JSON with references.
    """,
    tools=[google_search]
)

data_ingest_agent = Agent(
    name="data_ingest_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Normalizes incoming invoice data into a unified format.",
    instruction="""
    Take any provided invoice or ERP-like data and convert it into a canonical JSON structure.
    Ensure fields are cleaned, standardized, and consistent.
    """,
    tools=[]
)

class AnomalyValidationChecker(BaseAgent):
    def __init__(self, threshold=0.75):
        super().__init__(name="AnomalyValidationChecker")
        self.threshold = threshold

    def run(self, context):
        score = context.get("anomaly_score", 0.0)
        if score >= self.threshold:
            return EventActions(escalate=True, message="Validated")
        return None

anomaly_detector = LoopAgent(
    name="anomaly_detector",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Performs anomaly scoring using heuristics and ML-like reasoning.",
    loop_body_agent=Agent(
        name="anomaly_detector_iteration",
        model=Gemini(model="gemini-2.5-flash-lite"),
        description="Single iteration of anomaly scoring."
    ),
    validation_checker=AnomalyValidationChecker(threshold=0.75),
    tools=[research_agent]
)

reconciliation_agent = Agent(
    name="reconciliation_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Matches invoices to payments and identifies mismatches.",
    instruction="""
    Compare invoice amounts, vendor names, dates, and reference IDs with provided payment data.
    Output:
    - matched or unmatched
    - confidence score
    - short explanation
    """,
    tools=[]
)

investigation_agent = Agent(
    name="investigation_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Creates a human-readable case summary for suspicious invoices.",
    instruction="""
    Compile a Markdown report with:
    - summary of issue
    - risk explanation
    - anomaly evidence
    - recommended next steps
    """,
    tools=[]
)

comms_agent = Agent(
    name="comms_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Generates notification-style summaries and audit messages.",
    instruction="Produce short alerts and long-form communication summaries."
)

interactive_finops_agent = Agent(
    name="interactive_finops_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=RETRY_CONFIG),
    description="Coordinates the full InvoiceShield workflow.",
    instruction="""
    Execute the full pipeline:
    1. Ingest invoice data
    2. Run research_agent
    3. Perform anomaly detection using LoopAgent
    4. Reconcile invoice with payment info
    5. Generate investigation summary
    6. Produce communication outputs
    """,
    sub_agents=[
        data_ingest_agent,
        research_agent,
        anomaly_detector,
        reconciliation_agent,
        investigation_agent,
        comms_agent
    ],
    tools=[google_search]
)
