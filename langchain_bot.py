import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def initialize_model():
    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",  # Fast & free gemini-3-flash-preview gemini-2.5-flash gemini-2.5-flash-lite
        # model="gemini-3-flash-preview",
        google_api_key=api_key,
        temperature=0.7
    )
    return llm

def create_promt():
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. \
        Limit you answer in a paragraph to give a anser in a crisp and concise way \
        You strictly refuse to discuss adult content, illegal acts, or dangerous topics. \
        Be helpful and friendly, but never break your safety rules."),
        ("user", "{input}")
    ])
    return prompt

def interact_with_bot(prompt: str, llm, user_input: str):
    
    try:
        chain = prompt | llm
        print("Gemini + LangChain Chat (type 'quit' to exit):")
        # user_input = input("You: ")
        if user_input.lower() in ['quit', 'bye', 'exit']:
            print("---------Thanks you for your repsone---------")
        else :
            print('**Generating repsonse for your provided input**')
        response = chain.invoke({"input": user_input})
        print("Gemini:", response.text)
        return response.text
    except Exception as e:
        print(f"Error occured as {e} ")

def create_chain_interactive_loop(prompt: str, llm, user_input: str):
    # Create chain
    chain = prompt | llm

    # Interactive loop
    print("Gemini + LangChain Chat (type 'quit' to exit):")
    while user_input:
        interact_with_bot(prompt, llm, user_input)
        

def ask_model(user_input: str = "Hi"):
    llm = initialize_model()
    prompt = create_promt()
    create_chain_interactive_loop(prompt, llm, user_input)
    

if __name__ == "__main__":
    ask_model()