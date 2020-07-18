"""
skill toykon-button-skill
Copyright (C) 2020  limeStudio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill
from mycroft.messagebus.message import Message

import time
import RPi.GPIO as GPIO
import os

# GPIO pins
#BUTTON = 23
BUTTON = 17
#LED = 25

class ToykonToggleButton(MycroftSkill):
    def __init__(self):
        super(ToykonToggleButton, self).__init__("ToykonToggleButton")

    def initialize(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            #GPIO.setup(LED, GPIO.OUT)
            GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=handle_button, bouncetime = 500)
            #GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=handle_button)

        except GPIO.error:
            self.log.warning("Can't initialize GPIO - skill will not load")
            self.speak_dialog("error.initialise")
        finally:
            self.schedule_repeating_event(self.handle_button,
                                          None, 0.1, 'GoogleAIY')
            self.add_event('recognizer_loop:record_begin',
                           self.handle_listener_started)
            self.add_event('recognizer_loop:record_end',
                           self.handle_listener_ended)
                                       
    def handle_button(self, message):
        longpress_threshold = 2
        #self.log.info("callback handle_button")

        #if GPIO.event_detected(BUTTON):
        if not GPIO.input(BUTTON):
            self.log.info("GPIO.event_detected")
            #self.speak_dialog("GPIO.event_detected")
            pressed_time = time.time()
            while not GPIO.input(BUTTON):
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            elif pressed_time > 10:
               self.log.info("WIFI Inint")
               os.system('sudo systemctl disable wpa_supplicant@wlan0.service')
               os.system('sudo systemctl enable wpa_supplicant@ap0.service')
               os.system('sudo systemctl stop wpa_supplicant@wlan0.service')
               #os.system('mv wpa_supplicant-wlan0.conf.tmp /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
               os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
               os.system('sleep 5')
               os.system('sudo systemctl start wpa_supplicant@ap0.service')
               os.system('sleep 5')
               os.system('sudo shutdown -r now')
        #else:
            #self.log.info("Don't detect handle_button")


    def handle_listener_started(self, message):
        # code to excecute when active listening begins...
        self.log.info("listening begins")
        #GPIO.output(LED, GPIO.HIGH)

    def handle_listener_ended(self, message):
        self.log.info("listening ends")
        #GPIO.output(LED, GPIO.LOW)
        
def create_skill():
    return ToykonToggleButton()
