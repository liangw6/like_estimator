from flickrapi import FlickrAPI
import pandas as pd
import os
import time

FLICKR_KEY = os.environ["FLICKR_KEY"]
FLICKR_SECRET = os.environ["FLICKR_SECRET"]
TIME_THRESHOLD = 100

#  different url types
# url_c: URL of medium 800, 800 on longest size image
# url_m: URL of small, medium size image
# url_n: URL of small, 320 on longest side size image
# url_o: URL of original size image
# url_q: URL of large square 150x150 size image
# url_s: URL of small suqare 75x75 size image
# url_sq: URL of square size image
# url_t: URL of thumbnail, 100 on longest side size image


def get_urls_by_tag(image_tag, max_count=100, url_type='url_o'):
    """get a number of urls for images by their tags
    
    Arguments:
        image_tag {[string]} -- [tag applied to search for relevant images]
    
    Keyword Arguments:
        max_count {int} -- [total number of urls returned] (default: {100})
        url_type {string} -- [type for the urls to be returned, see the top of the file for explanation of different url types]
    
    Returns:
        [urls] -- [an array of urls (of size max_count), each of which can be used to download an image.]
    """
    flickr = FlickrAPI(FLICKR_KEY, FLICKR_SECRET)
    photos = flickr.walk(text=image_tag,
                         tag_mode='all',
                         extras=url_type,
                         per_page=50,
                         sort='relevance')
    t_prev = time.time()
    count = 0
    urls = []
    for photo in photos:
        if count % TIME_THRESHOLD == 0 and count != 0:
            print("{} urls downloaded in the past {:.3f} s".format(TIME_THRESHOLD, time.time() - t_prev))
            t_prev = time.time()
        if count >= max_count:
            print("all {} photo urls have been saved".format(count))
            break
        try:
            url = photo.get('url_o')
            if url is None:
                print('failed to fetch url for image {} '.format(count))
                continue
            urls.append(url)
        except:
            print('url for image number {} cannot be fetched'.format(count))
        # update the count
        count += 1
    return urls




