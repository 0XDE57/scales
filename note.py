class Note:
    def __init__(self, note, octave, frequency, cents, midi):
        self.note_letter = note
        self.octave = octave
        self.frequency = frequency
        self.cents = cents
        self.midi_ID = midi

    def get_note(self, freq):
        if freq:
            return self.note_letter + str(round(self.frequency, 2))
        else:
            return self.note_letter + str(self.octave)

    def to_string(self):
        return "{0:4} | {1:10} | {3:4}".format(self.get_note(False), round(self.frequency, 4), self.cents, self.midi_ID)
