import streamlit as st
import ai_boot

def get_answer(question):
    # In a real scenario, you'd have some logic to generate an answer based on the question
    # For simplicity, let's just return a placeholder answer
    return ai_boot.getAnswer(question)

def main():
    st.title("Question and Answer App")
    
    # Create a text input for the user to enter their question
    question = st.text_input("Ask a question:")
    
    # Create a button to trigger the answer
    if st.button("Get Answer"):
        if question:
            answer = get_answer(question)
            st.write(answer)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
