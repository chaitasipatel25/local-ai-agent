from ollama import chat
from calculator_tool import calculate

MODEL = "qwen3:8b"
MAX_STEPS = 5


tools = [calculate]

messages = [{
    "role": "user",
    "content": (
        "Use the calculate tool to compute (125 * 8) + 37. "
        "Then explain the result."
    ),
}]

for step in range(MAX_STEPS):
    response = chat(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    messages.append(response.message)
    calls = response.message.tool_calls or []

    if not calls:
        print("\nAgent:", response.message.content)
        break

    for call in calls:
        if call.function.name != "calculate":
            result = "Error: unknown tool"
        else:
            try:
                result = calculate(
                    call.function.arguments["expression"]
                )
            except Exception as exc:
                result = f"Tool error: {exc}"

        print(f"\nTool called: {call.function.name}")
        print(f"Arguments: {call.function.arguments}")
        print(f"Result: {result}")

        messages.append({
            "role": "tool",
            "tool_name": call.function.name,
            "content": str(result),
        })
else:
    print("Stopped: maximum agent steps reached.")
