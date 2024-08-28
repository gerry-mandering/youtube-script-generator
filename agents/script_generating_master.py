from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

def create_script_generating_master():
    llm = ChatOpenAI(model_name="gpt-4o-2024-08-06", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are a master YouTube script writer. Your task is to create a high-quality, "
        "well-structured YouTube video script that can draw attention and generate many views. "
        "The script should be formatted as a markdown file. "
        "Use the following information to craft an engaging script as long as you can:\n\n"
        "User Intent: {user_intent}\n"
        "Keywords: {keywords}\n"
        "Relevant Video Reports: {organized_reports}\n"
        "Search Results: {search_results}\n\n"
        "Please create a script that includes:\n"
        "1. An attention-grabbing introduction\n"
        "2. Clear and engaging main points\n"
        "3. Relevant examples or case studies\n"
        "4. A strong call-to-action\n"
        "5. A memorable conclusion\n\n"
        # "You must generate script in Korean.\n\n"
        "Script:"
    )
    return RunnableSequence(prompt | llm)

def generate_script(user_intent, keywords, organized_reports, search_results):
    master = create_script_generating_master()
    return master.invoke({
        "user_intent": user_intent,
        "keywords": ', '.join(keywords),
        "organized_reports": '\n\n'.join(organized_reports),
        "search_results": '\n\n'.join(search_results)
    })