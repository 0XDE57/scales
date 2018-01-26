import tkinter


class Keyboard:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h, bd=2, relief=tkinter.SUNKEN)

    def draw(self):
        self.canvas.create_rectangle(1, 0, 2, self.canvas["height"], fill='#999999')
