import tkinter
import math
import colorsys

# TODO
# [...] clean up and bug fix
# [ ] scale selection
# [ ] separate UI from music logic
# [ ] piano canvas
# [ ] waveform canvas (sine)
# [ ] midi input
# [ ] sine wave generation

window = tkinter.Tk()  # create window

# define music notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
intervals = [2, 2, 1, 2, 2, 2, 1]
# whole/half[w, w, h, w, w, w, h]
# tone/semi [T, T, S, T, T, T, S]
cur_scale = []

mouse_x, mouse_y = 0, 0

# which frets to highlight
fret_marking = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21]

fret_spacing = 28  # how far apart to draw notes (horizontal)
string_spacing = 20  # how far apart to draw strings (vertical)


# predefined notes used for calculation
# conforms to IPN(International Pitch Notation)
c2_freq = 65.40639
a4_freq = 440.0


def cents_from_frequency(freq):
    # C2 used as base "Low C"
    return cents_from_frequency(freq, c2_freq)


def cents_from_frequency(freq, base_freq):
    return (math.log(freq) - math.log(base_freq)) * 1200.0 * math.log2(math.e)


def frequency_to_note(freq):
    base_freq = c2_freq
    base_octave = 2
    total_cents = cents_from_frequency(freq, base_freq)

    while total_cents < 0:
        base_octave -= 1
        base_freq /= 2
        total_cents = cents_from_frequency(freq, base_freq)

    note_num = math.floor(total_cents / 100)
    cents = round(total_cents - (note_num * 100))

    if cents == 100:
        cents = 0
        note_num += 1
    elif cents > 50:
        cents = cents - 100
        note_num += 1

    cents = abs(cents)
    octave = math.floor(note_num / 12) + base_octave
    note = notes[note_num % 12]

    # print(note + str(octave) + ":" + str(cents))
    return note + str(octave)


def create_freq_map():
    frequency_map = {}
    a4_key_MIDI = 69

    for key_number in range(len(notes) * 9):
        # twelfth root of two
        # represents the frequency ratio of a semitone in twelve-tone equal temperament
        frequency = math.pow(2, (key_number - a4_key_MIDI) / 12) * a4_freq
        note = frequency_to_note(frequency)
        frequency_map[note] = frequency

    print('-' * 30)
    for key, value in frequency_map.items():
        if 'C' in key and '#' not in key:
            print("")
        print("{0:4} {1}".format(key, round(value, 3)))
    print('----')

    return frequency_map  # sorted(frequency_map.items(), key=lambda x: x[1])


# generate major scale
def get_scale(root):
    # root = root.upper()
    new_scale = []
    note = notes.index(root.upper())
    for x in range(len(intervals)):
        offset = intervals[x % len(intervals)]
        new_scale.append(notes[note % len(notes)])
        note += offset

    return new_scale


#def change_root(note_root):


# change current operating scale
def change_scale(scale_tonic_note):
    # change scale
    global cur_scale
    cur_scale = get_scale(scale_tonic_note)
    print(scale_tonic_note)
    # refresh options for root to be notes in new scale
    previous_root = selectedRoot.get()
    '''
    optionMenuRoot["menu"].delete(0, 'end')
    for n in cur_scale:
        optionMenuRoot['menu'].add_command(label=n, command=lambda v=n: draw_fretboard(v))
    '''
    if previous_root in cur_scale:
        # print(previous_root.get() + ' in new scale')
        selectedRoot.set(previous_root)
    else:
        print('reset root to first note in scale')
        selectedRoot.set(cur_scale[0])

    # update fretboard
    draw_fretboard(scale_tonic_note)


# create triad cord
def get_triad(root):
    return [cur_scale[(root + 0) % len(cur_scale)],  # root
            cur_scale[(root + 2) % len(cur_scale)],  # third
            cur_scale[(root + 4) % len(cur_scale)]]  # fifth


# draws a guitar string with notes
def draw_string(open_note, octave, triad, x, y):
    # draw line for string
    canvas.create_line(0, y, canvas['width'], y, fill='#007777')

    # starting note for the string
    note_string = notes.index(open_note)

    print('drawing string: ' + open_note + str(octave))
    for fret in range(len(notes) * 2):
        # calculate spacing between notes
        pos_x = (fret * fret_spacing) + x
        pos_y = y
        radius = 9

        # get note based on string position(fret),
        relative_oct = octave + math.floor((note_string + fret) / len(notes))
        note = notes[(note_string + fret) % len(notes)]
        frequency = str(round(note_map[note + str(relative_oct)]))

        color = get_color_for_octave(relative_oct)
        # canvas.create_rectangle(pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius, fill=color)

        # highlight triads
        if note in triad:
            canvas.create_text(pos_x, pos_y, text=note, fill=color)
            if note == triad[0]:
                # mark root note
                canvas.create_rectangle(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius, outline=color)
            else:
                # mark triad note
                canvas.create_oval(pos_x-radius, pos_y-radius, pos_x+radius, pos_y+radius, outline=color)
        else:
            canvas.create_text(pos_x, pos_y, text=note, fill='#333333')

        # show frequency
        canvas.create_text(pos_x, pos_y+7, text=frequency, font=("Purisa", 9), fill='white')


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
    triad = get_triad(cur_scale.index(triad_root_note))
    print('drawing: ' + triad_root_note + ' -> ' + str(triad))
    print('in scale: ' + str(cur_scale))
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


# initialize with c major
cur_scale = get_scale('C')
note_map = create_freq_map()

# drop down option menu to select root note of triad
selectedRoot = tkinter.StringVar()
selectedRoot.set(cur_scale[0])  # init with first note in scale
#optionMenuRoot = tkinter.OptionMenu(window, selectedRoot, *scale, command=change_root)# draw_fretboard)
#optionMenuRoot.pack()  # add menu to window

# drop down menu for scale
selectedScale = tkinter.StringVar()
selectedScale.set(notes[notes.index('C')])  # init with C (c major scale)
optionMenuScale = tkinter.OptionMenu(window, selectedScale, *notes, command=change_scale)
optionMenuScale.pack()  # add to window


# canvas as drawing surface to for fretboard
canvas = tkinter.Canvas(window, width=800, height=150, bd=2, relief=tkinter.SUNKEN)
canvas.pack()  # add canvas to window


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
draw_fretboard(selectedRoot.get())


# start the window
window.mainloop()
