import tkinter

import music


class Keyboard:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h, bd=2, relief=tkinter.SOLID)

    def draw(self):
        print('rendering piano')
        # per octave
        white_keys = 7
        white_key_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        black_key_notes = ['C#', 'D#', 'F#', 'G#', 'A#']
        # black_keys = 5
        keyspan_octave = ['w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w']
        black_keys = [1, 2, 4, 5, 6]

        num_octaves = 4
        num_keys = white_keys * num_octaves
        key_width = (int(self.canvas["width"]) + 4) / num_keys
        for key in range(white_keys * num_octaves):
            pos_x = (key * key_width)
            self.canvas.create_rectangle(pos_x,
                                         0,
                                         pos_x + key_width,
                                         int(self.canvas["height"]) + 4,
                                         fill='white', activefill='#999999')

            note = white_key_notes[key % len(white_key_notes)]
            self.canvas.create_text(pos_x+key_width/2, int(self.canvas["height"])-10, text=note, fill='#333333')

        black_width = key_width * 0.7
        height = int(self.canvas["height"])*0.7
        count = 0
        for key in range(len(music.notes) * num_octaves):
            if key % white_keys in black_keys:
                pos_x = (key * key_width)
                self.canvas.create_rectangle(pos_x - black_width/2,
                                             0,
                                             pos_x + black_width/2,
                                             height,
                                             fill='black', activefill='#999999')

                note = black_key_notes[count % len(black_key_notes)]
                count += 1
                self.canvas.create_text(pos_x, 15, text=note, fill='white')
        '''
        width = int(self.canvas["width"]) + 4
        height = int(self.canvas["height"]) + 4
        print(width)
        print(height)
        self.canvas.create_rectangle(0, 0, width, height, fill='black')'''
