# 🎾 Rakket AI — Tennis Coach AI

An AI tennis coach that makes your practice more fun, structured and effective. Describe your goals
in plain English and get tailored drill recommendations, or drop in a YouTube coaching video and get
a clean, structured breakdown of the drills and techniques in it.

> Personal side project. Powered by **Google Gemini** via **Pydantic AI**, served with **FastAPI** +
> **Streamlit**, containerised with **Docker** and deployed on **Google Cloud Run**.

> ⛔ **All rights reserved — look, don't copy.** Public for reference/portfolio purposes only; not
> open source, no permission to copy, fork, run, or reuse. See [`LICENSE`](LICENSE). Want to use any
> of it? Ask first: srimukessh1994@gmail.com

---

## What's inside

Rakket AI is two small apps that share a tennis-coach brain:

### 1. 🧠 Drill Recommender (`api/` + `frontend/`)
A FastAPI service over a curated library of tennis drills (`data/drills.csv`). It exposes both a
classic filtered search and a natural-language endpoint backed by a Pydantic AI agent, so a user can
just say *"I want to work on my backhand consistency on my own"* and get back matching drills.
A lightweight Streamlit UI sits on top.

### 2. 📺 YouTube Video Summariser (`youtube_summariser/`)
Paste a YouTube URL (or video ID) and it pulls the video's transcript (via `youtube-transcript-api`)
and metadata (via the YouTube Data API), then has a tennis-coach agent produce a structured summary —
main topic, each drill/technique broken down, and specific coaching points. Its own Streamlit app.

---

## Repository structure

```
rakket_ai/
├── api/                      # FastAPI drill-recommendation service
│   ├── main.py               #   /recommend-drills (filter) + /ai-recommend-drills (NL agent)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Streamlit UI that calls the deployed API
│   ├── streamlit_app.py
│   ├── Dockerfile
│   └── requirements.txt
├── youtube_summariser/       # Standalone YouTube → structured tennis summary app
│   ├── youtube_summariser.py       #   transcript + metadata → Gemini agent
│   ├── youtube_summariser_app.py   #   Streamlit UI
│   ├── Dockerfile
│   └── requirements.txt
├── data/drills.csv           # The drill library (source of truth for the recommender)
├── youtube_api_test.ipynb    # Exploration notebook
└── .devcontainer/            # VS Code dev container
```

---

## Tech stack

- **LLM:** Google Gemini (`gemini-1.5-flash`) via [Pydantic AI](https://ai.pydantic.dev) agents + tools
- **API:** FastAPI + Uvicorn
- **UI:** Streamlit
- **Data:** pandas over a CSV drill library
- **YouTube:** YouTube Data API v3 + `youtube-transcript-api`
- **Infra:** Docker, Google Cloud Run

---

## Getting started

### Prerequisites
- Python 3.10+
- A **Google Gemini API key**
- A **YouTube Data API key** (only for the summariser)

### Environment variables
Create a `.env` file (loaded via `python-dotenv`) or export in your shell:

```bash
GEMINI_API_KEY=your_gemini_key        # used by both agents
YOUTUBE_API_KEY=your_youtube_key      # used by the summariser only
```

For the Streamlit summariser, these can also be provided via Streamlit secrets.

### Run the Drill Recommender API
```bash
pip install -r api/requirements.txt
uvicorn api.main:app --reload          # http://localhost:8000  (docs at /docs)
```
The drill CSV is resolved relative to the source file, so you can launch from any directory.

### Run the Streamlit frontend
```bash
pip install -r frontend/requirements.txt
streamlit run frontend/streamlit_app.py
```
By default it calls the deployed Cloud Run endpoint; point it at `http://localhost:8000` to use a
local API.

### Run the YouTube Summariser
```bash
pip install -r youtube_summariser/requirements.txt
streamlit run youtube_summariser/youtube_summariser_app.py
```

---

## API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/recommend-drills` | Filter the drill library by query params: `focus_area`, `difficulty`, `num_players`, `shot_type`. |
| `POST` | `/ai-recommend-drills` | Natural-language recommendations. Param: `message`. A Pydantic AI agent interprets the request and calls the drill-filter tool, falling back to sensible defaults. |

Example:
```bash
curl "http://localhost:8000/recommend-drills?focus_area=Consistency&difficulty=Intermediate&num_players=2"
curl -X POST "http://localhost:8000/ai-recommend-drills?message=help%20me%20with%20my%20serve"
```

---

## The drill library

`data/drills.csv` is the heart of the recommender. Each row is one drill with columns including:
**Drill Name · Shot/Type · Focus Area · Number of Players · Singles/Doubles · Difficulty ·
Equipment · Time · Description · Coaching Tip · AI summary.** Add rows here to expand what the
coach can recommend — no code change needed.

---

## Deployment

Each app ships with a `Dockerfile`. The API is deployed to **Google Cloud Run** (the frontend points
at its public URL). Build and run locally with, e.g.:

```bash
docker build -t rakket-api ./api
docker run -p 8000:8000 --env-file .env rakket-api
```

---

## Roadmap ideas

- Expand and implement more of the drill library (several drills are marked *Not Implemented*).
- Richer video summaries (timestamps, per-drill clips).
- Session planning: chain recommended drills into a full practice plan.

---

*Made by the Rakket AI team · powered by the YouTube API & Google Gemini 🎾*
