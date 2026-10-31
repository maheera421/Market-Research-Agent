from app.clients.llm_client import run_agent
from app.schemas import Finding

TOPICS = [
    "pricing and commission structure charged to restaurants",
    "feature set and app capabilities",
    "service coverage and geographic reach",
    "recent product changes or updates",
]


def run(competitor: str, market_context: str) -> list[Finding]:
    findings = []
    for topic in TOPICS:
        system_prompt = f"""You are a Competitor Intelligence research agent.
You research one specific aspect of a competitor at a time, in the context of
a company evaluating whether to enter: {market_context}."""

        user_prompt = f"Research {competitor}'s {topic}. Find one specific, sourced fact."

        findings.append(run_agent(system_prompt, user_prompt, Finding))
    return findings
