from utils.utils import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re

def convert_views_to_number(views_str):
    views_str = views_str.lower().replace('views', '').strip()
    multiplier = 1
    if 'k' in views_str:
        multiplier = 1000
        views_str = views_str.replace('k', '')
    elif 'm' in views_str:
        multiplier = 1000000
        views_str = views_str.replace('m', '')
    
    try:
        return int(float(views_str) * multiplier)
    except ValueError:
        return 0

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def search_youtube(keyword):
    logger.info(f"Starting YouTube search for keyword: {keyword}")
    driver = setup_driver()
    url = f"https://www.youtube.com/results?search_query={keyword}"
    
    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)
        
        # Wait for the video elements to load
        wait = WebDriverWait(driver, 10)
        video_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer')))
        
        logger.info(f"Found {len(video_elements)} video elements")
        
        videos = []
        for i, video in enumerate(video_elements, 1):
            logger.info(f"Processing video element {i}")
        
            title_elem = video.find_element(By.CSS_SELECTOR, '#video-title')
            title = title_elem.text.strip() if title_elem else 'No title'
            link = title_elem.get_attribute('href') if title_elem else ''

            logger.info(f"Title: {title}, Link: {link}")

            # Continue if the link is youtube shorts
            if '/shorts/' in link:
              logger.info(f"Skipping shorts video: {title} with link: {link}")
              continue
        
            metadata_line = video.find_element(By.ID, 'metadata-line')
            metadata_spans = metadata_line.find_elements(By.CSS_SELECTOR, 'span.ytd-video-meta-block')
            views = metadata_spans[0].text if len(metadata_spans) > 0 else 'N/A'
        
            # Extract duration using the new method
            try:
                duration_elem = WebDriverWait(video, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#time-status #text'))
                )
                duration = duration_elem.get_attribute('aria-label')
                logger.info(f"Extracted duration: {duration}")
            except Exception as e:
                logger.error(f"Error extracting duration for video {i}: {str(e)}")
                continue
        
            # Parse duration and check if it's over 25 minutes
            duration_parts = duration.split(', ')
            total_minutes = 0
            for part in duration_parts:
                if 'minute' in part:
                    total_minutes += int(part.split()[0])
                elif 'hour' in part:
                    total_minutes += int(part.split()[0]) * 60

            logger.info(f"Calculated total minutes: {total_minutes}")

            if total_minutes >= 25:
                logger.info(f"Skipping video {title} due to length: {duration}")
                continue
        
            videos.append({'title': title, 'url': link, 'views': views, 'duration': duration})
            logger.info(f"Added video to list: {title} | Views: {views} | Duration: {duration}")
        
            if len(videos) == 5:
                break
        
        logger.info(f"Completed processing. Found {len(videos)} videos for keyword: {keyword}")
        return videos
    
    except TimeoutException:
        logger.error(f"Timeout while waiting for video elements to load for keyword: {keyword}")
        return []
    except Exception as e:
        logger.error(f"Error during YouTube search for '{keyword}': {str(e)}")
        return []
    finally:
        driver.quit()

def get_top_videos(keywords):
    logger.info(f"Starting to get top videos for keywords: {keywords}")
    all_videos = []
    for keyword in keywords:
        videos = search_youtube(keyword)
        all_videos.extend(videos)
        logger.info(f"Added {len(videos)} videos for keyword '{keyword}'. Total videos so far: {len(all_videos)}")
    
    # Convert views to numbers and sort
    for video in all_videos:
        video['views_count'] = convert_views_to_number(video['views'])
        logger.info(f"Converted views for video {video['title']}: {video['views_count']}")
    
    all_videos.sort(key=lambda x: x['views_count'], reverse=True)
    
    # Assign ranks
    for i, video in enumerate(all_videos, 1):
        video['rank'] = i
        logger.info(f"Assigned rank {i} to video {video['title']}: {video['views_count']}")

    logger.info(f"Completed gathering and ranking videos. Total videos found: {len(all_videos)}")
    return all_videos