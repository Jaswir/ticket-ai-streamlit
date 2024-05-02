import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import ai_boot

def main():
    st.title("Boston University IT Support Dashboard")
    st.subheader("AI Ticket Answering Assistant.")

    question_slot = st.empty()
    answer_slot = st.empty()

    with st.form('input_form'):
        # Place the text input and the button within the form
        col1, col2 = st.columns([5, 1])
        with col1:
            question = st.text_input("Ask a question:")
        with col2:
            st.write(" ")
            st.write(" ")
            submit_button = st.form_submit_button(label="Submit")

    # Check if the form has been submitted
    if submit_button:
        if question:
            answer = ai_boot.getSummarizedAnswer(question)

            question_slot.write(question + "?")
            answer_slot.write(answer["summary"])

            st.write("Sources: ")
            st.write("Number of results: ", len(answer["sources"]))
            st.write("Top 3 results: ")
            for i in range(3):
                with stylable_container(
                    key="container_with_border",
                    css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        overflow: auto;
                    }
                    """,
                ):
                    st.write("Ticket Number: ", answer["sources"][i]["ticket-number"])
                    st.write(answer["sources"][i]["text"])
                    st.write("Score: ", answer["sources"][i]["score"])

        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
