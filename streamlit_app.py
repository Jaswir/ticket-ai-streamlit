import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import ai_boot

def main():
    st.title("Boston University IT Support Dashboard")
    st.subheader("AI Ticket Answering Assistant.")

    question_slot = st.empty()
    answer_slot = st.empty()

    # Function to handle button click
    def run_query(question):
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

    st.sidebar.title("Existing Tickets")

    placeholder_tickets = {
        "IDC738912": "Are there many opportunities for learning AI development in BU?",
        "IDC732671": "What is the latest IT support trend at BU?",
        "IDC732237": "How to get BU account?",
    }

    # Define sidebar buttons for different questions
    question_button_1 = st.sidebar.button("Ticket Number:" + " IDC738912  \n " + placeholder_tickets["IDC738912"])
    question_button_2 = st.sidebar.button("Ticket Number: IDC732671  \n " + placeholder_tickets["IDC732671"])
    question_button_3 = st.sidebar.button("Ticket Number: IDC732237  \n " + placeholder_tickets["IDC732237"])

    if question_button_1:
        run_query(placeholder_tickets["IDC738912"])
    elif question_button_2:
        run_query(placeholder_tickets["IDC732671"])
    elif question_button_3:
        run_query(placeholder_tickets["IDC732237"])

    # Add a button at the bottom of the navbar for generating own ticket
    st.sidebar.markdown("---")
    if st.sidebar.button("Generate Your Own Ticket"):
        question_slot.empty()
        answer_slot.empty()

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
            run_query(question)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
