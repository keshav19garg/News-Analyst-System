import streamlit as st
# Assuming your logic is inside get_answer in urlloading.py
from urlloading import get_answer 

st.title("News Research Tool 2026")

# 1. Capture Sources and Question in ONE form for stability
with st.form("main_form"):
    st.subheader("1. Provide Sources")
    s1 = st.text_input("Source 1", key="s1")
    s2 = st.text_input("Source 2", key="s2")
    s3 = st.text_input("Source 3", key="s3")
    
    st.divider()
    
    st.subheader("2. Ask your Question")
    query = st.text_input("Question", key="q1", placeholder="What would you like to know?")
    
    # Single Submit Button
    submitted = st.form_submit_button("Generate Answer")

# 2. Process Logic
if submitted:
    # Filter valid sources
    raw_inputs = [s1, s2, s3]
    valid_sources = [res.strip() for res in raw_inputs if res.strip()]
    
    if not valid_sources:
        st.error("Please provide at least one source URL.")
    elif not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing articles..."):
            try:
                # Call your backend function
                answer = get_answer(valid_sources, query)
                
                # MOCK DATA for demonstration (Replace with actual function call)
                st.subheader("Answer")
                st.text_area(
                        label="LLM Response",
                        value=answer["answer_text"],
                        height=300,
                        key="ans_display"
                    )
                
                st.subheader("Source")
                st.text_area(
                        label="LLM Response",
                        value=answer["source"],
                        height=300,
                        key="ans_displays"
                    )
                # # 3. Display Results in Text Areas
                # st.subheader("Results")
                # col1, col2 = st.columns(2)
                
                # with col1:
                #     st.text_area(
                #         label="LLM Response",
                #         value=answer,
                #         height=300,
                #         key="ans_display"
                #     )

                # with col2:
                #     st.text_area(
                #         label="Source Material Used",
                #         value=answer["source"],
                #         height=300,
                #         key="src_display"
                #     )
            except Exception as e:
                st.error(f"An error occurred: {e}")
