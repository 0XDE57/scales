import tkinter
import math

import music
import util


# todo: dynamic fret spacing
# frets should not be evenly spaced, but mapped according to the tonal interval
# map interval to string length from 0-24+ frets.
# fret | interval | length | cents
# 0 (nut) | 2^(0/12) = 1 | = 0 | 0
# 3 | 2^(3/12) = 1.189 | = 0.159 | 300
# 5 | 2^(5/12) = 1.133 | = 0.251 | 500
# 7 | 2^(7/12) = 1.498 | = 0.333 | 700
# 12 (octave) | 2^(12/12) = 2 |  = 0.5 | 1200
# 24 | 2^(24/12) = |  = 2 | 2400
# ...


class Fretboard:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h, bd=2, relief=tkinter.SOLID)

        self.fret_marking = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21]  # which frets to highlight
        self.fret_spacing = 28  # how far apart to draw notes (horizontal)
        self.string_spacing = 20  # how far apart to draw strings (vertical)

        self.show_freq = False
        self.triad = None

    # draws a guitar string with notes
    def draw_string(self, open_note, octave, x, y):
        # draw line for string
        self.canvas.create_line(0, y, self.canvas['width'], y, fill='#007777')

        # starting note for the string
        note_string = music.notes.index(open_note)

        # print('drawing string: ' + open_note + str(octave))
        for fret in range(len(music.notes) * 2):
            # calculate spacing between notes
            pos_x = (fret * self.fret_spacing) + x
            pos_y = y
            radius = 9

            # get note based on string position(fret),
            fret_oct = octave + math.floor((note_string + fret) / len(music.notes))
            fret_note = music.notes[(note_string + fret) % len(music.notes)]

            color = util.get_color_for_octave(fret_oct)
            # canvas.create_rectangle(pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius, fill=color)

            # highlight triads
            if fret_note in self.triad:
                self.canvas.create_text(pos_x, pos_y, text=fret_note, fill=color, activefill='white')
                if fret_note == self.triad[0]:
                    # mark root note
                    self.canvas.create_rectangle(pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius, outline=color)
                else:
                    # mark triad note
                    self.canvas.create_oval(pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius, outline=color)
            else:
                self.canvas.create_text(pos_x, pos_y, text=fret_note, fill='#333333', activefill='white')

            # show frequency
            if self.show_freq:
                fret_frequency = str(round(music.note_map[fret_note + str(fret_oct)].frequency))
                self.canvas.create_text(pos_x, pos_y + 7, text=fret_frequency, font=("Purisa", 9), fill='white')

    # draws background and frets
    def draw_fret_backing(self, x):
        width = int(self.canvas['width']) + 4
        height = int(self.canvas['height']) + 4
        # draw background
        self.canvas.create_rectangle(0, 0, width, height, fill='#777777')

        for fret in range(len(music.notes) * 2):
            pos_x = (fret * self.fret_spacing) + x

            # highlight frets
            if fret in self.fret_marking:
                self.canvas.create_rectangle(
                    pos_x - self.fret_spacing / 2, 0,
                    pos_x + self.fret_spacing / 2, height,
                    fill='#999999')

            # draw fret number
            self.canvas.create_text(pos_x, self.string_spacing * 7, text=fret, fill='#007777')

    # draws fretboard with guitar strings and notes
    def draw(self):
        # get the triad from the scale
        # triad = music.get_triad(music.cur_scale.index(triad_root_note), music.cur_scale)
        # print('drawing: ' + triad_root_note + ' -> ' + str(triad))
        # print('in key: ' + str(music.cur_scale))
        x = 20

        # draw background and highlight frets
        self.draw_fret_backing(x)

        '''
        global mouse_x, mouse_y
        print('{}, {}'.format(mouse_x, mouse_y))
        self.canvas.create_line(mouse_x, 0, mouse_x, self.canvas['height'], fill="red", dash=(4, 4))
        self.canvas.create_line(0, mouse_y, self.canvas['width'], mouse_y, fill="red", dash=(4, 4))
        '''

        # draw each string (standard guitar tuning)
        self.draw_string('E', 4, x, self.string_spacing * 1)
        self.draw_string('B', 3, x, self.string_spacing * 2)
        self.draw_string('G', 3, x, self.string_spacing * 3)
        self.draw_string('D', 3, x, self.string_spacing * 4)
        self.draw_string('A', 2, x, self.string_spacing * 5)
        self.draw_string('E', 2, x, self.string_spacing * 6)
