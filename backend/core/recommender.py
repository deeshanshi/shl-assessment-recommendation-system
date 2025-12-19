import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def detect_domains(query):
    tech = ["java", "python", "developer", "software", "sql", "cloud"]
    soft = ["communication", "collaboration", "teamwork", "leadership"]

    q = query.lower()
    return {
        "tech": any(t in q for t in tech),
        "soft": any(s in q for s in soft)
    }


def recommend_assessments(query: str, df: pd.DataFrame, k: int = 10):
    df = df.copy()

    # ---------- TF-IDF ----------
    corpus = (
        df["name"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["test_type"].fillna("")
    ).tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(corpus)
    q_vec = vectorizer.transform([query])

    scores = cosine_similarity(q_vec, X)[0]
    df["score"] = scores

    df = df.sort_values("score", ascending=False)

    # ---------- K/P BALANCE ----------
    domains = detect_domains(query)
    results = []

    if domains["tech"] and domains["soft"]:
        k_df = df[df["test_type"].str.contains("K", na=False)]
        p_df = df[df["test_type"].str.contains("P", na=False)]

        results = (
            k_df.head(k // 2).to_dict("records") +
            p_df.head(k // 2).to_dict("records")
        )

        if len(results) < k:
            results += df.head(k - len(results)).to_dict("records")
    else:
        results = df.head(k).to_dict("records")

    # ---------- SAFE OUTPUT ----------
    final = []
    for r in results[:k]:
        final.append({
            "name": r.get("name", ""),
            "url": r.get("url", ""),
            "description": r.get("description", ""),
            "duration": int(r["duration"]) if pd.notna(r.get("duration")) else 0,
            "remote_support": r.get("remote_support", "Yes"),
            "adaptive_support": r.get("adaptive_support", "No"),
            "test_type": [r.get("test_type")] if pd.notna(r.get("test_type")) else []
        })

    return final
