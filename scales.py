import tkinter
import math

import music
import fretboard
import colorsys

# TODO
# [...] clean up and bug fix
# [...] scale selection
# [...] separate UI from music logic
# [ ] piano canvas
# [ ] note canvas
# [ ] waveform canvas (sine)
# [ ] circle of fifths canvas
# [ ] midi input
# [ ] sine wave generation

# research
# circle of 5ths
# define key, define mode, define scale

window = tkinter.Tk()  # create window


# mouse_x, mouse_y = 0, 0

'''
# which frets to highlight
fret_marking = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21]

fret_spacing = 28  # how far apart to draw notes (horizontal)
string_spacing = 20  # how far apart to draw strings (vertical)
'''

# change current operating scale
def change_scale(scale_tonic_note):
    # change scale
    #global music.cur_scale
    music.cur_scale = music.get_scale(scale_tonic_note)

    print(scale_tonic_note)
    # refresh options for root to be notes in new scale
    previous_root = selectedRoot.get()
    '''
    optionMenuRoot["menu"].delete(0, 'end')
    for n in cur_scale:
        optionMenuRoot['menu'].add_command(label=n, command=lambda v=n: draw_fretboard(v))
    '''
    if previous_root in music.cur_scale:
        # print(previous_root.get() + ' in new scale')
        selectedRoot.set(previous_root)
    else:
        print('reset root to first note in scale')
        selectedRoot.set(music.cur_scale[0])

    # update fretboard
    myfretboard.draw_fretboard(scale_tonic_note)

'''
# draws a guitar string with notes
def draw_string(open_note, octave, triad, x, y):
    # draw line for string
    canvas.create_line(0, y, canvas['width'], y, fill='#007777')

    # starting note for the string
    note_string = music.notes.index(open_note)

    print('drawing string: ' + open_note + str(octave))
    for fret in range(len(music.notes) * 2):
        # calculate spacing between notes
        pos_x = (fret * fret_spacing) + x
        pos_y = y
        radius = 9

        # get note based on string position(fret),
        fret_oct = octave + math.floor((note_string + fret) / len(music.notes))
        fret_note = music.notes[(note_string + fret) % len(music.notes)]
        fret_frequency = str(round(note_map[fret_note + str(fret_oct)]))

        color = get_color_for_octave(fret_oct)
        # canvas.create_rectangle(pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius, fill=color)

        # highlight triads
        if fret_note in triad:
            canvas.create_text(pos_x, pos_y, text=fret_note, fill=color)
            if fret_note == triad[0]:
                # mark root note
                canvas.create_rectangle(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius, outline=color)
            else:
                # mark triad note
                canvas.create_oval(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius, outline=color)
        else:
            canvas.create_text(pos_x, pos_y, text=fret_note, fill='#333333')

        # show frequency
        canvas.create_text(pos_x, pos_y+7, text=fret_frequency, font=("Purisa", 9), fill='white')


def get_color_for_octave(octave):
    #colorsys.rgb_to_hls(1, 0, 0)
    if octave == 1:
        return '#9400D3'
    elif octave == 2:
        return '#4B0082'
    elif octave == 3:
        return '#0000FF'
    elif octave == 4:
        return '#00FF00'
    elif octave == 5:
        return '#FFFF00'
    elif octave == 6:
        return '#FF0000'
    else:
        return 'black'


# draws background and frets
def draw_fret_backing(x):
    # draw background
    canvas.create_rectangle(0, 0, canvas['width'], canvas['height'], fill='#777777')

    for fret in range(len(music.notes) * 2):
        pos_x = (fret * fret_spacing) + x

        # highlight frets
        if fret in fret_marking:
            canvas.create_rectangle(pos_x - fret_spacing/2, 0, pos_x + fret_spacing/2, canvas["height"], fill='#999999')

        # draw fret number
        canvas.create_text(pos_x, string_spacing * 7, text=fret, fill='#007777')


# draws fretboard with guitar strings and notes
def draw_fretboard(triad_root_note):
    # get the triad from the scale
    triad = music.get_triad(music.cur_scale.index(triad_root_note), music.cur_scale)
    print('drawing: ' + triad_root_note + ' -> ' + str(triad))
    print('in key: ' + str(music.cur_scale))
    x = 20

    # draw background and highlight frets
    draw_fret_backing(x)

    global mouse_x, mouse_y
    print('{}, {}'.format(mouse_x, mouse_y))
    canvas.create_line(mouse_x, 0, mouse_x, canvas['height'], fill="red", dash=(4, 4))
    canvas.create_line(0, mouse_y, canvas['width'], mouse_y, fill="red", dash=(4, 4))

    # draw each string (standard guitar tuning)
    draw_string('E', 4, triad, x, string_spacing * 1)
    draw_string('B', 3, triad, x, string_spacing * 2)
    draw_string('G', 3, triad, x, string_spacing * 3)
    draw_string('D', 3, triad, x, string_spacing * 4)
    draw_string('A', 2, triad, x, string_spacing * 5)
    draw_string('E', 2, triad, x, string_spacing * 6)
'''

# initialize with c major
music.cur_scale = music.get_scale('C')
#note_map = music.create_freq_map()

# drop down option menu to select root note of triad
selectedRoot = tkinter.StringVar()
selectedRoot.set(music.cur_scale[0])  # init with first note in scale
#optionMenuRoot = tkinter.OptionMenu(window, selectedRoot, *scale, command=change_root)# draw_fretboard)
#optionMenuRoot.pack()  # add menu to window

# drop down menu for scale
selectedScale = tkinter.StringVar()
selectedScale.set(music.notes[music.notes.index('C')])  # init with C (c major scale)
optionMenuScale = tkinter.OptionMenu(window, selectedScale, *music.notes, command=change_scale)
optionMenuScale.pack()  # add to window


# canvas as drawing surface to for fretboard
# canvas = tkinter.Canvas(window, width=800, height=150, bd=2, relief=tkinter.SUNKEN)
myfretboard = fretboard.Fretboard(window, 800, 150)
myfretboard.canvas.pack()  # add canvas to window


'''
def motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y
    # print('{}, {}'.format(mouse_x, mouse_y))
    draw_fretboard(selectedRoot.get())

canvas.bind('<Motion>', motion)  # test
'''


# draw fretboard
#myfretboard.draw_fretboard(selectedRoot.get())
change_scale(selectedRoot.get())

# start the window
window.mainloop()
