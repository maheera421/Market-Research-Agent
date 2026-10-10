from app.clients.llm_client import run_agent
from app.schemas import Finding

TOPICS = [
    "recent funding rounds or investment news",
    "recent market expansion or new service launches",
    "recent partnerships or acquisitions",
    "recent controversies, incidents, or regulatory actions",
]


def run(competitor: str, market_context: str) -> list[Finding]:
    findings = []
    for topic in TOPICS:
        system_prompt = f"""You are a News & Events research agent.
You research recent, time-sensitive developments for one specific competitor,
in the context of a company evaluating whether to enter: {market_context}."""

        user_prompt = f"Research {competitor}'s {topic}. Find one specific, sourced, recent fact."

        findings.append(run_agent(system_prompt, user_prompt, Finding))
    return findings
