import time
from groq import Groq
import streamlit as st

# Groq API setup
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

# System message that sets the behavior of the chatbot
system_message = (
    "You are an expert assistant designed to help people with Smart Agriculture and IoT systems. "
    "Your role is to provide guidance, troubleshooting, and information regarding smart agriculture technologies, including IoT sensors (temperature, humidity, soil moisture), devices (ESP32, Raspberry Pi), and network configuration. "
    "You should provide practical advice to users of all experience levels, including farmers, engineers, and hobbyists. "
    "Answers should be clear, concise, and offer practical solutions or tips. "
    "Your tone should be friendly and professional."
)

# System prompt setup
system_prompt = {
    "role": "system",
    "content": system_message
}

# Function to get the response from Groq API
def get_response(chat_history):
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192", 
        messages=chat_history,
        max_tokens=200,
        temperature=0.8 
    )
    chat_response = response.choices[0].message.content
    return chat_response

# Personalized recommendation based on user input
def personalized_recommendation(user_input):
    """ Custom function to provide personalized recommendations based on user input """
    user_input = user_input.lower()
    if "corn" in user_input and "dry" in user_input:
        return "For corn in dry conditions, we recommend using soil moisture sensors to monitor irrigation needs."
    elif "tomatoes" in user_input:
        return "Tomatoes require careful monitoring of both soil moisture and temperature. We recommend using both soil moisture and temperature sensors."
    else:
        return "I recommend using a soil moisture sensor to monitor irrigation. Let me know if you need more specific recommendations."

# Troubleshooting common issues with IoT devices
def troubleshoot_device(issue):
    """ Troubleshooting for common issues """
    issue = issue.lower()
    if "wifi" in issue:
        return "Ensure your ESP32 device is within range of your router, or try resetting the device and checking the credentials."
    elif "sensor" in issue:
        return "If your sensor isn't giving the correct readings, check its wiring and recalibrate it if necessary."
    else:
        return "Could you provide more details about the issue you're facing?"

# Main function to run the Streamlit app
def main():
    st.title("IoT-Partner")
    
    # Expanded description section
    with st.expander("About"):
        st.write("""
            This chatbot helps users with information, guidance, and troubleshooting for IoT systems in smart agriculture, such as temperature, humidity, and soil moisture sensors. 
            It can assist with devices like ESP32 and Raspberry Pi.
        """)
    
    # Initialize session state to store the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt]  # Start with system message

    # Display chat history
    for message in st.session_state.messages:
        if message != system_prompt:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Capture user input
    if prompt := st.chat_input("Ask me anything about IoT in agriculture!"):
        st.session_state.messages.append({"role": "user", "content": prompt})  # Add user message to history

        # Display user input
        with st.chat_message("user"):
            st.markdown(prompt)

        # Personalized Recommendation or Troubleshooting Logic
        if "recommend" in prompt or "advice" in prompt:
            response = personalized_recommendation(prompt)
        elif "issue" in prompt or "problem" in prompt:
            response = troubleshoot_device(prompt)
        else:
            # Get chatbot response via Groq API
            response = get_response(st.session_state.messages)

        # Display the chatbot's response with word-by-word streaming (using Markdown for formatting)
        with st.chat_message("assistant"):
            for word in response.split():
                st.markdown(word + " ", unsafe_allow_html=True)
                time.sleep(0.05)  # Simulate word-by-word streaming

        # Append assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the app
if __name__ == "__main__":
    main()

