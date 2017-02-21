import tkinter

window = tkinter.Tk()  # create window

# define music notes
notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
intervals = [2, 2, 1, 2, 2, 2, 1]
scale = []

# define c major scale
# scale_c_major = get_scale('C')['C', 'D', 'E', 'F', 'G', 'A', 'B']
# whole/half      w,   w,   h,   w,   w,   w,   h
# tone/semitone   T,   T,   S,   T,   T,   T,   S
#                 2,   2,   1,   2,   2,   2,   1

# which frets to highlight
fret_marking = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21]

fret_spacing = 25  # how far apart to draw notes (horizontal)
string_spacing = 20  # how far apart to draw strings (vertical)


# generate major scale
def get_scale(root):
    root = root.upper()
    new_scale = []
    note = notes.index(root)
    for x in range(len(intervals)):
        offset = intervals[x % len(intervals)]
        new_scale.append(notes[note % len(notes)])
        note += offset

    return new_scale


# change current operating scale
def change_scale(scale_tonic_note):
    # change scale
    global scale
    scale = get_scale(scale_tonic_note)

    # refresh options for root to be notes in new scale
    previous_root = selectedRoot.get()
    optionMenuRoot["menu"].delete(0, 'end')
    for n in scale:
        optionMenuRoot['menu'].add_command(label=n, command=lambda v=n: draw_fretboard(v))

    if previous_root in scale:
        # print(previous_root.get() + ' in new scale')
        selectedRoot.set(previous_root)
    else:
        print('reset root to first note in scale')
        selectedRoot.set(scale[0])

    # update fretboard
    draw_fretboard(selectedRoot.get())


# create triad cord
def get_triad(root):
    note_root  = scale[(root + 0) % len(scale)]
    note_third = scale[(root + 2) % len(scale)]
    note_fifth = scale[(root + 4) % len(scale)]
    return note_root + note_third + note_fifth


# draws a guitar string with notes
def draw_string(open_note, triad, x, y):
    # draw line for string
    canvas.create_line(0, y, canvas['width'], y, fill='#007777')

    # starting note for the string
    note_string = notes.index(open_note)
    for n in range(len(notes) * 2):
        # calculate spacing between notes
        pos_x = (n * fret_spacing) + x
        pos_y = y
        radius = 8

        # get note based on string position(fret),
        note = notes[(note_string + n) % len(notes)]

        # if note is a triad, mark/highlight it
        if note in triad:
            if note == triad[0]:
                # mark root note
                canvas.create_rectangle(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius)
            else:
                # mark triad note
                canvas.create_oval(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius)

            # draw triad note
            canvas.create_text(pos_x, pos_y, text=note, fill='white')
        else:
            # draw non-triad note
            canvas.create_text(pos_x, pos_y, text=note, fill='#333333')


# draws background and frets
def draw_fret_backing(x):
    # draw background
    canvas.create_rectangle(0, 0, canvas['width'], canvas['height'], fill='#777777')

    for fret in range(len(notes) * 2):
        pos_x = (fret * fret_spacing) + x

        # highlight frets
        if fret in fret_marking:
            canvas.create_rectangle(pos_x - fret_spacing/2, 0, pos_x + fret_spacing/2, canvas["height"], fill='#999999')

        # draw fret number
        canvas.create_text(pos_x, string_spacing * 7, text=fret, fill='#007777')


# draws fretboard with guitar strings and notes
def draw_fretboard(triad_root_note):
    # get the triad from the scale
    triad = get_triad(scale.index(triad_root_note))
    print('drawing: ' + triad_root_note + ' -> ' + triad)
    print('in scale: ' + str(scale))
    x = 20

    # draw background and highlight frets
    draw_fret_backing(x)

    # draw each string (standard guitar tuning)
    draw_string('E', triad, x, string_spacing * 1)
    draw_string('B', triad, x, string_spacing * 2)
    draw_string('G', triad, x, string_spacing * 3)
    draw_string('D', triad, x, string_spacing * 4)
    draw_string('A', triad, x, string_spacing * 5)
    draw_string('E', triad, x, string_spacing * 6)


# initialize with c major
scale = get_scale('C')

# drop down option menu to select root note of triad
selectedRoot = tkinter.StringVar()
selectedRoot.set(scale[0])  # init with first note in scale
optionMenuRoot = tkinter.OptionMenu(window, selectedRoot, *scale, command=draw_fretboard)
optionMenuRoot.pack()  # add menu to window

# drop down menu for scale
selectedScale = tkinter.StringVar()
selectedScale.set(notes[notes.index('C')])  # init with C (c major scale)
optionMenuScale = tkinter.OptionMenu(window, selectedScale, *notes, command=change_scale)
optionMenuScale.pack()  # add to window


# canvas as drawing surface to for fretboard
canvas = tkinter.Canvas(window, width=800, height=150, bd=2, relief=tkinter.SUNKEN)
canvas.pack()  # add canvas to window

# TODO
# -piano canvas
# -waveform canvas (sine)

# draw fretboard
draw_fretboard(selectedRoot.get())

# debug
# draw_fretboard('A')
# print(get_scale('C'))

# start the window
window.mainloop()
