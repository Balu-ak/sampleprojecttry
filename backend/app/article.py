from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ArticleContent:
    title: str
    text: str
    source_url: str
    source_domain: str
    estimated_reading_time_minutes: int


def extract_article(url: str) -> ArticleContent:
    parsed_url = urlparse(url)
    source_domain = parsed_url.netloc

    return ArticleContent(
        title="Article extraction not implemented yet",
        text="",
        source_url=url,
        source_domain=source_domain,
        estimated_reading_time_minutes=0,
    )
