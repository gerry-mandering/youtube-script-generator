from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_url):
    video_id = video_url.split('v=')[1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en', 'en-US'])
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {str(e)}")
        return None