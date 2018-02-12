import rtmidi_python as rtmidi
import music


class MIDI:
    def __init__(self):
        self.midi_opened = False

        self.midi_in = rtmidi.MidiIn(b'in')  # fixed for python3 via: https://github.com/superquadratic/rtmidi-python/issues/17

        if not self.midi_in.ports:
            print('No midi devices found.')
            return
        else:
            for x in self.midi_in.ports:
                print(x)

        self.midi_in.callback = self.callback
        self.midi_in.open_port(0)

    def callback(self, message, time_stamp):
        midi_type = message[0]
        midi_note = message[1]
        midi_velocity = message[2]
        #print(str(message))
        if midi_type == 144:
            if midi_velocity == 0:
                print('Off: ' + music.note_map[midi_note].to_string())
            else:
                print('On:  ' + music.note_map[midi_note].to_string() + ' -> ' + str(midi_velocity))
        else:
            print(str(message))
