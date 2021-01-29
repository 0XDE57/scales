import rtmidi


class MIDI:
    def __init__(self, callback):
        self.midi_opened = False

        self.midi_in = rtmidi.MidiIn()

        if not self.midi_in.get_ports():
            print('No midi devices found.')
            return
        else:
            print('detected midi devices:')
            for x in self.midi_in.get_ports():
                print(x)

        self.midi_in.set_callback(callback)
        self.midi_in.open_port(0)


