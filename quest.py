from typing import Text, List

import GPIO as GPIO

from display import QuestDisplay
from get_location import get_current_lat_lon
from dataclasses import dataclass
import geopy.distance


@dataclass
class Quest():
    name: Text
    lat: float
    lon: float
    attempts: int
    final_message: Text

    def __post_init__(self):
        self.current_attempt = 0

    def distance_to(self, lat: float, lon: float) -> float:
        return geopy.distance.distance((self.lat, self.lon), (lat, lon)).km


def start_quests(quests: List[Quest]):
    display = QuestDisplay()
    current_location = get_current_lat_lon()

    for quest in quests:
        distance_to_quest = quest.distance_to(*current_location)
        while True:
            # Do a button press
            if GPIO.input(10) == GPIO.HIGH:
                current_location = get_current_lat_lon()
                distance_to_quest = quest.distance_to(*current_location)
                display.draw_distance(distance_to_quest)
                quest.current_attempt = 1




