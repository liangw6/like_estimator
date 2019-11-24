import os

def retrieve_secret():
    """returns the key and secrets used for a flickr api connection
    
    Returns:
        a tuple -- (FLICK_KEY, FLICK_SECRET)
    """
    return os.environ["FLICKR_KEY"], os.environ["FLICKR_SECRET"]


