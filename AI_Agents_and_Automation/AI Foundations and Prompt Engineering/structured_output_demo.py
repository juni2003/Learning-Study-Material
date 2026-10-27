"""
Day 1: Structured Output Demo

This example demonstrates how to:

1. Build a reusable prompt
2. Simulate an AI response
3. Parse JSON from the response
4. Validate the result
5. Convert unreliable text into predictable application data

The example uses a fake model so it can run without an API key.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class SupportTicket:
    """Validated representation of a support ticket."""

    category: str
    priority: str
    summary: str
    suggested_action: str


ALLOWED_CATEGORIES = {
    "billing",
    "technical",
    "account",
    "feedback",
    "other",
}

ALLOWED_PRIORITIES = {
    "low",
    "medium",
    "high",
}


def build_classification_prompt(ticket_text: str) -> str:
    """
    Build a prompt that requests a predictable JSON response.
    """

    return f"""
You are a support-ticket classification assistant.

Classify the customer message below.

Allowed categories:
- billing
- technical
- account
- feedback
- other

Allowed priorities:
- low
- medium
- high

Return only valid JSON with exactly these fields:

{{
  "category": "one allowed category",
  "priority": "one allowed priority",
  "summary": "short summary",
  "suggested_action": "recommended next action"
}}

Customer message:
{ticket_text}
""".strip()


def fake_model(prompt: str) -> str:
    """
    Simulate an AI model response.

    In a real application, this function would call an AI provider.
    The rest of the workflow should remain similar:

        prompt -> model -> parse -> validate -> use
    """

    if "charged twice" in prompt.lower():
        return json.dumps(
            {
                "category": "billing",
                "priority": "high",
                "summary": "The customer reports being charged twice.",
                "suggested_action": "Review the payment record and issue a refund if appropriate.",
            }
        )

    return json.dumps(
        {
            "category": "other",
            "priority": "medium",
            "summary": "The customer submitted a general support request.",
            "suggested_action": "Review the request and route it to the correct team.",
        }
    )


def parse_json_response(raw_response: str) -> dict[str, Any]:
    """
    Parse a model response as JSON.

    This intentionally fails loudly when the response is invalid.
    Silent failures can create dangerous downstream behavior.
    """

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise ValueError("The model did not return valid JSON.") from error

    if not isinstance(parsed, dict):
        raise ValueError("The model response must be a JSON object.")

    return parsed


def validate_ticket(data: dict[str, Any]) -> SupportTicket:
    """
    Validate model-generated fields before application code uses them.
    """

    required_fields = {
        "category",
        "priority",
        "summary",
        "suggested_action",
    }

    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise ValueError(f"Missing required fields: {sorted(missing_fields)}")

    category = data["category"]
    priority = data["priority"]
    summary = data["summary"]
    suggested_action = data["suggested_action"]

    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    if priority not in ALLOWED_PRIORITIES:
        raise ValueError(f"Invalid priority: {priority}")

    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("Summary must be a non-empty string.")

    if not isinstance(suggested_action, str) or not suggested_action.strip():
        raise ValueError("Suggested action must be a non-empty string.")

    return SupportTicket(
        category=category,
        priority=priority,
        summary=summary.strip(),
        suggested_action=suggested_action.strip(),
    )


def classify_support_ticket(ticket_text: str) -> SupportTicket:
    """
    Complete AI-style pipeline:

    1. Build prompt
    2. Generate response
    3. Parse JSON
    4. Validate result
    """

    if not ticket_text.strip():
        raise ValueError("Ticket text cannot be empty.")

    prompt = build_classification_prompt(ticket_text)
    raw_response = fake_model(prompt)
    parsed_response = parse_json_response(raw_response)

    return validate_ticket(parsed_response)


def main() -> None:
    ticket_text = (
        "I was charged twice for my subscription this month. "
        "Please help me get one of the charges refunded."
    )

    prompt = build_classification_prompt(ticket_text)
    result = classify_support_ticket(ticket_text)

    print("Generated prompt:")
    print("-" * 60)
    print(prompt)

    print("\nValidated result:")
    print("-" * 60)
    print(json.dumps(result.__dict__, indent=2))


if __name__ == "__main__":
    main()
