# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bisect
import os

# read finished list
def read_list():
    beatmaps = []
    SONG_PATH = 'E:/osu!/Songs'
    filenames = os.listdir(SONG_PATH)
    for name in filenames:
        bisect.insort(beatmaps, int(name.split(' ')[0]))
    return beatmaps
    
# set up
def setup(web_url):
    DRIVER_PATH = 'C:/Users/simon/Downloads/chromedriver.exe'
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(web_url)
    return driver

# download
def download(driver, beatmap_num, maps):
    index = bisect.bisect_left(maps['beatmaps'], beatmap_num)
    start_time = time.time()
    while True:
        try:
            downloads = driver.find_elements(By.CLASS_NAME, 'btn-osu-big')
            if len(downloads) >= 4:              # find download available 
                if index >= len(maps['beatmaps']) or beatmap_num != maps['beatmaps'][index]:    # find downloaded not not
                    bisect.insort(maps['beatmaps'], int(beatmap_num))
                    maps['new_beatmaps'].append(int(beatmap_num))
                    if len(downloads) == 6: # no video version
                        downloads[2].click()
                    if len(downloads) == 5:
                        downloads[1].click()
                    if len(downloads) == 4:
                        downloads[1].click()
            elif time.time() - start_time < 3:  # keep loading
                continue
            else:
                failed_index = bisect.bisect_left(maps['failed_beatmaps'], beatmap_num)
                if failed_index >= len(maps['failed_beatmaps']) or beatmap_num != maps['failed_beatmaps'][failed_index]:    # find downloaded not not
                    bisect.insort(maps['failed_beatmaps'], int(beatmap_num))
            break  #download NOT available 
        except: # keep loading
            continue
    
    index2 = bisect.bisect_left(maps['total_beatmaps'], beatmap_num)
    if index2 >= len(maps['total_beatmaps']) or beatmap_num != maps['total_beatmaps'][index2]:    # find downloaded not not
        bisect.insort(maps['total_beatmaps'], int(beatmap_num))
    return maps

#close tab   
def close(driver):
    handles = driver.window_handles
    driver.switch_to.window(window_name=handles[1])
    driver.close()
    driver.switch_to.window(window_name=handles[0])
    
def main():  # first time run
    maps = {}
    maps['beatmaps'] = read_list()
    web_url = 'https://osu.ppy.sh/users/2025671'
    driver = setup(web_url)
    time.sleep(15)  # login
    
    # expand all beatmaps history
    while True:
        buttons = driver.find_elements(By.CLASS_NAME, 'show-more-link')
        if len(buttons) == 4:
            # loading element
            try:
                buttons[3].click()
            except:
                continue
        else:
            break
    
    # main function
    maps['total_beatmaps'] = []
    maps['new_beatmaps'] = []
    maps['failed_beatmaps'] = []
    blocks = driver.find_elements(By.CLASS_NAME, 'beatmap-playcount__cover')
    for block in blocks:
        # find beatmaps
        link = block.get_attribute('href')
        driver.switch_to.new_window('tab')
        driver.get(link)
        time.sleep(1)  # avoid too many request 
        strUrl = driver.current_url
        beatmap_num = int(strUrl.split('/')[4].split('#')[0])
        
        maps = download(driver, beatmap_num, maps)
        close(driver)
    
    print('Total played songs: '+str(len(maps['total_beatmaps'])))
    print('Local songs: '+str(len(maps['beatmaps'])))
    print('Should download songs: '+str(len(maps['new_beatmaps'])))
    print('Failed songs: '+str(len(maps['failed_beatmaps'])))
    
    return maps

def recheck(maps):
    maps['beatmaps'] = read_list()
    web_url = 'https://osu.ppy.sh/beatmapsets/'    
    driver = setup(web_url)
    time.sleep(15)  # login
    
    old_failed_beatmaps = maps['failed_beatmaps']
    maps['new_beatmaps'] = []
    maps['failed_beatmaps'] = []
    for beatmap_num in old_failed_beatmaps:
        link = web_url+str(beatmap_num)
        driver.switch_to.new_window('tab')
        driver.get(link)
        
        maps = download(driver, beatmap_num, maps)
        close(driver)
    
    print('Local songs: '+str(len(maps['beatmaps'])))
    print('Should download songs: '+str(len(maps['new_beatmaps'])))
    print('Failed songs: '+str(len(maps['failed_beatmaps'])))
    
