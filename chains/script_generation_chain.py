from utils.utils import logger
from agents.user_intent_analyst import create_user_intent_analyst
from agents.keyword_generator import create_keyword_generator
from agents.video_viral_analyst import create_video_viral_analyst
from agents.reports_organizer import create_reports_organizer
from agents.script_generating_master import create_script_generating_master
from utils.youtube_crawler import get_top_videos
from utils.youtube_transcript import get_video_transcript
from utils.perplexity_search import perplexity_search

# logging.basicConfig(filename="logs/log.txt", level=logging.INFO, 
#                     format="%(asctime)s - %(levelname)s - %(message)s")

def create_script_generation_chain():
    return {
        "user_intent_analyst": create_user_intent_analyst(),
        "keyword_generator": create_keyword_generator(),
        "video_viral_analyst": create_video_viral_analyst(),
        "reports_organizer": create_reports_organizer(),
        "script_generating_master": create_script_generating_master()
    }

def run_script_generation_chain(user_input):
    logger.info(f"Starting script generation for input: {user_input}")
    chains = create_script_generation_chain()
    
    # Analyze user intent
    logger.info("Analyzing user intent")
    user_intent = chains["user_intent_analyst"].invoke({"user_input": user_input})
    # logging.info(f"User intent analysis complete: {user_intent[:100]}...")
    logger.info(f"User intent analysis complete: {user_intent}")
    
    # Generate keywords
    logger.info("Generating keywords")
    keywords_response = chains["keyword_generator"].invoke({"context": user_input})
    keywords = keywords_response.content if hasattr(keywords_response, 'content') else str(keywords_response)
    keywords = [keyword.strip().strip('"') for keyword in keywords.split(',')]
    logger.info(f"Keywords generated: {keywords}")
    
    # Get top videos and analyze them
    logger.info("Fetching and analyzing top videos")
    top_videos = get_top_videos(keywords)
    video_reports = []
    for video in top_videos:
        logger.info(f"Analyzing video {video['rank']}/{len(top_videos)}: {video['title']}")
        transcript = get_video_transcript(video['url'])
        logger.info(f"Transcript: {transcript}")
        if transcript:
            report = chains["video_viral_analyst"].invoke({
                "title": video['title'],
                "transcript": transcript,
                "views": video['views'],
                "rank": video['rank']
            })
            logger.info(f"Report: {report}")
            video_reports.append(report.content if hasattr(report, 'content') else str(report))
        else:
            logger.warning(f"Failed to fetch transcript for video: {video['title']}")
    logger.info(f"Video analysis complete. Analyzed {len(video_reports)} videos")

    # Organize the video reports
    logger.info("Organizing video reports")
    organized_reports = chains["reports_organizer"].invoke({
        "video_reports": video_reports
    })
    organized_reports = organized_reports.content if hasattr(organized_reports, 'content') else str(organized_reports)
    logger.info(f"Video reports organized: {organized_reports}")

    # Perform Perplexity searches
    logger.info("Performing Perplexity searches")
    search_results = []
    for keyword in keywords:
        logger.info(f"Searching Perplexity for: {keyword}")
        result = perplexity_search(keyword)
        search_results.append(result)
    logger.info("Perplexity searches complete")

    # Generate the final script
    logger.info("Generating final script")
    script = chains["script_generating_master"].invoke({
        "user_intent": user_intent,
        "keywords": ', '.join(keywords),
        "organized_reports": organized_reports,
        "search_results": '\n\n'.join(search_results)
    })
    script = script.content if hasattr(script, 'content') else str(script)
    logger.info("Script generation complete")
    logger.info(f"Generated script: {script}")
    
    return script