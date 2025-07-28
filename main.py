import os, re
from openai import OpenAI
from utils import get_by_category, get_by_score, search_articles, get_by_source, get_nearby


api_key = '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'

# openai.api_key = os.getenv("OPENAI_KEY")
# openai.api_key = os.getenv("OS")

client = OpenAI(api_key=api_key)

# user_query = input()
# prompt = "Give me a the list of entities and intents from the query " + user_query + " . Format of the output: First line of the output should contain entities and the second line should contain Intent. Intent can be one of category, score, search, source, nearby, trending."


def parse_input(input_str):
    # Extract entities
    entities_match = re.search(r"Entities:\s*(.+)", input_str, re.IGNORECASE)
    entities = []
    if entities_match:
        entities = [e.strip() for e in entities_match.group(1).split(",")]

    # Extract intent description
    intent_match = intent_match = re.search(r"Intent:\s*(.+)", input_str, re.IGNORECASE)
    intent_description = intent_match.group(1) if intent_match else ""

    # Simple keyword-based intent classification
    detected_intent = "search"  # default intent
    if "near" in intent_description.lower():
        detected_intent = "nearby"
    elif "category" in intent_description.lower():
        detected_intent = "category"
    elif "score" in intent_description.lower():
        detected_intent = "score"
    elif "source" in intent_description.lower():
        detected_intent = "source"
    elif "trend" in intent_description.lower():
        detected_intent = "trending"

    return entities, detected_intent


# response = client.chat.completions.create(
#     model="gpt-4o-mini",    # Low-cost model
#     messages=[
#         {"role": "user", "content": prompt}
#     ]
# )

# result = response.choices[0].message.content
# print("AI Response:\n", result)

input = """Entities: Elon Musk, Twitter acquisition, Palo Alto
Intent: nearby"""

entities, intent = parse_input(input)

# Output as required
print(f"entities: {entities}")
print(f"Intent: {intent}")

print("Category=Technology ->", get_by_category('Technology'))
# print("Score>=0.7 ->", get_by_score(0.7))
# print("Search 'Elon Musk' ->", search_articles('Elon Musk'))
# print("Source='New York Times' ->", get_by_source('New York Times'))
# print("Nearby (37.422, -122.084, 10km) ->", get_nearby(37.4220, -122.0840, 10))