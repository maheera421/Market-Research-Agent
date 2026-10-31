from app.clients.llm_client import run_agent
from app.schemas import Finding

TOPICS = [
    "most common customer complaints in app store and online reviews",
    "most common customer praise in app store and online reviews",
    "complaints specifically about delivery time or rider reliability",
    "complaints specifically about customer support or refund handling",
]


def run(competitor: str, market_context: str) -> list[Finding]:
    findings = []
    for topic in TOPICS:
        system_prompt = f"""You are a Customer Sentiment research agent.
You research recurring themes in customer feedback for one specific competitor,
in the context of a company evaluating whether to enter: {market_context}."""

        user_prompt = f"Research {competitor}'s {topic}. Find one specific, sourced fact."

        findings.append(run_agent(system_prompt, user_prompt, Finding))
    return findings
