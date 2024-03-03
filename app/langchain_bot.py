from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

def create_chat_chain(api_key, system_prompt):
    # Create a system message prompt
    prompt = SystemMessage(content=system_prompt)
    
    # Create a new prompt with system message, human message, AI message, and user input placeholder
    new_prompt = prompt + HumanMessage(content="hi") + AIMessage(content="what?") + "{input}"
    
    return LLMChain(llm=ChatOpenAI(openai_api_key=api_key), prompt=new_prompt)

def chat(chain, user_input):
    # Run the chain with the user input
    output = chain.run(user_input)
    return output

# Example usage:
api_key = "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"
system_prompt = "I am MINMIN and I am like a friend to you and I am a helpful assistant trained on psychiatrists data  about the mental health patients."

# Create the chat chain


# Chat with the model using user input
# user_input = input("You: ")
# output = chat(chat_chain, user_input)
# print("Model: ", output)
