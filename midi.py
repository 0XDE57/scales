import rtmidi_python as rtmidi
import threading


class MIDIthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.midi_in = rtmidi.MidiIn(b'in')  # fixed for python3 via: https://github.com/superquadratic/rtmidi-python/issues/17
        self.midi_in.open_port(0)

    def run(self):
        while True:
            message, delta_time = self.midi_in.get_message()
            if message:
                print(message, delta_time)
