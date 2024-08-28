from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

def create_reports_organizer():
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are an expert analyst tasked with distilling the key success factors from multiple YouTube video reports. "
        "Your goal is to identify and summarize the common elements that contribute to the success of these videos, "
        "focusing on content, presentation, and audience engagement strategies.\n\n"
        "Given the following video reports, please analyze and organize the information to reveal "
        "the secrets of success for these videos. Your analysis should cover:\n\n"
        "1. Common themes or topics that resonate with the audience\n"
        "2. Effective presentation techniques and video structures\n"
        "3. Engagement strategies that drive views and interactions\n"
        "4. Any unique or innovative approaches that stand out\n"
        "5. Patterns in video length, style, or format that contribute to success\n\n"
        "Video Reports:\n{video_reports}\n\n"
        "Please provide a concise, well-structured summary of your findings, highlighting the key factors "
        "that contribute to the success of these videos. Your analysis should be actionable for someone "
        "looking to create successful YouTube content.\n\n"
        # "You must generate reports in Korean.\n\n"
        "Organized Report:"
    )
    return RunnableSequence(prompt | llm)

def organize_reports(video_reports):
    organizer = create_reports_organizer()
    return organizer.invoke({"video_reports": "\n\n".join(video_reports)})
