# Day 1: AI Foundations and Prompt Engineering

## Overview

This module introduces the basic concepts behind modern AI applications, especially applications powered by Large Language Models, commonly called LLMs.

The goal is not only to learn how to ask questions to an AI model, but also to understand how to design reliable AI workflows.

This topic covers:

- What Large Language Models are
- How prompts influence model behavior
- System, user, and assistant messages
- Context and instructions
- Prompt templates
- Structured outputs
- Input validation
- Basic AI workflow design
- Limitations of language models
- Common mistakes when building AI applications

## Why This Topic Matters

Modern software engineering is increasingly using AI for:

- Code generation
- Document summarization
- Customer support
- Data extraction
- Report generation
- Search systems
- Workflow automation
- Decision support
- Software testing
- Data analysis

However, an AI model should not be treated as a perfect source of truth.

A reliable AI application needs:

1. Clear instructions
2. Well-defined input data
3. Output validation
4. Error handling
5. Logging
6. Human review for important decisions

## Files in This Module

```text
Day-18-AI-Foundations-and-Prompt-Engineering/
├── README.md
├── llm_theory_and_prompting.md
├── structured_output_demo.py
├── ai_workflow_example.py
└── common_mistakes_and_best_practices.txt
```

## Learning Objectives

After completing this module, you should be able to:

- Explain what an LLM does at a high level
- Write clear prompts
- Separate instructions from user data
- Create reusable prompt templates
- Request structured outputs
- Validate AI-generated data
- Build a simple AI-style workflow
- Understand why AI output must be checked before use

## Running the Examples

The Python examples use only the standard library.

```bash
python structured_output_demo.py
```

```bash
python ai_workflow_example.py
```

## Important Principle

An AI model can produce convincing but incorrect information.

Therefore:

```text
AI output is an input to your software system, not automatically the final truth.
```

## Next Topic

The next topic will cover how to connect applications to LLM APIs and how to safely handle structured JSON responses.
