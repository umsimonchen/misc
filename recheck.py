# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 18:22:37 2022

@author: simon
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bisect
import os

# read finished list
beatmaps = []
SONG_PATH = 'E:/osu!/Songs'
filenames = os.listdir(SONG_PATH)
for name in filenames:
    bisect.insort(beatmaps, int(name.split(' ')[0]))
  
# set up
web_url = 'https://osu.ppy.sh/beatmapsets/'
DRIVER_PATH = 'C:/Users/simon/Downloads/chromedriver.exe'
driver = webdriver.Chrome(DRIVER_PATH)
driver.get(web_url)

# login
time.sleep(15)

failed_beatmaps = [21928,
 51755,
 52709,
 60214,
 70257,
 73903,
 83333,
 95533,
 173051,
 176832,
 257623]

new_failed_beatmaps = []

for beatmap_num in failed_beatmaps:
    link = web_url+str(beatmap_num)
    driver.switch_to.new_window('tab')
    driver.get(link)
    
    # download
    index = bisect.bisect_left(beatmaps, beatmap_num)
    start_time = time.time()
    while True:
        try:
            downloads = driver.find_elements(By.CLASS_NAME, 'btn-osu-big')
            if len(downloads) >= 4:              # find download available 
                if index >= len(beatmaps) or beatmap_num != beatmaps[index]:    # find downloaded not not
                    bisect.insort(beatmaps, int(beatmap_num))
                    #new_beatmaps.append(int(beatmap_num))
                    if len(downloads) == 6: # no video version
                        downloads[2].click()
                    if len(downloads) == 5:
                        downloads[1].click()
                    if len(downloads) == 4:
                        downloads[1].click()
                time.sleep(1) # avoid too many request 
            elif time.time() - start_time < 3:  # keep loading
                continue
            else:
                failed_index = bisect.bisect_left(failed_beatmaps, beatmap_num)
                if failed_index >= len(failed_beatmaps) or beatmap_num != failed_beatmaps[failed_index]:    # find downloaded not not
                    bisect.insort(new_failed_beatmaps, int(beatmap_num))
            break  #download NOT available 
        except: # keep loading
            continue
    
    #close tab
    tmp = driver.current_url    
    handles = driver.window_handles
    driver.switch_to.window(window_name=handles[1])
    driver.close()
    driver.switch_to.window(window_name=handles[0])

    
    
    
    