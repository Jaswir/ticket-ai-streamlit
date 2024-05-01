import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.tags import tagger_component
import ai_boot

def get_answer(question):
    # In a real scenario, you'd have some logic to generate an answer based on the question
    # For simplicity, let's just return a placeholder answer
        
    return ai_boot.getAnswer(question)

import streamlit as st

if 'show_title' not in st.session_state:
    st.session_state.show_title = False

def main():
    if not st.session_state.show_title:
        st.title("TicketAI")
        st.subheader("AI Ticket Answering Tool.")
        st.session_state.show_title = True

    # Create a text input for the user to enter their question
    question = st.text_input("Ask a question:")
    
    # Create a button to trigger the answer
    if st.button("Get Answer"):
        if question:
            answer = get_answer(question)

            numofresults = str(len(answer))
            tagger_component(
                "tags:",
                ["tickets: " + numofresults, "number", "answer", "question", "support"],
                color_name=["blue", "green", "red", "yellow", "pink"],
            )   

            ticketno1 = answer[0]["metadata"]["ticket-number"].strip('"')
            ticketno2 = answer[1]["metadata"]["ticket-number"].strip('"')
            ticketno3 = answer[2]["metadata"]["ticket-number"].strip('"')
            
            with stylable_container(
                key="container_with_border",
                css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
                st.write("Ticket Number: ", ticketno1)
                st.write(answer[0]["text"])

            with stylable_container(
                key="container_with_border",
                css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
                st.write("Ticket Number: ", ticketno2)
                st.write(answer[1]["text"])

            with stylable_container(
                key="container_with_border",
                css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
                st.write("Ticket Number: ", ticketno3)
                st.write(answer[2]["text"])

            st.write("Complete Returned Object: ")
            st.write(answer)
            
            st.session_state.show_title = False
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
