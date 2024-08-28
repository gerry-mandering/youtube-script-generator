from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

def create_video_viral_analyst():
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are an expert in analyzing viral YouTube videos. Given the following information about a video, "
        "please analyze why it went viral or not, and provide a detailed report. "
        "Title: {title}\n"
        "Transcript: {transcript}\n"
        "Views: {views}\n"
        "Rank: {rank} out of 15\n\n"
        "Please provide your analysis in the following format:\n"
        "1. Essential Parts 1:\n"
        "   - [Copy and paste the transcript here]\n"
        "   - [Describe key points of that part]\n\n"
        "2. Essential Parts 2:\n"
        "   - [Copy and paste the transcript here]\n"
        "   - [Describe key points of that part]\n\n"
        "3. Essential Parts 3:\n"
        "   - [Copy and paste the transcript here]\n"
        "   - [Describe key points of that part]\n\n"
        "4. Viral Analysis:\n"
        "   - [Provide an overall review of why this video went viral or not, and how]\n\n"
        # "You must generate analysis in Korean.\n\n"
        "Analysis:"
    )
    return RunnableSequence(prompt | llm)

def analyze_video_virality(title, transcript, views, rank):
    analyst = create_video_viral_analyst()
    return analyst.invoke({
        "title": title,
        "transcript": transcript,
        "views": views,
        "rank": rank
    })