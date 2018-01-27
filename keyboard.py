import tkinter

import music


class Keyboard:
    def __init__(self, window, w, h):
        self.canvas = tkinter.Canvas(window, width=w, height=h, bd=2, relief=tkinter.SOLID)

    def draw(self):
        # per octave
        white_keys = 7
        black_keys = 5
        keyspan_octave = ['w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w']
        test = [1, 2, 4, 5, 6]


        num_octaves = 3
        num_keys = white_keys * num_octaves
        key_width = (int(self.canvas["width"]) + 4) / num_keys
        for key in range(white_keys * num_octaves):
            pos_x = (key * key_width)
            self.canvas.create_rectangle(pos_x,
                                         0,
                                         pos_x + key_width,
                                         int(self.canvas["height"]) + 4,
                                         fill='white', activefill='#999999')
        black_width = key_width * 0.7
        for key in range(12 * num_octaves):
            if key % white_keys in test:
                pos_x = (key * key_width)
                self.canvas.create_rectangle(pos_x - black_width/2,
                                             0,
                                             pos_x + black_width/2,
                                             int(self.canvas["height"])*0.7,
                                             fill='black', activefill='#999999')
        '''
        width = int(self.canvas["width"]) + 4
        height = int(self.canvas["height"]) + 4
        print(width)
        print(height)
        self.canvas.create_rectangle(0, 0, width, height, fill='black')'''
