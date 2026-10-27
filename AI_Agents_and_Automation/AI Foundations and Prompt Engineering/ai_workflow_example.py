"""
1: Simple AI Workflow Example

This example demonstrates a small workflow that resembles a real
AI automation system.

Workflow:

1. Receive a customer message
2. Validate the message
3. Classify the message
4. Select a response template
5. Decide whether human approval is needed
6. Produce a final workflow result

This example intentionally uses simple rules instead of an external AI API.
That keeps the learning example easy to run and understand.

In a later topic, the classification step can be replaced by an LLM call.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal
import json


Category = Literal["billing", "technical", "account", "general"]
Priority = Literal["low", "medium", "high"]


@dataclass
class WorkflowInput:
    customer_id: str
    message: str


@dataclass
class Classification:
    category: Category
    priority: Priority
    confidence: float


@dataclass
class WorkflowResult:
    customer_id: str
    category: Category
    priority: Priority
    confidence: float
    suggested_reply: str
    requires_human_approval: bool


def validate_input(workflow_input: WorkflowInput) -> None:
    """Validate incoming data before processing it."""

    if not workflow_input.customer_id.strip():
        raise ValueError("customer_id cannot be empty.")

    if not workflow_input.message.strip():
        raise ValueError("message cannot be empty.")

    if len(workflow_input.message) > 5_000:
        raise ValueError("message is too long.")


def classify_message(message: str) -> Classification:
    """
    Simple rule-based classifier.

    This function represents the location where an AI model could later
    be integrated.
    """

    normalized = message.lower()

    billing_words = {
        "charged",
        "invoice",
        "payment",
        "refund",
        "subscription",
        "billing",
    }

    technical_words = {
        "error",
        "bug",
        "crash",
        "broken",
        "not working",
        "server",
        "failed",
    }

    account_words = {
        "password",
        "login",
        "account",
        "verification",
        "sign in",
    }

    if any(word in normalized for word in billing_words):
        priority: Priority = "high" if "charged twice" in normalized else "medium"
        return Classification(
            category="billing",
            priority=priority,
            confidence=0.90,
        )

    if any(word in normalized for word in technical_words):
        return Classification(
            category="technical",
            priority="high",
            confidence=0.85,
        )

    if any(word in normalized for word in account_words):
        return Classification(
            category="account",
            priority="medium",
            confidence=0.80,
        )

    return Classification(
        category="general",
        priority="low",
        confidence=0.55,
    )


def create_reply(classification: Classification) -> str:
    """Create a safe response template based on classification."""

    replies = {
        "billing": (
            "Thank you for contacting us. We will review your billing details "
            "and investigate the payment issue."
        ),
        "technical": (
            "Thank you for reporting this technical problem. Our technical "
            "team will investigate the issue."
        ),
        "account": (
            "We can help with your account issue. Please follow the approved "
            "account recovery process."
        ),
        "general": (
            "Thank you for contacting us. A support representative will review "
            "your request."
        ),
    }

    return replies[classification.category]


def requires_human_approval(classification: Classification) -> bool:
    """
    Decide whether a human should review the result.

    Human approval is useful when:

    - The priority is high
    - The confidence is low
    - The workflow could cause a financial or operational action
    """

    if classification.priority == "high":
        return True

    if classification.confidence < 0.70:
        return True

    return False


def run_workflow(workflow_input: WorkflowInput) -> WorkflowResult:
    """Run the complete customer-message workflow."""

    validate_input(workflow_input)

    classification = classify_message(workflow_input.message)
    reply = create_reply(classification)
    approval_required = requires_human_approval(classification)

    return WorkflowResult(
        customer_id=workflow_input.customer_id,
        category=classification.category,
        priority=classification.priority,
        confidence=classification.confidence,
        suggested_reply=reply,
        requires_human_approval=approval_required,
    )


def main() -> None:
    example_input = WorkflowInput(
        customer_id="customer-1001",
        message="I was charged twice for my subscription.",
    )

    result = run_workflow(example_input)

    print(json.dumps(asdict(result), indent=2))

    if result.requires_human_approval:
        print("\nHuman approval is required before sending or applying an action.")
    else:
        print("\nThe workflow can continue automatically.")


if __name__ == "__main__":
    main()
