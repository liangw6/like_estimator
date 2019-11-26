import requests
import os
import sys
import urllib
import time

IMAGE_THRESHOLD = 10

def download_image_by_url(dir_name, urls, image_names=['image']):
    if len(image_names) == 1:
        # add unique labels to images
        image_names = ['{}_{}'.format(image_names[0], i) for i in range(len(urls))]
    if not os.path.isdir(dir_name):
        # create the directory if not exists
        os.mkdir(dir_name)

    # help us record how fast we are downloading
    count = 0
    t0 = time.time()
    prev_t = t0
    for url, image_name in zip(urls, image_names):
        if count % IMAGE_THRESHOLD == 0 and count != 0:
            print("downloaded {} images in the past {} secs".format(IMAGE_THRESHOLD, time.time() - prev_t))
            prev_t = time.time()
        path_to_write = os.path.join(dir_name, image_name + url.split('.')[-1])
        try:
            urllib.request.urlretrieve(url, path_to_write)
        except Exception as e:
            print("exception {} occurred when downloading image {}".format(e, count))
        # update count
        count += 1
    
    curr_t = time.time()
    print("total {} images downloaded in the past {} sec".format(len(count), curr_t - t0))
    print("average download speed: {} sec per image".format((curr_t - t0) / count))

