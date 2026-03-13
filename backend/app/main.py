from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .article import extract_article
from .nlp import extract_keywords
from .schemas import AnalyzeRequest, AnalyzeResponse


app = FastAPI(title="3D Word Cloud News Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
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
