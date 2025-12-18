SHL Assessment Recommendation System – Approach
1. Problem Understanding

Hiring managers often struggle to identify the most relevant assessments for a given role using traditional keyword-based search and filtering. Such approaches fail to capture the semantic intent of job descriptions and often lead to irrelevant or unbalanced assessment recommendations.

The objective of this project is to build an intelligent recommendation system that accepts a natural language query or job description and returns 5–10 relevant SHL Individual Test Solutions. The system must be accurate, scalable, and capable of balancing technical and behavioral assessments as required by SHL.

2. Data Collection and Preparation

The first step involved building a data ingestion pipeline by scraping the SHL Product Catalog. Only Individual Test Solutions were collected, explicitly excluding pre-packaged job solutions as per the assignment requirements.

For each assessment, the following attributes were extracted and structured:

Assessment name

Assessment URL

Description

Test type (Knowledge & Skills / Personality & Behavior)

Duration

Remote support

Adaptive support

The scraped data was cleaned and stored in a CSV format. Special care was taken to handle missing values and ensure robustness. The final dataset contained more than the minimum required number of assessments, making it suitable for downstream retrieval and evaluation.

3. Recommendation Architecture

To overcome the limitations of keyword matching, the recommendation system uses a semantic retrieval-based approach.

The overall pipeline is:

User provides a natural language query or job description

The query is processed and tokenized

Assessments are ranked based on relevance using a scoring mechanism

Top candidates are selected and post-processed for balance

Final recommendations are returned via an API

This modular pipeline ensures clarity, maintainability, and extensibility.

4. Domain Detection and Balancing Logic

An important requirement of the assignment is to ensure balanced recommendations when a query spans multiple competency domains.

To address this, the system performs lightweight domain detection by identifying whether the query relates to:

Technical skills (e.g., programming, software development, data skills)

Behavioral or personality traits (e.g., communication, teamwork, leadership)

If both domains are detected, the recommender intentionally balances the output by including assessments from both Knowledge & Skills and Personality & Behavior categories. This ensures that hiring managers receive a holistic set of assessments aligned with real-world hiring needs.

5. API and Application Design

The recommendation engine is exposed via a FastAPI backend with two endpoints:

/health – Used to verify API availability

/recommend – Accepts a query and returns recommended assessments

The API response strictly follows the format specified in the SHL assessment document.

A Streamlit-based frontend is built on top of the API to provide a simple and user-friendly interface. Users can enter a query and view the recommended assessments in a tabular format.

6. Evaluation Strategy

To evaluate the effectiveness of the recommendation system, the provided labeled training dataset was used. The performance metric chosen was Mean Recall@10, as specified in the assignment.

For each query in the training set:

The top 10 recommended assessments were retrieved

The overlap between predicted and ground-truth assessment URLs was computed

Although initial recall values were low due to the small dataset and strict URL-level matching, the evaluation pipeline demonstrates a correct and reproducible methodology. The focus of this step was on validating the retrieval logic and ensuring metric correctness rather than overfitting to the limited training data.

7. Final Predictions

After finalizing the system, predictions were generated for the unlabeled test dataset. The results were exported in the exact CSV format required by SHL, with each query mapped to its recommended assessment URLs.

8. Conclusion

This project demonstrates an end-to-end assessment recommendation system that satisfies all requirements outlined in the SHL assignment. It includes data scraping, semantic relevance modeling, balanced recommendation logic, evaluation, API exposure, and a user-facing application. The solution is modular, explainable, and designed to be easily extended or improved in future iterations.