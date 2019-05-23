class Button:
    name = 'btn'
    id = -1

    state = False
    prev_state = False
    active = False

    btn_state_supplier = lambda: print('button')

    def __init__(self, id, pressed_supplier):
        self.btn_state_supplier = pressed_supplier
        self.id = id
        self.on_pressed = []
        self.on_released = []
        self.on_click = []

    def update(self):
        """
        this method must be called periodically.
        it updates the state of the button and runs everything it needs to
        :return:
        """
        self.prev_state = self.state
        self.state = self.btn_state_supplier(self.id)

        if self.is_clicked():
            self.clicked()

        elif self.is_pressed():
            self.pressed()
            # print('button {} pressed'.format(self.id))

        if self.is_released():
            self.released()
            # print('button {} released'.format(self.id))

    def set_clicked_callback(self, callback):
        self.on_click.append(callback)

    def set_pressed_callback(self, callback):
        self.on_pressed.append(callback)

    def set_released_callback(self, callback):
        self.on_released.append(callback)

    def is_clicked(self):
        """
        this method should be run periodically to check for button "clicks"
        a click is *not* the same as being pressed
        :return:
        """
        return not self.prev_state and self.state

    def is_pressed(self):
        return self.prev_state and self.state and not self.active

    def is_released(self):
        return self.prev_state and not self.state and self.active

    def pressed(self):
        self.active = True
        for c in self.on_pressed:
            c()

    def released(self):
        for c in self.on_released:
            c()
        self.active = False

    def clicked(self):
        for c in self.on_click:
            c()
