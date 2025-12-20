import streamlit as st
import requests
import time

# 🔗 LIVE BACKEND URL (Render)
BASE_URL = "https://shl-assessment-recommendation-system-1-wcau.onrender.com"
API_URL = f"{BASE_URL}/recommend"
HEALTH_URL = f"{BASE_URL}/health"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    layout="centered"
)

st.title("🔍 SHL Assessment Recommendation System")

st.markdown(
    "Enter a hiring requirement or job description to get the most relevant "
    "SHL assessment recommendations."
)

query = st.text_area(
    "Hiring requirement / Job description:",
    placeholder="e.g. Looking for Java developers with teamwork and communication skills"
)

k = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=10,
    value=10
)

# ---------- Helper: Wake up backend ----------
def warm_up_backend():
    try:
        requests.get(HEALTH_URL, timeout=15)
        time.sleep(1)
        return True
    except Exception:
        return False


if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Connecting to recommendation service..."):
            backend_ready = warm_up_backend()

        if not backend_ready:
            st.error(
                "Backend service is waking up. "
                "Please wait a few seconds and try again."
            )
        else:
            with st.spinner("Fetching recommendations..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"query": query, "k": k},
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json().get("recommendations", [])

                        if not data:
                            st.info("No recommendations found for this query.")
                        else:
                            st.success("Recommended SHL Assessments:")
                            for i, rec in enumerate(data, start=1):
                                st.markdown(
                                    f"**{i}. {rec.get('name','')}**  \n"
                                    f"[Open Assessment]({rec.get('url','')})"
                                )
                    else:
                        st.error(
                            f"API error ({response.status_code}). "
                            "Please try again later."
                        )

                except requests.exceptions.Timeout:
                    st.error("Request timed out. Backend may be waking up.")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to backend service. "
                        "Please try again in a moment."
                    )
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
