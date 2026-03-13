from sklearn.feature_extraction.text import TfidfVectorizer

from .schemas import WordCloudEntry


MAX_FEATURES = 50
TOP_PHRASE_COUNT = 3
WORD_CLOUD_COUNT = 30
MINIMUM_TERM_LENGTH = 2


def extract_keywords(text: str) -> tuple[list[str], list[WordCloudEntry]]:
    cleaned_text = text.strip()
    if not cleaned_text:
        return [], []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=MAX_FEATURES,
        lowercase=True,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
    )

    try:
        matrix = vectorizer.fit_transform([cleaned_text])
    except ValueError:
        return [], []

    feature_names = vectorizer.get_feature_names_out().tolist()
    scores = matrix.toarray()[0].tolist()

    ranked_terms = _rank_terms(feature_names, scores)
    if not ranked_terms:
        return [], []

    top_phrases = [term for term, _ in ranked_terms[:TOP_PHRASE_COUNT]]
    word_cloud = _build_word_cloud(ranked_terms[:WORD_CLOUD_COUNT])
    return top_phrases, word_cloud


def _rank_terms(
    feature_names: list[str],
    scores: list[float],
) -> list[tuple[str, float]]:
    ranked_terms: list[tuple[str, float]] = []

    for term, score in zip(feature_names, scores):
        if score <= 0:
            continue
        if not _is_useful_term(term):
            continue
        ranked_terms.append((term, float(score)))

    ranked_terms.sort(key=lambda item: (-item[1], item[0]))
    return ranked_terms


def _build_word_cloud(ranked_terms: list[tuple[str, float]]) -> list[WordCloudEntry]:
    if not ranked_terms:
        return []

    max_score = ranked_terms[0][1]
    if max_score <= 0:
        return []

    return [
        WordCloudEntry(word=term, weight=round(score / max_score, 4))
        for term, score in ranked_terms
    ]


def _is_useful_term(term: str) -> bool:
    cleaned_term = term.strip()
    if not cleaned_term:
        return False

    tokens = cleaned_term.split()
    if not tokens:
        return False

    return all(len(token) >= MINIMUM_TERM_LENGTH for token in tokens)
