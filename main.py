import pygame
import pymouse
import time
from queue import Queue
from threading import Thread
import Xlib.threaded
from Joystick import Joystick

pygame.joystick.init()
pygame.display.init()
print('pygame inited')

# config joystick
js = Joystick(0)

mouse = pymouse.PyMouse()
MOUSE_MOVE_MULTIPLIER: int = 30
SCROLL_MULTIPLIER: int = 10


btn_queue = Queue()

# js.set_button_clicked_callback(0, lambda: btn_queue.put((lambda m: m.click(m.position()[0], m.position()[1]), mouse)))
js.set_button_pressed_callback(3, lambda: btn_queue.put((lambda m: m.press(m.position()[0], m.position()[1], button=1), mouse)))
js.set_button_released_callback(3, lambda: btn_queue.put((lambda m: m.release(m.position()[0], m.position()[1], button=1), mouse)))

js.set_button_pressed_callback(0, lambda: btn_queue.put((lambda m: m.press(m.position()[0], m.position()[1], button=2), mouse)))
js.set_button_released_callback(0, lambda: btn_queue.put((lambda m: m.release(m.position()[0], m.position()[1], button=2), mouse)))

js.set_button_pressed_callback(12, lambda: btn_queue.put((lambda m: m.press(m.position()[0], m.position()[1], button=3), mouse)))
js.set_button_released_callback(12, lambda: btn_queue.put((lambda m: m.release(m.position()[0], m.position()[1], button=3), mouse)))

def handle_btns():
    while True:
        while not btn_queue.empty():
            func, args = btn_queue.get()
            func(args)
            btn_queue.task_done()
        time.sleep(0.04)


def scroll(mouse, movement_callback):
    while True:
        mouse.scroll(vertical=movement_callback())
        time.sleep(0.2)


btn_thread = Thread(target=handle_btns)
btn_thread.setDaemon(True)
btn_thread.setName('btn_thread')
btn_thread.start()

scroll_thread = Thread(target=scroll, args=(mouse, lambda: -js.get_axis(4)*SCROLL_MULTIPLIER))
scroll_thread.setName('scroll_thread')
scroll_thread.setDaemon(True)
scroll_thread.start()

while True:
    pygame.event.pump()

    js.update_buttons()

    # handle joystick
    current_pos = mouse.position()
    from Tools import non_linear_map
    mov_x = int(non_linear_map(js.get_axis(0)))# * MOUSE_MOVE_MULTIPLIER)
    mov_y = int(non_linear_map(js.get_axis(1))) #* MOUSE_MOVE_MULTIPLIER)
    mouse.move(current_pos[0] + mov_x, current_pos[1] + mov_y)

    time.sleep(0.03)






