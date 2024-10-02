import google.generativeai as genai
import streamlit as st

# Set up the title and description of the app
st.title('Vamshi : AI-Powered Mental Health Support Chatbot')
st.write('Ask me about mental health and emotional support!')


api_key=st.secrets["gemini_api_key"]
# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define a more detailed persona for the chatbot
persona = """You are Vamshi, the Supportive AI Mentor. You are empathetic, understanding, and capable of providing support to students experiencing mental health challenges. 
- Ensure your responses are concise, supportive, and relevant to the user's query.
- Offer advice based on the user's feelings or questions, providing practical tips and resources.
- Use a friendly and approachable tone, avoiding judgmental or dismissive language.
"""

feedback_prompt = "How did I do? Please provide your feedback on the support provided."

# Initialize session state variables
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Input box for user queries
question = st.text_input("How are you feeling or what would you like to know about mental health?")

if st.button("Ask"):
    if question:
        # Append the user's question to the conversation history
        st.session_state.conversation_history.append(f"**You:** {question}")

        # Create a more specific prompt with context
        prompt = f"{persona} The user is feeling {question}. Please provide a concise, supportive, and informative response, considering the previous conversation history: {st.session_state.conversation_history}"
        response = model.generate_content(prompt)

        # Ensure the response is under 500 words
        if len(response.text) > 500:
            response.text = response.text[:500] + "..."

        # Append the chatbot's response to the conversation history
        st.session_state.conversation_history.append(f"**Vamshi:** {response.text}")

        # Display the conversation history with labels and styling
        for message in st.session_state.conversation_history:
            if message.startswith("**You:**"):
                st.markdown(f"<div style='text-align: right; color: #007bff;'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; color: #000000;'>{message}</div>", unsafe_allow_html=True)

        # Feedback section with a rating scale
        feedback_rating = st.selectbox("How helpful was the response?", ["Very helpful", "Helpful", "Neutral", "Not helpful", "Very not helpful"])
        if st.button("Submit Feedback"):
            # Log the feedback (e.g., save to a database or file)
            st.success("Thank you for your feedback!")

# Add functionality to provide support tips or resources
if st.button("Get Mental Health Tips"):
    tips_prompt = "Provide concise mental health tips for students, tailored to their specific needs. Consider their emotional state and any challenges they may be facing."
    tips_response = model.generate_content(tips_prompt)
    st.markdown(f"<div style='text-align: left; color: #000000;'>**Mental Health Tips:** {tips_response.text}</div>", unsafe_allow_html=True)

# Clear conversation history button
if st.button("Clear Memories"):
    # Clear the conversation history from the session state
    st.session_state.conversation_history = []
    # Refresh the app (optional)
    # st.experimental_rerun()  # This might be unreliable, consider alternative

    # Alternative: Manually trigger a re-render without relying on experimental rerun
    st.write("")  # Add an empty space to force a re-render
    st.experimental_rerender()  # This is a more reliable way to refresh

# Additional features
if st.button("Track Your Mood"):
    # Implement a mood tracking feature (e.g., using a slider or rating scale)
    st.write("Mood Tracking Feature: Coming soon!")

if st.button("Set Goals"):
    # Implement a goal setting feature (e.g., allowing users to input their goals)
    st.write("Goal Setting Feature: Coming soon!")
