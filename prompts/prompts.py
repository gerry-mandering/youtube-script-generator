from langchain.prompts import PromptTemplate

def greet_prompt():
    return PromptTemplate(
        input_variables=["name"],
        template="What is the best way to greet {name}?"
    )