from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
def create_user_intent_analyst():
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are an expert in analyzing user intentions for YouTube video ideas. "
        "Given the following user input, please analyze and expand on their intention, "
        "providing a detailed context and explanation of what they want in their YouTube video. "
        "User Input: {user_input}\n\n"
        # "You must generate analysis in Korean.\n\n"
        "Detailed Analysis:"
    )
    return RunnableSequence(prompt | llm)

def analyze_user_intent(user_input):
    analyst = create_user_intent_analyst()
    return analyst.invoke({"user_input": user_input})