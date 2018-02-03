import tkinter

import music
import util


white_key_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_key_notes = ['C#', 'D#', 'F#', 'G#', 'A#']


class Key:
    def __init__(self, note, octave, rectangle_widget_id):
        if note in white_key_notes:
            self.key = 'white'
        else:
            self.key = 'black'
        
        self.note = music.Note(note, octave)
        self.widget_id = rectangle_widget_id



class Keyboard:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h, bd=2, relief=tkinter.SOLID)
        self.triad = None

    def object_click(self, event):
        item = event.widget.find_closest(event.x, event.y)
        print('event click', event.x, event.y, item)
        self.canvas.itemconfigure(item, fill='#333333')
        #self.canvas.itemconfigure(item, activefill='#333333')

        # hmm, look at: find_overlapping(x1, y1, x2, y2)

    def object_release(self, event):
        item = event.widget.find_closest(event.x, event.y)
        print('event release', event.x, event.y, item)

        self.canvas.itemconfigure(item, fill='white')
        #self.canvas.itemconfigure(item, activefill=)
        # hmm, look at: find_overlapping(x1, y1, x2, y2)

    def draw(self):
        print('rendering piano')
        starting_octave = 1
        # per octave
        white_keys = 7

        # black_keys = 5
        keyspan_octave = ['w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w']
        black_keys = [1, 2, 4, 5, 6]

        num_octaves = 6
        num_keys = white_keys * num_octaves
        key_width = (int(self.canvas["width"]) + 4) / num_keys
        for key in range(white_keys * num_octaves):
            pos_x = (key * key_width)
            note = white_key_notes[key % len(white_key_notes)]
            current_octave = starting_octave + int(key / 7)
            color_note = util.get_color_for_octave(current_octave)

            color_key = 'white'
            if self.triad is not None:
                if note in self.triad:
                    color_key = color_note
                    color_note = 'black'

            object_id = self.canvas.create_rectangle(pos_x,
                                                     0,
                                                     pos_x + key_width-1,
                                                     int(self.canvas["height"]) + 4,
                                                     fill=color_key, outline=color_note, activefill=color_note)

            #self.canvas.tag_bind(object_id, '<ButtonPress-1>', self.object_click)
            #self.canvas.tag_bind(object_id, '<ButtonRelease-1>', self.object_release)
            #self.canvas.tag_bind(object_id, '<Leave>', self.object_release)
            self.canvas.create_text(pos_x+key_width/2, int(self.canvas["height"])-10, text=note, fill=color_note)

        black_width = key_width * 0.7
        height = int(self.canvas["height"])*0.7
        count = 0
        for key in range(len(music.notes) * num_octaves):
            if key % white_keys in black_keys:
                pos_x = (key * key_width)
                note = black_key_notes[count % len(black_key_notes)]
                count += 1
                current_octave = starting_octave + int(key / 7)
                color_note = util.get_color_for_octave(current_octave)
                color_key = 'black'
                if self.triad is not None:
                    if note in self.triad:
                        color_key = color_note
                        color_note = 'black'

                self.canvas.create_rectangle(pos_x - black_width/2,
                                             0,
                                             pos_x + black_width/2,
                                             height,
                                             fill=color_key, outline=color_note, activefill=color_note)

                self.canvas.create_text(pos_x, 15, text=note, font=("Purisa", 9), fill=color_note)
        '''
        width = int(self.canvas["width"]) + 4
        height = int(self.canvas["height"]) + 4
        print(width)
        print(height)
        self.canvas.create_rectangle(0, 0, width, height, fill='black')'''

