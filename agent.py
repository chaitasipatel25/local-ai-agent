from ollama import chat

MODEL = "qwen3:8b"
MAX_STEPS = 5


def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely."""
    import ast
    import operator

    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Unsupported arithmetic expression")

    tree = ast.parse(expression, mode="eval")
    return str(evaluate(tree))


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
