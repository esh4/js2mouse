import pygame
import pymouse
import time
from queue import Queue
from threading import Thread
import Xlib.threaded

pygame.joystick.init()
pygame.display.init()
print('pygame inited')

js = pygame.joystick.Joystick(0)
js.init()
mouse = pymouse.PyMouse()

print(js.get_name())
print(js.get_numaxes())
AXIS_MULTIPLIER = 35

btn_queue = Queue()


def handle_btns():
    while True:
        while not btn_queue.empty():
            func, args = btn_queue.get()
            func(args)
            print(func)
            btn_queue.task_done()
            print('task done')
    time.sleep(0.5)


btn_thread = Thread(target=handle_btns)
btn_thread.setDaemon(True)
btn_thread.setName('btn_thread')
# btn_thread.start()

previous_btn_states = {
    0: False
}

while True:
    pygame.event.pump()
    current_pos = mouse.position()
    mov_x = int(js.get_axis(0) * AXIS_MULTIPLIER)
    mov_y = int(js.get_axis(1) * AXIS_MULTIPLIER)

    mouse.move(current_pos[0] + mov_x, current_pos[1] + mov_y)

    if not previous_btn_states[0] and js.get_button(0):
        print('adding to queue')
        btn_queue.put((lambda m: m.click(m.position()[0], m.position()[1]), mouse))
        print('click added to queue')
    # else:
    #     print('no press')

    previous_btn_states[0] = js.get_button(0)
    # time.sleep(0.2)

print('exited main loop')





