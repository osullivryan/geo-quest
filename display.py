#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in66
import time
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)


class QuestDisplay():

    def __init__(self):
        self.edp = epd2in66.EDP()
        self.edp.init(1)
        self.edp.Clear()

        self.empty_frame = Image.new('1', (self.epd.width, self.epd.height), 0xFF)
        self.quest_draw = ImageDraw.Draw(self.empty_frame)
        self.attempt_draw = ImageDraw.Draw(self.empty_frame)
        self.distance_draw = ImageDraw.Draw(self.empty_frame)

    def draw_attempts(self, current: int, limit: int):
        attempt_string = f"Attempts: {current}/{limit}"
        self.attempt_draw.text((10, 210), attempt_string, font=font24, fill=0)
        self.epd.display(epd.getbuffer(self.empty_frame))

    def draw_distance(self, distance: float):
        distance_string = f"Distance: {distance} km"
        self.distance_draw.text((40, 210), distance_string, font=font24, fill=0)
        self.epd.display(epd.getbuffer(self.empty_frame))

    def draw_quest(self, current: int, limit: int):
        quest_string = f"Quest: {current}/{limit}"
        self.quest_draw.text((50, 210), quest_string, font=font24, fill=0)
        self.epd.display(epd.getbuffer(self.empty_frame))


try:
    logging.info("epd2in66 Demo")

    epd = epd2in66.EPD()
    logging.info("init and Clear")
    epd.init(0)
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    Limage = Image.new('1', (epd.width, epd.height), 0xFF)  # 0xFF: clear the frame

    # partial update, mode 1
    logging.info("5.show time, partial update, just mode 1")
    epd.init(1)  # partial mode
    epd.Clear()
    time_draw = ImageDraw.Draw(Limage)
    num = 0
    while (True):
        time_draw.rectangle((10, 210, 120, 250), fill=255)
        time_draw.text((10, 210), time.strftime('%H:%M:%S'), font=font24, fill=0)
        epd.display(epd.getbuffer(Limage))

        num = num + 1
        if (num == 10):
            break

    logging.info("Clear...")
    epd.init(0)
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in66.epdconfig.module_exit()
    exit()
