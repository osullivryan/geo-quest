from typing import Text, List

import RPi.GPIO as GPIO

from display import QuestDisplay
from get_location import get_current_lat_lon, GPSNotConnectedError
from dataclasses import dataclass
import geopy.distance
import threading
import sys
import time

BUTTON_PIN = 3
LED_PIN = 21
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN,
           pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.setup(LED_PIN, GPIO.OUT)
BUTTON_LED_PWN = GPIO.PWM(LED_PIN, 1000)  # create PWM instance with frequency
BUTTON_LED_PWN.start(0)  # start PWM of required Duty Cycle


class ThreadWithKill(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def led_button_sweep():
    while True:
        for duty in range(0, 66, 1):
            BUTTON_LED_PWN.ChangeDutyCycle(duty)  # provide duty cycle in the range 0-100
            time.sleep(0.01)
        time.sleep(0.25)

        for duty in range(66, -1, -1):
            BUTTON_LED_PWN.ChangeDutyCycle(duty)
            time.sleep(0.01)
        time.sleep(0.25)


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
    BUTTON_LED_PWN.ChangeDutyCycle(100)
    display = QuestDisplay()
    gps_found = False
    time.sleep(10)
    while not gps_found:
        try:
            get_current_lat_lon()
            gps_found = True
        except GPSNotConnectedError:
            display.draw_text('No GPS signal found...')
        time.sleep(5.0)
    display.clear()
    n_quests = len(quests)
    for quest_idx, quest in enumerate(quests):

        quest_led_sweep_thread = ThreadWithKill(target=led_button_sweep)
        quest_led_sweep_thread.start()

        display.clear()
        display.draw_quest(quest_idx + 1, n_quests + 1)
        done_with_quest = False
        display.draw_attempts(quest.current_attempt, quest.attempts)

        quest_led_sweep_thread.kill()
        quest_led_sweep_thread.join()
        BUTTON_LED_PWN.ChangeDutyCycle(100)
        while not done_with_quest:
            led_sweep_thread = ThreadWithKill(target=led_button_sweep)
            # If a distance is requested
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                led_sweep_thread.start()
                current_location = get_current_lat_lon(attempts=1000)
                distance_to_quest = quest.distance_to(*current_location)

                if distance_to_quest <= quest.tolerance:
                    done_with_quest = True
                    if quest_idx == n_quests - 1:
                        display.draw_center(quest.final_message)
                    else:
                        display.draw_text(quest.final_message)
                    led_sweep_thread.kill()
                    led_sweep_thread.join()
                    BUTTON_LED_PWN.ChangeDutyCycle(100)
                    # Wait for a button press to continue
                    while not (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
                        led_sweep_thread.kill()
                        led_sweep_thread.join()
                        BUTTON_LED_PWN.ChangeDutyCycle(100)
                        continue

                else:
                    display.draw_distance(round(distance_to_quest, 4))
                    quest.current_attempt += 1
                    display.draw_attempts(quest.current_attempt, quest.attempts)

                led_sweep_thread.kill()
                led_sweep_thread.join()
                BUTTON_LED_PWN.ChangeDutyCycle(100)
