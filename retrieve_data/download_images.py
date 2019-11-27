import requests
import os
import sys
import urllib
import time
import math
import multiprocessing as mp
import socket

IMAGE_THRESHOLD = 10
SOCKET_TIMEOUT = 5   # 5 secs according to https://docs.python.org/2/library/socket.html#socket.socket.settimeout

def download_image_by_url(dir_name, urls, image_names=['image'], set_timeout=False):
    print("inputs", dir_name, len(urls), len(image_names))
    if set_timeout:
        socket.setdefaulttimeout(SOCKET_TIMEOUT)
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
    print("total {} images downloaded in the past {} sec".format(count, curr_t - t0))
    print("average download speed: {} sec per image".format((curr_t - t0) / count))

def multiprocess_download_image_by_url(dir_name, urls, image_names=['image'], nprocess=8):
    # set up timeout
    socket.setdefaulttimeout(SOCKET_TIMEOUT)
    # set up input arguments so they can be used in parallel
    if len(image_names) == 1:
        # add unique labels to images
        image_names = ['{}_{}'.format(image_names[0], i) for i in range(len(urls))]
    urls_per_process = math.ceil(len(urls) / nprocess)
    input_args = [(dir_name,
                   urls[urls_per_process * i: urls_per_process * (i + 1)],
                   image_names[urls_per_process * i: urls_per_process * (i + 1)]) for i in range(nprocess)]
    # print(input_args[:10])

    with mp.Pool(processes=nprocess) as pool:
        pool.starmap(download_image_by_url, input_args)
        
