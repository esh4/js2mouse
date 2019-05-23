import pygame
from pygame import joystick
from Button import Button


class Joystick:
    pygame_js = None
    buttons = {}

    def __init__(self, id=0):
        if not joystick.get_init():
            joystick.init()
        self.pygame_js = joystick.Joystick(id)
        self.pygame_js.init()

        # initialize all the buttons to False
        for i in range(self.pygame_js.get_numbuttons()):
            self.buttons[i] = Button(i, self.pygame_js.get_button)

    def update_buttons(self):
        for btn in self.buttons:
            self.buttons[btn].update()

    def set_button_clicked_callback(self, btn, callback):
        self.buttons[btn].set_clicked_callback(callback)

    def set_button_pressed_callback(self, btn, callback):
        print('setting button {} callback {}'.format(btn, callback))
        self.buttons[btn].set_pressed_callback(callback)

    def set_button_released_callback(self, btn, callback):
        self.buttons[btn].set_released_callback(callback)

    def get_axis(self, num):
        return self.pygame_js.get_axis(num)


