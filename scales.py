
import tkinter

import music
import fretboard
import keyboard
import waveform
import midi
import embeddedconsole

# TODO
# [ ] fix notation, eg: D Phrygian: [D D# F G A A# C] should be [D Eb F G A Bb C], check circle of fifths,
#     number of sharps and flats. the notes are still technically correct as they are the same
#     (at least in an equal-temperment scale, perhaps not in pythagorean scale as far as I currently understand?)
# [...] midi input/output
# [...] note highlight linking between keyboard and fretboard and waveform to display 1-1 mapping
# [ ] keyboard and fretboard canvas objects should be event based instead of re-added each change -> memory leak
# [ ] options for instruments
# [ ] circle of fifths canvas
# [ ] note/staff canvas
# [...] waveform canvas (sine)
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


def midi_input_handler(event, data=None):
    message = event[0]
    timestamp = event[1]
    # TODO: look up midi types and message ID's
    # looks like some midi keyboard use type 144 and velocity 0 for off, while others use type 128 for off
    print(str(timestamp) + ' ' + str(message))
    # 144 = note on
    # 128 = note off
    # 176 = modifier/knob?
    midi_type = message[0]
    midi_note = message[1]
    midi_velocity = message[2]

    wave.scale = tk_wave_scale_slider.get()
    if midi_type == 144:
        note_pressed = music.note_map[midi_note]
        if midi_velocity > 0:
            print('On:  ' + note_pressed.to_string() + ' -> ' + str(midi_velocity))
            if note_pressed not in wave.active_notes:
                wave.active_notes.append(note_pressed)
        else:
            print('Off: ' + note_pressed.to_string())
            wave.active_notes.remove(note_pressed)

    elif midi_type == 128:
        note_pressed = music.note_map[midi_note]
        print('Off: ' + note_pressed.to_string())
        wave.active_notes.remove(note_pressed)


'''
init 
'''
tk_main_window = tkinter.Tk()  # create window
tk_main_window.configure(background="red")
# console = embeddedconsole.EmbeddedConsole(tk_main_window)


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
# TODO:
# [ ] embed pyplot instead?
#       - https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html
# [ ] display multi-note combined wave -> sum
# [ ] option to center frequency instead of starting from left
# [ ] option to animate, roll the frequency
# [ ] option for velocity sensitive amplitude
# [ ] play with alternate wave function eg multiply, subtract instead of sum
# [ ] fourier transform to split sum wave, display visualizer/frequency gragh
#
# https://www.youtube.com/watch?v=spUNpyF58BY
# https://www.quora.com/Why-do-certain-musical-notes-sound-good-together-What-is-the-relationship-between-the-frequencies-of-their-waves
# https://www.youtube.com/watch?v=JDFa8TSn6vY
tk_labelframe_waveform_group = tkinter.LabelFrame(tk_main_window, text="waveform")
wave = waveform.WaveForm(tk_main_window, tk_labelframe_waveform_group, 800, 150)
wave.canvas.pack()
tk_wave_scale_slider = tkinter.Scale(tk_labelframe_waveform_group, from_=1, to=20000, orient='horizontal', length=800)
tk_wave_scale_slider.set(100)
tk_wave_scale_slider.pack()
tk_labelframe_waveform_group.pack()

# console.frame.pack()

'''
start
'''
wave.draw()  # start async event loop to render
midi = midi.MIDI(midi_input_handler)  # init mid, if found open and wait for events

# debug print scale,mode possibilities
for note in music.notes:
    print('Key sig = ' + note)
    for mode in music.modes.keys():
        print('\t' + str(mode) + ' -> ' + str(music.get_mode_of_scale(note, music.modes[mode])))

# init ui
update_ui()

# start the window
tk_main_window.mainloop()
