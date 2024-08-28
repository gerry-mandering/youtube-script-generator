from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

def create_keyword_generator():
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are an expert in generating relevant keywords based on a given context. "
        "Given the following context, please generate 3 highly relevant keywords or short phrases "
        "(3-6 words each) that best represent the content and would be effective for search keywords. "
        # "You must generate keywords in Korean.\n\n"
        "Context: {context}\n\n"
        "Keywords (comma-separated):"
    )
    return RunnableSequence(prompt | llm)

def generate_keywords(context):
    generator = create_keyword_generator()
    keywords = generator.invoke({"context": context})
    return [keyword.strip() for keyword in keywords.split(',')]