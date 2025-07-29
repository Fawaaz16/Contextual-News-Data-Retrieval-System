import os, re
from openai import OpenAI
from utils import parse_intent_entity, get_by_category, get_by_score, search_articles, get_by_source, get_nearby


api_key = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=api_key)

user_query = input("Enter the user query: ")

prompt = "Given the user query: " + user_query + " ,extract from a user's query:\
1. The user's most appropriate intent (one of: category, score, search, source, nearby, trending).  \
2. The single entity in the query that corresponds to that intent. Format your answer as:  <intent>:<entity> \
intent should have no capital letters. \
There is an exception to the format of the output, if the intent is nearby, there are two cases possible \
1. If the user specifies the coordinates of the nearby area, extract lat, log of the user and radius from the user query. \
2. If the user does not specify the coordinates(), but specifies the nearby area, in that case, use the coordinates of that area. \
and the format of the answer is <intent>:<lat>,<lon>,<radius>."



response = client.chat.completions.create(
    model="gpt-4o-mini",    # Low-cost model
    messages=[
        {"role": "user", "content": prompt}
    ]
)

result = response.choices[0].message.content

input = result
# input = "nearby: 16.894328,80.505096,50"
# input = "category: Technology"
# input = "source: Hindustan Times"
# input = "score: 0.95"

intent, entity = parse_intent_entity(input)

if intent == "nearby":
    lat, lon, radius = entity[0], entity[1], entity[2]

print(f"entity: {entity}")
print(f"Intent: {intent}")


if intent == "category":
    news_feed = get_by_category(entity)
elif intent == "score":
    news_feed = get_by_score(entity)
elif intent == "search":
    news_feed = search_articles(entity)
elif intent == "source":
    news_feed = get_by_source(entity)
elif intent == "nearby":
    news_feed = get_nearby(lat, lon, radius)
else:
    raise ValueError(f"Unknown intent: {intent}")

for i in range(len(news_feed)):
    enrichment_prompt = f"""
    You are an AI that summarizes articles based only on their title and description.
    Given the following information:

    Title: {news_feed[i]['title']}
    Description: {news_feed[i]['description']}

    Provide a concise, clear summary of what the article is likely about in 2-3 sentences.
    Just return the 2-3 line summary as response, without any heading or any sort of thing.
    """

    llm_generated_response = client.chat.completions.create(
        model="gpt-4o-mini",    # Low-cost model
        messages=[
            {"role": "user", "content": enrichment_prompt}
        ]
    )

    llm_generated_summary = llm_generated_response.choices[0].message.content
    news_feed[i]['llm_generated_summary'] = llm_generated_summary

print(news_feed)