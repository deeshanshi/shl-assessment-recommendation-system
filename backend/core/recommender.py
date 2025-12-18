import pandas as pd
import re

# ---------- helpers ----------

def keyword_score(row, query_words):
    text = f"{row.get('name','')} {row.get('description','')}".lower()
    return sum(1 for w in query_words if w in text)


def detect_domains(query):
    tech_keywords = [
        "java", "python", "developer", "software", "cloud", "sql",
        "engineering", "programming", "coding", "devops"
    ]
    soft_keywords = [
        "collaboration", "teamwork", "communication",
        "leadership", "adaptability", "motivation"
    ]

    q = query.lower()
    return {
        "tech": any(k in q for k in tech_keywords),
        "soft": any(k in q for k in soft_keywords)
    }


# ---------- MAIN FUNCTION (SIGNATURE MUST NOT CHANGE) ----------

def recommend_assessments(query: str, df: pd.DataFrame, k: int = 10):
    """
    SHL-compliant recommender
    Returns list of dicts with full assessment details
    """

    # Tokenize query
    tokens = re.findall(r"\w+", query.lower())
    query_words = [t for t in tokens if len(t) > 2]

    domains = detect_domains(query)

    df = df.copy()

    # Keyword-based scoring
    df["score"] = df.apply(lambda r: keyword_score(r, query_words), axis=1)

    df = df.sort_values("score", ascending=False).reset_index(drop=True)

    # Fallback if no keyword match
    if df["score"].max() == 0:
        df["score"] = 1

    results = []

    # ---------- BALANCED LOGIC (TECH + SOFT) ----------
    if domains["tech"] and domains["soft"]:
        tech_df = df[df["test_type"].astype(str).str.contains("K", na=False)]
        soft_df = df[df["test_type"].astype(str).str.contains("P", na=False)]

        n_each = max(1, k // 3)

        picks = (
            tech_df.head(n_each).to_dict("records") +
            soft_df.head(n_each).to_dict("records")
        )

        seen = set(p.get("url") for p in picks)

        for _, r in df.iterrows():
            if len(picks) >= k:
                break
            if r.get("url") not in seen:
                picks.append(r.to_dict())
                seen.add(r.get("url"))

        results = picks
    else:
        results = df.head(k).to_dict("records")

    # ---------- SAFE FINAL OUTPUT (NO NaN CRASH) ----------
    final_results = []
    for r in results[:k]:
        final_results.append({
            "name": r.get("name", ""),
            "url": r.get("url", ""),
            "description": r.get("description", "") if pd.notna(r.get("description")) else "",
            "duration": int(r["duration"]) if pd.notna(r.get("duration")) else 0,
            "remote_support": r.get("remote_support", "Yes") if pd.notna(r.get("remote_support")) else "Yes",
            "adaptive_support": r.get("adaptive_support", "No") if pd.notna(r.get("adaptive_support")) else "No",
            "test_type": [r["test_type"]] if pd.notna(r.get("test_type")) else []
        })

    return final_results
