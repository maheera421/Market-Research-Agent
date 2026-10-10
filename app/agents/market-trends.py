from app.clients.llm_client import run_agent
from app.schemas import Finding

TOPICS = [
    "market size and growth rate",
    "regulatory environment and recent regulations affecting the industry",
    "broader industry trends shaping the sector",
    "competitive intensity and market concentration",
]


def run(competitor: str, market_context: str) -> list[Finding]:
    findings = []
    for topic in TOPICS:
        system_prompt = f"""You are a Market & Industry Trends research agent.
You research the broader market conditions relevant to a company evaluating
whether to enter and compete with {competitor} in: {market_context}."""

        user_prompt = f"Research the {topic} for: {market_context}. Find one specific, sourced fact."

        findings.append(run_agent(system_prompt, user_prompt, Finding))
    return findings
