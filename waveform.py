import tkinter
import math


class WaveForm:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h)#, bd=2, relief=tkinter.SOLID)

    def draw(self, frequency):
        center = int(self.canvas["height"]) / 2

        scale = 1000
        frequency /= scale
        amplitude = center * 0.9

        points = []
        for x in range(int(self.canvas["width"])):
            points.append(x)  # x
            points.append(int(math.sin(x * frequency) * amplitude) + center)  # y

        self.canvas.delete('all')
        self.canvas.create_line(0, center, int(self.canvas["width"]), center, fill='black')
        self.canvas.create_line(points, fill='blue')