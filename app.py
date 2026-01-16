import streamlit as st
from urlloading import get_answer

st.title("News Analysis Tool")

# ---- INPUT SECTION ----
with st.form("main_form"):
    left_col, right_col = st.columns([1, 1])

    # LEFT: News Sources
    with left_col:
        st.subheader("📰 News Sources")
        s1 = st.text_input("Source 1")
        s2 = st.text_input("Source 2")
        s3 = st.text_input("Source 3")

    # RIGHT: Question
    with right_col:
        st.subheader("❓ Your Question")
        query = st.text_area(
            "Ask your question",
            placeholder="What would you like to know from these articles?",
            height=150
        )

    submitted = st.form_submit_button("Generate Answer")

# ---- PROCESSING SECTION ----
if submitted:
    valid_sources = [s.strip() for s in [s1, s2, s3] if s.strip()]

    if not valid_sources:
        st.error("Please provide at least one source URL.")
    elif not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing articles..."):
            try:
                answer = get_answer(valid_sources, query)

                st.divider()

                # ---- OUTPUT SECTION ----
                st.subheader("✅ Answer")
                st.markdown(answer["answer_text"])

                st.subheader("🔗 Source")
                if answer["source"]:
                    st.markdown(answer["source"])
                else:
                    st.markdown("_No source available_")

            except Exception as e:
                st.error(f"An error occurred: {e}")
