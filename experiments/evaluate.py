import pandas as pd
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath("."))

from backend.core.recommender import recommend_assessments

TRAIN_PATH = "data/evaluation/train.csv"
K = 10

def recall_at_k(predicted, relevant, k):
    predicted_k = set(predicted[:k])
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    return len(predicted_k & relevant_set) / len(relevant_set)

def main():
    df = pd.read_csv(
        TRAIN_PATH,
        encoding="latin1",
        engine="python"
    )

    # 🔹 Group relevant URLs by query
    query_to_urls = defaultdict(list)
    for _, row in df.iterrows():
        query_to_urls[row["Query"]].append(row["Assessment_url"])

    recalls = []

    for query, relevant_urls in query_to_urls.items():
        catalog_df = pd.read_csv("data/processed/shl_assessments.csv")

        recommendations = recommend_assessments(
            query=query,
            df=catalog_df,
            k=K
            )
        predicted_urls = [r["url"] for r in recommendations]

        r = recall_at_k(predicted_urls, relevant_urls, K)
        recalls.append(r)

    mean_recall = sum(recalls) / len(recalls)
    print(f"✅ Mean Recall@{K}: {mean_recall:.4f}")

if __name__ == "__main__":
    main()