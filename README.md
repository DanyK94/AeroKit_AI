# AEROKIT AI
## Project:
16 Week Journey Building an AI-Powered Aviation Tools

## Week 1 - Mini Projects - 14/04 Started
- [x] ICAO Code Lookup CLI
- [X] Flight Status Check
- [X] METAR Parser
- [X] Acronym Explainer
- [X] Airport Info API

## Week 2 - XX - 20/04 Started
- [ ] RAG

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env  # Add your AIRLABS_API_KEY & AVWX_API_KEY & OPENROUTER_API_KEY
python main.py
```

## API
### Start server
```bash
uvicorn main:app --reload 
```
### Call Examples
- http://127.0.0.1:8000/airport/LIRF
- http://127.0.0.1:8000/airport/LIRF/weather
- http://127.0.0.1:8000/airports/search?query=Roma
- 

## Tech Stack
- Python 3.11+
- requests
- rich (CLI formatting)
- OpenAI
- FastAPI
- Unstructured
- Langchain