import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.tags import tagger_component
import ai_boot

def get_answer(question):
    # In a real scenario, you'd have some logic to generate an answer based on the question
    # For simplicity, let's just return a placeholder answer
        
    return ai_boot.getAnswer(question)


import streamlit as st

def main():
    
    st.title("Boston University IT Support Dashboard")
    st.subheader("AI Ticket Answering Assistant.")
    
    question_slot = st.empty()
    answer_slot = st.empty()

    # Create a text input for the user to enter their question
    question = st.text_input("Ask a question:")
    
    # Create a button to trigger the answer
    if st.button("Get Answer"):
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

            numofresults = str(len(answer))
            
            # with stylable_container(
            #     key="container_with_border",
            #     css_styles="""
            #     {
            #         border: 1px solid rgba(49, 51, 63, 0.2);
            #         border-radius: 0.5rem;
            #         padding: calc(1em - 1px)
            #     }
            #     """,
            # ):
            #     st.write("Ticket Number: ", ticketno1)
            #     st.write(answer[0]["text"])

            # with stylable_container(
            #     key="container_with_border",
            #     css_styles="""
            #     {
            #         border: 1px solid rgba(49, 51, 63, 0.2);
            #         border-radius: 0.5rem;
            #         padding: calc(1em - 1px)
            #     }
            #     """,
            # ):
            #     st.write("Ticket Number: ", ticketno2)
            #     st.write(answer[1]["text"])

            # with stylable_container(
            #     key="container_with_border",
            #     css_styles="""
            #     {
            #         border: 1px solid rgba(49, 51, 63, 0.2);
            #         border-radius: 0.5rem;
            #         padding: calc(1em - 1px)
            #     }
            #     """,
            # ):
            #     st.write("Ticket Number: ", ticketno3)
            #     st.write(answer[2]["text"])

        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
