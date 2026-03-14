import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .article import extract_article
from .nlp import extract_keywords
from .schemas import AnalyzeRequest, AnalyzeResponse


LOCAL_DEVELOPMENT_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


app = FastAPI(title="3D Word Cloud News Analyzer API")


def get_allowed_origins() -> list[str]:
    configured_origins = os.getenv("FRONTEND_ORIGINS", "")
    extra_origins = [
        origin.strip() for origin in configured_origins.split(",") if origin.strip()
    ]
    return LOCAL_DEVELOPMENT_ORIGINS + extra_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_article(request: AnalyzeRequest) -> AnalyzeResponse:
    article = extract_article(str(request.url))
    top_phrases, word_cloud = extract_keywords(article.text)

    return AnalyzeResponse(
        title=article.title,
        source_url=article.source_url,
        source_domain=article.source_domain,
        estimated_reading_time_minutes=article.estimated_reading_time_minutes,
        top_phrases=top_phrases,
        word_cloud=word_cloud,
    )
