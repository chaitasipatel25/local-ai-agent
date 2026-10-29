# Local AI Agent

Build and run a simple AI agent locally using Python, Ollama, and an open-weight language model.

This project is designed for developers who want to understand how an LLM can call tools, receive their results, and use those results to complete a task—all without relying on a hosted model API.

## What you'll learn

- How to run a local language model with Ollama
- How to connect an LLM to Python functions
- How tool calling works in an agent loop
- How to return tool results to the model
- How to limit agent execution with a maximum step count
- How to evaluate basic arithmetic expressions without using `eval()`

## Architecture

```mermaid
flowchart TD
    A[User task] --> B[Local LLM via Ollama]
    B --> C{Request a tool?}
    C -->|Yes| D[Python calculate tool]
    D --> E[Return tool result]
    E --> B
    C -->|No| F[Final response]
