from pydantic import BaseModel, Field, HttpUrl


class AnalyzeRequest(BaseModel):
    url: HttpUrl = Field(..., description="Public article URL to analyze.")


class WordCloudEntry(BaseModel):
    word: str = Field(..., description="Keyword or phrase for visualization.")
    weight: float = Field(..., description="Normalized relevance score.")


class AnalyzeResponse(BaseModel):
    title: str
    source_url: str
    source_domain: str
    estimated_reading_time_minutes: int
    top_phrases: list[str]
    word_cloud: list[WordCloudEntry]
