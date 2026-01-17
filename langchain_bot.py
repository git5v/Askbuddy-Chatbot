import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# def initialize_model():
#     # Initialize Gemini model
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",  # Fast & free gemini-3-flash-preview gemini-2.5-flash gemini-2.0-flash-lite
# #  gemini-2.5-flash-lite
#         # model="gemini-3-flash-preview",
#         google_api_key=api_key,
#         temperature=0.7
#     )
#     return llm

def initialize_model():
    # Define your primary model (the one you prefer to use)
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )

    # Define your fallback models
    fallback_1 = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=api_key,
        temperature=0.7
    )
    
    fallback_2 = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", # Older stable version as a safety net
        google_api_key=api_key,
        temperature=0.7
    )

    fallback_3 = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview", # Older stable version as a safety net
        google_api_key=api_key,
        temperature=0.7
    )

    fallback_4 = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", # Older stable version as a safety net
        google_api_key=api_key,
        temperature=0.7
    )

    # Combine them using fallbacks
    # If primary fails due to rate limits (429), it immediately tries the next in the list
    llm_with_fallback = primary_llm.with_fallbacks([fallback_1, fallback_2, fallback_3, fallback_4])
    
    return llm_with_fallback

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
        model_used = response.response_metadata.get("model_name")
        print(model_used)
        return response.text
    except Exception as e:
        error = f"Error occured as {e} "
        return error

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