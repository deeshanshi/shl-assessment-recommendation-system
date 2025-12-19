import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🔍 SHL Assessment Recommendation System")

query = st.text_area(
    "Enter hiring requirement / job description:",
    placeholder="e.g. Looking for Java developers with teamwork skills"
)

k = st.slider("Number of recommendations", min_value=5, max_value=20, value=10)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query, "k": k},
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json().get("recommendations", [])

                    if not data:
                        st.info("No recommendations found.")
                    else:
                        st.success("Recommended Assessments:")
                        for i, rec in enumerate(data, start=1):
                            st.markdown(
                                f"**{i}. {rec.get('name','')}**  \n"
                                f"[Open Assessment]({rec.get('url','')})"
                            )
                else:
                    st.error(f"API error ({response.status_code}). Please try again.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Please make sure the backend is running.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
