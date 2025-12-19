import pandas as pd
from collections import defaultdict
from backend.core.recommender import recommend_assessments


TRAIN_PATH = "data/evaluation/train.csv"
CATALOG_PATH = "data/processed/shl_assessments.csv"
K = 10


# -------- URL NORMALIZATION (VERY IMPORTANT) --------
def normalize_url(url):
    if not isinstance(url, str):
        return ""
    return url.strip().lower().rstrip("/")


def recall_at_k(predicted, relevant, k):
    predicted_k = {normalize_url(u) for u in predicted[:k]}
    relevant_set = {normalize_url(u) for u in relevant}

    if not relevant_set:
        return 0.0

    return len(predicted_k & relevant_set) / len(relevant_set)


def main():
    # -------- Load data --------
    train_df = pd.read_csv(TRAIN_PATH, encoding="latin1")
    catalog_df = pd.read_csv(CATALOG_PATH)

    # -------- Group relevant URLs by query --------
    query_to_urls = defaultdict(list)
    for _, row in train_df.iterrows():
        query_to_urls[row["Query"]].append(row["Assessment_url"])

    recalls = []

    # -------- Evaluate each query --------
    for query, relevant_urls in query_to_urls.items():

        recommendations = recommend_assessments(
            query=query,
            df=catalog_df,
            k=K
        )

        predicted_urls = [r["url"] for r in recommendations]

        r = recall_at_k(predicted_urls, relevant_urls, K)
        recalls.append(r)

        print("Query:", query[:80] + ("..." if len(query) > 80 else ""))
        print(f"Recall@{K}: {r:.3f}\n")

    # -------- Final Mean Recall --------
    mean_recall = sum(recalls) / len(recalls)
    print(f"✅ FINAL Mean Recall@{K}: {mean_recall:.4f}")


if __name__ == "__main__":
    main()
