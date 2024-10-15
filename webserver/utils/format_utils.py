import re

def is_youtube_url(url):
    # Regular expression pattern for a YouTube video URL
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})'

    # Match the URL pattern against the input string
    match = re.match(pattern, url)

    # Return True if the pattern matches, otherwise False
    return match is not None
