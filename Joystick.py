import pygame
from pygame import joystick


class Joystick:
    button_names = {}
    button_states = {}
    prev_button_states = {}
    button_callbacks = {}

    py_js = None

    def __init__(self, id=0):
        if not joystick.get_init():
            joystick.init()
        self.py_js = joystick.Joystick(id)
        self.py_js.init()

        # initialize all the buttons to False
        for i in range(self.py_js.get_numbuttons()):
            self.button_states[i] = False

    def update_button(self, btn, val):
        self.prev_button_states[btn] = self.button_states[btn]
        self.button_states[btn] = val

    def set_button_click_callback(self, btn, callback):
        self.button_callbacks[btn] = callback

    def check_clicks(self):
        for btn in self.button_states:
            if not self.prev_button_states[btn] and self.button_states[btn]:
                self.button_callbacks[btn]()

    def get_axis(self, num):
        return self.py_js.get_axis(num)
