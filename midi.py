import rtmidi


class MIDI:
    def __init__(self, callback):
        self.midi_opened = False

        self.midi_in = rtmidi.MidiIn()

        if not self.midi_in.get_ports():
            print('No midi devices found.')
            return

        print('detected midi devices:')
        for ports in self.midi_in.get_ports():
            print(ports)

        # open first device by default
        self.midi_in.set_callback(callback)
        self.midi_in.open_port(0)

        self.midi_opened = True
