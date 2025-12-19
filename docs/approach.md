# SHL Assessment Recommendation System – Approach

## 1. Problem Understanding

The goal of this project is to build a recommendation system that suggests the most relevant SHL **Individual Test Solutions** for a given recruiter query or job description.

Given an input query (natural language job description), the system must:
- Recommend **up to 10 assessments**
- Ensure recommendations align with both **technical skills** and **behavioral/personality requirements**
- Return results in a structured format suitable for automated evaluation

This is a **multi-label recommendation problem**, as each query can map to multiple valid SHL assessments.

---

## 2. Data Sources

### 2.1 SHL Assessment Catalog
The SHL product catalog was used to construct the assessment dataset.  
Each assessment contains:
- Assessment name  
- Assessment URL  
- Description  
- Test type (Knowledge/Skill or Personality/Behavior)  
- Duration  
- Remote and adaptive support flags  

Pre-packaged job solutions were excluded, and only **Individual Test Solutions** were considered.

### 2.2 Labeled Evaluation Data
SHL-provided train and test datasets were used:
- `train.csv` for evaluation
- `test.csv` for final submission

Each query in the train dataset maps to **multiple relevant assessment URLs**, making the task multi-label.

---

## 3. Recommendation Approach

### 3.1 Retrieval Method

Due to system-level constraints on Windows (PyTorch DLL issues), a **TF-IDF based vector retrieval approach** was implemented as a robust and reproducible baseline.

The assessment text representation is created by combining:
- Assessment name  
- Assessment description  
- Test type  

TF-IDF vectors are computed for all assessments, and cosine similarity is used to retrieve the most relevant candidates for a given query.

This satisfies the requirement of a **vector-based retrieval system** as specified in the assignment.

---

### 3.2 Domain-Aware Re-ranking (K / P Balance)

Recruiter queries often contain both:
- **Technical requirements** (e.g., Java, Python, SQL)
- **Behavioral or soft-skill requirements** (e.g., collaboration, leadership)

To address this, a domain detection heuristic is applied:
- If both technical and soft-skill signals are detected, the final recommendation list is balanced between:
  - Knowledge/Skill (K) tests
  - Personality/Behavior (P) tests

This ensures the recommendations better reflect real hiring needs rather than relying purely on lexical similarity.

---

## 4. Evaluation Strategy

### 4.1 Metric

The system is evaluated using **Mean Recall@10**, as required.

For each query:
- The top 10 recommended assessment URLs are compared against the ground-truth URLs
- Recall is computed using **exact URL-level matching**

### 4.2 URL Normalization

During evaluation, URLs are normalized by:
- Converting to lowercase
- Removing trailing slashes

This avoids false negatives due to formatting differences.

---

## 5. Results and Observations

The TF-IDF baseline achieved a **low Mean Recall@10 (~0.02)**.

This result is expected due to:
- Long and generic job descriptions
- Strict URL-level matching
- The lexical nature of TF-IDF, which struggles with semantic similarity
- A large and diverse set of relevant assessments per query

Despite the low recall value, the evaluation pipeline is correct and highlights the limitations of keyword-based retrieval on this dataset.

---

## 6. Limitations

- TF-IDF does not capture semantic similarity effectively for long job descriptions
- Exact URL-level evaluation is very strict in a multi-label setting
- Embedding-based semantic retrieval (e.g., sentence transformers) is expected to significantly improve recall but could not be fully deployed due to system constraints

---

## 7. Future Improvements

- Replace TF-IDF with transformer-based sentence embeddings
- Apply hybrid retrieval (semantic retrieval + rule-based re-ranking)
- Incorporate additional constraints such as duration and seniority
- Use relaxed or category-level evaluation for qualitative analysis

---

## 8. Conclusion

This project demonstrates a complete, end-to-end assessment recommendation pipeline:
- Data preparation
- Vector-based retrieval
- Domain-aware re-ranking
- Proper evaluation and analysis

The system is robust, reproducible, and aligns with SHL’s problem requirements while clearly documenting its limitations and improvement opportunities.
