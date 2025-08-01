# News Query Processor

A Flask-powered news API and CLI tool that:
1. **Ingests** a JSON dump of news articles into MySQL (with full-text search and category tables).  
2. **Serves** endpoints for querying by category, score, keywords (full-text), source and geographic proximity.  
3. **CLI “main”** that takes a user’s natural-language query, extracts intent/entity with OpenAI, calls the API, then enriches each article with a 2–3 sentence LLM summary.


---

## Features

- **Full-text search** across article titles and descriptions  
- **Category**, **score**, **source**, **nearby** (Haversine) filters  
- **OpenAI**-powered intent/entity extraction  
- **Automated LLM summaries** for each returned article  

---

## Prerequisites

- Python 3.8+  
- MySQL server  
- An OpenAI API key  

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Fawaaz16/Contextual-News-Data-Retrieval-System.git