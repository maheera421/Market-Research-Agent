import json

from groq import BadRequestError, Groq
from pydantic import BaseModel, ValidationError

from app import config
from app.clients.search_client import search

_client = Groq(api_key=config.GROQ_API_KEY)

_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search the web for current information. Use this whenever you need facts, figures, or sources you don't already have.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."}
            },
            "required": ["query"],
        },
    },
}

MAX_TOOL_ITERATIONS = 5
MAX_VALIDATION_RETRIES = 2


def run_agent(system_prompt: str, user_prompt: str, response_model: type[BaseModel]) -> BaseModel:
    schema_note = (
        "\n\nYour final answer must be valid JSON matching this schema, with no other text:\n"
        f"{response_model.model_json_schema()}"
    )
    messages = [
        {"role": "system", "content": system_prompt + schema_note},
        {"role": "user", "content": user_prompt},
    ]

    for _ in range(MAX_TOOL_ITERATIONS):
        try:
            response = _client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=messages,
                tools=[_SEARCH_TOOL],
                tool_choice="auto",
            )
        except BadRequestError:
            # Model emitted a malformed tool call (open-weight models occasionally
            # do this). Stop searching and answer with whatever was gathered so far.
            break
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            results = search(args["query"])
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(results),
                }
            )
    # If the loop runs out of iterations without the model stopping on its own,
    # fall through and force a final answer with whatever was gathered so far.

    messages.append(
        {
            "role": "user",
            "content": "Now give your final answer as JSON matching the schema above. Do not call any tools.",
        }
    )

    for attempt in range(MAX_VALIDATION_RETRIES + 1):
        response = _client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        try:
            return response_model.model_validate_json(content)
        except ValidationError as e:
            if attempt == MAX_VALIDATION_RETRIES:
                raise
            messages.append({"role": "assistant", "content": content})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "That output didn't match the required schema. "
                        f"Error: {e}\nRespond again with ONLY corrected valid JSON."
                    ),
                }
            )
