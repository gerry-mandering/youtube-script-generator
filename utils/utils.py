import logging

def setup_logger():
    logger = logging.getLogger('youtube_script_generator')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('logs/log.txt')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()