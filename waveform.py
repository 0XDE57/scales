import tkinter
import math
import util
import time

class WaveForm:
    def __init__(self, tk_main, window, w, h):
        self.tk_mainwindow = tk_main
        self.canvas = tkinter.Canvas(window, width=w, height=h)#, bd=2, relief=tkinter.SOLID)
        # Create a image, this acts as the canvas
        self.img = tkinter.PhotoImage(width=w, height=h)

        # Put the image on the canvas
        self.canvas.create_image((w / 2, h / 2), image=self.img, state="normal")

        self.scale = 1000
        self.active_notes = []

    def draw(self):
        if len(self.active_notes) == 0:
            self.canvas.delete('all')
            self.tk_mainwindow.after(200, self.draw)
            return

        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])
        center = canvas_height / 2
        amplitude = int(center * 0.9)

        '''
        # create a blank area for what where we are going to draw
        color_table = [["#000000" for x in range(canvas_width)] for y in range(canvas_height)]

        for x in range(canvas_width):
            y = int((math.sin(x * (frequency/self.scale)) * amplitude) + center)
            color_table[y][x] = "#ffff00"

        self.img.put(''.join("{" + (" ".join(str(color) for color in row)) + "} " for row in color_table), (0, int(canvas_height / 2 - amplitude)))
        '''
        self.canvas.delete('all')
        pos = 1
        for note in self.active_notes:
            pos += 1
            points = []
            for x in range(canvas_width):
                points.append(x)  # x
                points.append(int(math.sin(x * (note.frequency/self.scale)) * amplitude) + center)  # y

            self.canvas.create_line(0, center, canvas_width, center, fill='black')
            self.canvas.create_line(points, fill=util.get_color_for_octave(pos))
            self.canvas.create_text(10, pos*12, text=str(round(note.frequency, 2)), anchor='w')


        #print("draw freq:{0} at scale:{1} -> points={2}".format(round(self.frequency, 2), self.scale, len(points)/2))
        self.tk_mainwindow.after(100, self.draw)

