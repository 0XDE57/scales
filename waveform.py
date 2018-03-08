import tkinter
import math
import util
import time

class WaveForm:
    def __init__(self, tk_main, window, w, h):
        self.tk_mainwindow = tk_main
        self.canvas = tkinter.Canvas(window, width=w, height=h*2)#, bd=2, relief=tkinter.SOLID)
        # Create a image, this acts as the canvas
        self.img = tkinter.PhotoImage(width=w, height=h*2)

        # Put the image on the canvas
        self.canvas.create_image((w / 2, h / 2), image=self.img, state="normal")

        self.scale = 1000
        self.active_notes = []

    def draw(self):

        if len(self.active_notes) == 0:
            self.canvas.delete('all')
            self.tk_mainwindow.after(1, self.draw)
            return

        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])
        #self.canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill='black')
        center = canvas_height / 4
        amplitude = int(center * 0.9)

        '''
        # create a blank area for what where we are going to draw
        color_table = [["#000000" for x in range(canvas_width)] for y in range(canvas_height)]

        for x in range(canvas_width):
            y = int((math.sin(x * (frequency/self.scale)) * amplitude) + center)
            color_table[y][x] = "#ffff00"

        self.img.put(''.join("{" + (" ".join(str(color) for color in row)) + "} " for row in color_table), (0, int(canvas_height / 2 - amplitude)))
        '''
        # TODO: fix phase alignment of
        self.canvas.delete('all')
        pos = 1
        sin_wave_sum = []
        phase_offset = math.radians(270)
        for note in self.active_notes:
            sin_wave = []
            for x in range(int(canvas_width)):
                sin_wave.append(x)  # x
                y = int(math.sin(x * (note.frequency/self.scale) + phase_offset) * amplitude) + center
                sin_wave.append(y)  # y

                y += center*2

                if pos > 1:
                    sin_wave_sum[x*2+1] += y/len(self.active_notes)
                else:
                    sin_wave_sum.append(x)
                    sin_wave_sum.append(y / len(self.active_notes))

            #print(sin_wave)
            pos += 1
            color = util.get_color_for_octave(pos)#misleading use, not actualy octave, just using key index
            self.canvas.create_line(0, center, canvas_width, center, fill='black')
            self.canvas.create_line(sin_wave, fill=color)

        pos = 1
        for note in self.active_notes:
            self.canvas.create_text(10, pos * 12, text=note.to_string(), anchor='w', fill='black')
            pos += 1

        #print(sin_wave_sum)
        try:
            self.canvas.create_line(sin_wave_sum, fill='black')
        except:
            print(sin_wave_sum)  # TODO: fix. somethings wrong

        #print("draw freq:{0} at scale:{1} -> sin_wave={2}".format(round(self.frequency, 2), self.scale, len(sin_wave)/2))
        self.tk_mainwindow.after(1, self.draw)

