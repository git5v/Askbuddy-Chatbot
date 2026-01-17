import streamlit as st
from langchain_bot import interact_with_bot, initialize_model, create_promt  

st.set_page_config(
    page_title="Askbuddy AI Bot",
    page_icon="🤖", # You can also use ":robot_face:"
)

st.title("Askbuddy 🤖 your personal AI Chatbot")
st.markdown("Question and answer board 🖥️ with Langchain and Gemini")

llm = initialize_model()
prompt = create_promt()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    content = message['content']
    st.chat_message('AI').markdown(content)


query = st.chat_input("Please ask your query")
if query:
    try:
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message('User').markdown(query)
        context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        with st.spinner("Thinking..."):
            output = interact_with_bot(prompt, llm, context)
            st.spinner("Thinking...")
            st.chat_message('AI').markdown(output)
            st.session_state.messages.append({"role": "AI", "content": output})

    except Exception as e:
        st.error(f"An error occusrred: {e}")  

