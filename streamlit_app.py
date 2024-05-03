import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import ai_boot
import json
import random

def main():
    st.title("Boston University IT Support Dashboard")
    st.subheader("AI Ticket Answering Assistant.")

    question_slot = st.empty()
    answer_slot = st.empty()

    # Function to handle button click
    def run_query(question):
        answer = ai_boot.getSummarizedAnswerGPT4(question)

        question_slot.write(question + "?")
        answer_slot.write(answer["summary"])

        st.write("Sources: ")
        st.write("Number of results: ", len(answer["sources"]))
        st.write("Top 3 results: ")

        # Generate a unique ticket number
        ticket_number = "IDC" + ''.join(random.choices('0123456789', k=6))

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
                st.write("Ticket Number: ", answer["sources"][i]["ticket-number"].strip('"'))
                st.write(answer["sources"][i]["text"])
                # st.write("Score: ", answer["sources"][i]["score"])

        return ticket_number

    st.sidebar.title("Incoming Questions")

    # Load tickets from JSON file
    try:
        with open('tickets.json', 'r') as file:
            placeholder_tickets = json.load(file)
    except FileNotFoundError:
        placeholder_tickets = {}

    # Define sidebar buttons for different questions
    for ticket_id, ticket_question in placeholder_tickets.items():
        if st.sidebar.button("Ticket Number: " + ticket_id + "\n" + ticket_question):
            run_query(ticket_question)

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
            save_query = st.checkbox("Save this query")
        with col2:
            st.write(" ")
            st.write(" ")
            submit_button = st.form_submit_button(label="Submit")

    # Check if the form has been submitted
    if submit_button:
        if question:
            ticket_number = run_query(question)
            if save_query:
                save_to_file(ticket_number, question)
        else:
            st.warning("Please enter a question.")

def save_to_file(ticket_number, question):
    # Save the ticket to the JSON file
    with open('tickets.json', 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
        data[ticket_number] = " \n " + question
        file.seek(0)
        json.dump(data, file)

if __name__ == "__main__":
    main()