import rtmidi_python as rtmidi
import music


class MIDI:
    def __init__(self, callback):
        self.midi_opened = False

        self.midi_in = rtmidi.MidiIn(b'in')  # fixed for python3 via: https://github.com/superquadratic/rtmidi-python/issues/17

        if not self.midi_in.ports:
            print('No midi devices found.')
            return
        else:
            print('detected midi devices:')
            for x in self.midi_in.ports:
                print(x)

        self.midi_in.callback = callback # self.callback
        self.midi_in.open_port(0)


