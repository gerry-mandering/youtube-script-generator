from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
from config.settings import OPENAI_API_KEY, MODEL_NAME

def create_greeting_chain():
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=MODEL_NAME)
    prompt = ChatPromptTemplate.from_template("What is the best way to greet {name}?")
    return RunnableSequence(prompt | llm)

def run_greeting_chain(name):
    chain = create_greeting_chain()
    return chain.invoke({"name": name})