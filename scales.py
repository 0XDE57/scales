import sys

import tkinter

import music
import fretboard
import keyboard
import waveform
import midi

# TODO
# [...] piano canvas
# [ ] midi input/output
# [...] note highlight linking between keyboard and fretboard to display 1-1 mapping
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
'''
TODO: figure out structure
instrument -> piano
instrument -> guitar
note -> key(y) -> keyboard
note -> fret/string(x,y) -> fretboard

note -> letter, octave, frequency, cents, midi_key

key -> rectangle widget, note, state(highlight, focus, click, 
fret -> text widget with circle / rect outline, hmm...
'''


class EmbeddedConsole:
    def __init__(self, window):
        self.frame = tkinter.Frame(window)
        self.entry = tkinter.Entry(self.frame)
        self.entry.pack()
        self.doIt = tkinter.Button(self.frame, text="DoIt", command=self.onEnter)
        self.doIt.pack()
        self.output = tkinter.Text(self.frame)
        self.output.pack()
        sys.stdout = self

    def onEnter(self):
        print(eval(self.entry.get()))

    def write(self, txt):
        self.output.insert('end', str(txt))


def update_ui(*args):
    scale_tonic_note = tk_stringvar_selected_tonic.get()
    mode = tk_mode.get()

    global cur_scale
    cur_scale = music.get_mode_of_scale(scale_tonic_note, music.modes[mode])
    triad = music.get_triad(cur_scale.index(scale_tonic_note), cur_scale)

    print(scale_tonic_note + ' -> ' + str(triad))
    print('mode: ' + mode + '' + str(cur_scale))

    tk_entry_scale_text.delete(0, 'end')
    tk_entry_scale_text.insert(0, cur_scale)
    tk_entry_triad_text.delete(0, 'end')
    tk_entry_triad_text.insert(0, triad)

    # update instruments
    guitar.show_freq = tk_intvar_show_freq.get()
    guitar.triad = triad
    guitar.draw()

    piano.triad = triad
    piano.draw()

    #wave.draw()


def callback(message, time_stamp):
    midi_type = message[0]
    midi_note = message[1]
    midi_velocity = message[2]

    if midi_type == 144:
        if midi_velocity == 0:
            print('Off: ' + music.note_map[midi_note].to_string())
        else:
            print('On:  ' + music.note_map[midi_note].to_string() + ' -> ' + str(midi_velocity))
            wave.draw(music.note_map[midi_note].frequency)
    else:
        print(str(message))


'''
init 
'''
tk_main_window = tkinter.Tk()  # create window
# console = EmbeddedConsole(tk_main_window)


'''
build options section
'''
tk_labelframe_options = tkinter.LabelFrame(tk_main_window, text="scales")
tk_labelframe_options.pack(fill="both", expand="yes")

# drop down option menu to select root note of triad
tk_stringvar_selected_tonic = tkinter.StringVar()
tk_stringvar_selected_tonic.set(music.notes[music.notes.index('C')])  # init with C (c major scale)
tk_optionmenu_tonic_selection = tkinter.OptionMenu(tk_labelframe_options, tk_stringvar_selected_tonic, *music.notes, command=update_ui)
tk_optionmenu_tonic_selection.pack()
tk_mode = tkinter.StringVar()
tk_mode.set(next(iter(music.modes.keys())))
tk_optionmenu_mode_selection = tkinter.OptionMenu(tk_labelframe_options, tk_mode, *music.modes.keys(), command=update_ui)
tk_optionmenu_mode_selection.pack()

# scale and triad display
tk_entry_triad_text = tkinter.Entry(tk_labelframe_options)
tk_entry_scale_text = tkinter.Entry(tk_labelframe_options)
tk_entry_triad_text.pack()
tk_entry_scale_text.pack()


'''
add instruments
'''
# add guitar
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
tk_labelframe_guitar_group = tkinter.LabelFrame(tk_main_window, text='guitar')
guitar = fretboard.Fretboard(tk_labelframe_guitar_group, 800, 150)
guitar.canvas.pack()
tk_intvar_show_freq = tkinter.IntVar()
tk_checkbutton_show_freq = tkinter.Checkbutton(tk_labelframe_guitar_group, text='Show Frequency', variable=tk_intvar_show_freq, command=update_ui)
tk_checkbutton_show_freq.pack()
tk_labelframe_guitar_group.pack()

# piano
# TODO:
# [ ] toggle show frequency
# [ ] number of octaves
# [ ] toggle color octave
# [ ] starting octave
tk_labelframe_piano_group = tkinter.LabelFrame(tk_main_window, text="piano")
piano = keyboard.Keyboard(tk_labelframe_piano_group, 800, 150)
piano.canvas.pack()
tk_labelframe_piano_group.pack()

# frequency
# TODO: this is place holder test, embed pyplot instead
# https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html
# https://www.youtube.com/watch?v=spUNpyF58BY
# https://www.quora.com/Why-do-certain-musical-notes-sound-good-together-What-is-the-relationship-between-the-frequencies-of-their-waves
# https://www.youtube.com/watch?v=JDFa8TSn6vY
tk_labelframe_waveform_group = tkinter.LabelFrame(tk_main_window, text="waveform")
wave = waveform.WaveForm(tk_labelframe_waveform_group, 800, 150)
wave.canvas.pack()
tk_labelframe_waveform_group.pack()


#console.frame.pack()

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

'''
start
'''
midi = midi.MIDI(callback)


for note in music.notes:
    print('Key sig = ' + note)
    for mode in music.modes.keys():
        print('\t' + str(mode) + ' -> ' + str(music.get_mode_of_scale(note, music.modes[mode])))

# draw
update_ui()

# start the window
tk_main_window.mainloop()
