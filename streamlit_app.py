import streamlit as st
import ai_boot

def get_answer(question):
    # In a real scenario, you'd have some logic to generate an answer based on the question
    # For simplicity, let's just return a placeholder answer
    return ai_boot.getAnswer(question)

def main():
    st.title("TicketAI")
    st.subheader("AI Ticket Answering Tool.")
    
    # Create a text input for the user to enter their question
    question = st.text_input("Ask a question:")
    
    # Create a button to trigger the answer
    if st.button("Get Answer"):
        if question:
            answer = get_answer(question)
            ticketno1 = answer[0]["metadata"]["ticket-number"].strip('"')
            ticketno2 = answer[1]["metadata"]["ticket-number"].strip('"')
            ticketno3 = answer[2]["metadata"]["ticket-number"].strip('"')
            st.write("Ticket Number: ", ticketno1)
            st.write(answer[0]["text"])
            st.write("Ticket Number: ", ticketno2)
            st.write(answer[1]["text"])
            st.write("Ticket Number: ", ticketno3)
            st.write(answer[2]["text"])
            st.write("Complete Returned Data: ")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
