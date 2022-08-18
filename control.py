# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 22:36:11 2022

@author: simon
"""

import pyautogui as pg
import time

# detect position
# pos = [0, 0]
# while True:
#     if pos != list(pg.position()):
#         pos = list(pg.position())
#         print(pos)

# action
start_time = [23, 20, 0]
now_time = time.localtime()
duration = 60 * 60 * (start_time[0]-now_time[3]) + 60 * (start_time[1]-now_time[4]) + (start_time[2]-now_time[5])
time.sleep(duration)
pg.moveTo(36, 297, 2)
pg.click()
pg.moveTo(1186, 673, 2)
pg.click()
    

