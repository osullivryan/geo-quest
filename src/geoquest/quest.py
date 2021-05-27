from typing import Text, List

import RPi.GPIO as GPIO

from .display import QuestDisplay
from .get_location import get_current_lat_lon
from dataclasses import dataclass
import geopy.distance

#
BUTTON_PIN = 16
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN,
           pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)



@dataclass
class Quest:
    name: Text
    lat: float
    lon: float
    tolerance: float
    attempts: int
    final_message: Text

    def __post_init__(self):
        self.current_attempt = 0

    def distance_to(self, lat: float, lon: float) -> float:
        return geopy.distance.distance((self.lat, self.lon), (lat, lon)).km


def start_quests(quests: List[Quest]):
    display = QuestDisplay()
    current_location = get_current_lat_lon()
    n_quests = len(quests)

    for quest_idx, quest in enumerate(quests):
        display.clear()
        display.draw_quest(quest_idx + 1, n_quests)
        done_with_quest = False
        display.draw_attempts(quest.current_attempt, quest.attempts)
        while not done_with_quest:

            # If a distance is requested
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                current_location = get_current_lat_lon()
                distance_to_quest = quest.distance_to(*current_location)

                if distance_to_quest <= quest.tolerance:
                    done_with_quest = True
                    display.draw_text(quest.final_message)

                    # Wait for a button press to continue
                    while not (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
                        continue

                else:
                    display.draw_distance(round(distance_to_quest, 4))
                    quest.current_attempt += 1
                    display.draw_attempts(quest.current_attempt, quest.attempts)

