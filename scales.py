import tkinter

import music
import fretboard
import keyboard
import midi

# TODO
# [...] piano canvas
# [...] midi input/output
# [ ] note highlight linking between keyboard and fretboard to display 1-1 mapping
# [ ] mode selection -> shifting intervals (Ionian,Dorian,Phrygian,etc...)
# [ ] options for instruments
# [ ] circle of fifths canvas
# [ ] note/staff canvas
# [ ] waveform canvas (sine)
# [ ] sine wave generation
# [ ] clean up UI layout
# [ ] research
#       - circle of 5ths
#       - define key, define mode, define scale (i am confused, they are all the same but different?)
#       - what makes a scale or chord minor or major?


# change current operating scale
def change_scale(scale_tonic_note):
    # change scale
    global cur_scale
    cur_scale = music.get_scale(scale_tonic_note)
    triad = music.get_triad(cur_scale.index(scale_tonic_note), cur_scale)
    print(scale_tonic_note + ' -> ' + str(triad))
    print('in key: ' + str(cur_scale))

    # refresh options for root to be notes in new scale
    previous_root = selectedRoot.get()
    '''
    optionMenuRoot["menu"].delete(0, 'end')
    for n in cur_scale:
        optionMenuRoot['menu'].add_command(label=n, command=lambda v=n: draw_fretboard(v))
    '''
    scale_text.delete(0, 'end')
    scale_text.insert(0, cur_scale)
    triad_text.delete(0, 'end')
    triad_text.insert(0, triad)

    if previous_root in cur_scale:
        # print(previous_root.get() + ' in new scale')
        selectedRoot.set(previous_root)
    else:
        print('reset root to first note in scale')
        selectedRoot.set(cur_scale[0])

    # update instruments
    guitar.show_freq = sf.get()
    guitar.draw_fretboard(triad)

    piano.draw()


window = tkinter.Tk()  # create window

# initialize with c major
cur_scale = music.get_scale('C')

option_group = tkinter.LabelFrame(window, text="scales")
option_group.pack(fill="both", expand="yes")


# drop down option menu to select root note of triad
selectedRoot = tkinter.StringVar()
selectedRoot.set(cur_scale[0])  # init with first note in scale
#optionMenuRoot = tkinter.OptionMenu(window, selectedRoot, *scale, command=change_root)# draw_fretboard)
#optionMenuRoot.pack()  # add menu to window

# drop down menu for scale
selectedScale = tkinter.StringVar()
selectedScale.set(music.notes[music.notes.index('C')])  # init with C (c major scale)
optionMenuScale = tkinter.OptionMenu(option_group, selectedScale, *music.notes, command=change_scale)
optionMenuScale.pack()  # add to window

triad_text = tkinter.Entry(option_group)
scale_text = tkinter.Entry(option_group)
triad_text.pack()
scale_text.pack()


# add instruments
guitar_group = tkinter.LabelFrame(window, text='guitar')
guitar = fretboard.Fretboard(guitar_group, 800, 150)
guitar.canvas.pack()
sf = tkinter.IntVar()
show_freq = tkinter.Checkbutton(guitar_group, text='Show Frequency', variable=sf, command=change_scale)
show_freq.pack()
# TODO:
# [ ] toggle draw note
# [ ] toggle include octave
# [ ] toggle color octave
# [ ] toggle draw fret number
# [ ] toggle show non-highlighted notes
# [ ] pick strings/octaves
# [ ] add/remove strings
# [ ] load presets eg:
#       - guitar6 = [E4, B3, G3, D3, A2, E2]
#       - guitar6dropD = [D4, B3, G3, D3, A2, E2]
#       - bass4 = [G2, D2, A1, E1]
#       - base5 = [G2, D2, A1, E1, B0]
guitar_group.pack()


piano_group = tkinter.LabelFrame(window, text="piano")
piano = keyboard.Keyboard(piano_group, 800, 150)
# TODO:
# [ ] number of octaves
# [ ] toggle color octave
piano.canvas.pack()
piano_group.pack()


'''
mouse_x, mouse_y = 0, 0
def motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y
    # print('{}, {}'.format(mouse_x, mouse_y))
    draw_fretboard(selectedRoot.get())

canvas.bind('<Motion>', motion)  # test
'''


#midi = midi.MIDIthread();
#midi.start();

# draw fretboard
change_scale(selectedRoot.get())

# start the window
window.mainloop()
