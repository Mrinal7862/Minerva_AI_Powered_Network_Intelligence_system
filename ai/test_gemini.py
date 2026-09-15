from .gemini_client import ask_gemini

response = ask_gemini(
        "In one sentence, explain what a knowledge graph is."
)

print(response)