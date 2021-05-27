#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
from typing import Text

from waveshare_epd import epd2in66
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

CWD = Path(__file__).parent
FONT_FILE = str(CWD / "Font.ttc")

FONT12 = ImageFont.truetype(FONT_FILE, 12)
FONT18 = ImageFont.truetype(FONT_FILE, 18)
FONT24 = ImageFont.truetype(FONT_FILE, 24)
PADDING = 4


class QuestDisplay:

    def __init__(self):
        self.epd = epd2in66.EPD()
        self.epd.init(0)
        self.epd.Clear()
        self.epd.init(1)
        self.epd.Clear()

        self.empty_frame = Image.new('1', (self.epd.height, self.epd.width), 0xFF)
        self.draw_area = ImageDraw.Draw(self.empty_frame)
        self.draw_area.rectangle((0, 0, 2500, 2500), fill=255)

    def clear(self):
        self.draw_area.rectangle((0, 0, 2500, 2500), fill=255)

    def draw_quest(self, current: int, limit: int):
        quest_string = f"Quest: {current}/{limit}"
        size = FONT24.getsize(quest_string)
        location = (10, 0, self.epd.height, size[1])
        self.draw_area.rectangle(location, fill=255)
        self.draw_area.text((location[0], location[1]), quest_string, font=FONT24, fill=0)
        self.epd.display(self.epd.getbuffer(self.empty_frame))

    def draw_attempts(self, current: int, limit: int):
        attempt_string = f"Attempts: {current}/{limit}"
        size = FONT24.getsize(attempt_string)
        location = (10, PADDING + size[1], self.epd.height, PADDING + 2.0 * size[1])
        self.draw_area.rectangle(location, fill=255)
        self.draw_area.text((location[0], location[1]), attempt_string, font=FONT24, fill=0)
        self.epd.display(self.epd.getbuffer(self.empty_frame))

    def draw_distance(self, distance: float):
        distance_string = f"Distance: {round(distance, 4)} km"
        size = FONT24.getsize(distance_string)
        location = (10, 2.0 * PADDING + 3.0 * size[1], self.epd.height, 3.0 * PADDING + 4.0 * size[1])
        self.draw_area.rectangle(location, fill=255)
        self.draw_area.text((location[0], location[1]), distance_string, font=FONT24, fill=0)
        self.epd.display(self.epd.getbuffer(self.empty_frame))

    def draw_text(self, message: Text):
        size = FONT24.getsize(message)
        location = (10, self.epd.width - size[1] - PADDING - 1, self.epd.height, self.epd.width)
        self.draw_area.rectangle(location, fill=255)
        self.draw_area.text((location[0], location[1]), message, font=FONT24, fill=0)
        self.epd.display(self.epd.getbuffer(self.empty_frame))

    def draw_center(self, message: Text):
        size = FONT24.getsize(message)
        location = ((self.epd.height - size[0]) / 2.0, (self.epd.width - size[1]) / 2.0)
        self.draw_area.rectangle((0, 0, 2500, 2500), fill=255)
        self.draw_area.text((location[0], location[1]), message, font=FONT24, fill=0)
        self.epd.display(self.epd.getbuffer(self.empty_frame))
