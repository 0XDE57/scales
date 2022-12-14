import math

# define music notes
notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

# mode intervals
# whole/half            [w, w, h, w, w, w, h]
# tone/semi             [T, T, S, T, T, T, S]
modes = {'Ionian':      (2, 2, 1, 2, 2, 2, 1),  # major
         'Dorian':      (2, 1, 2, 2, 2, 1, 2),
         'Phrygian':    (1, 2, 2, 2, 1, 2, 2),
         'Lydian':      (2, 2, 2, 1, 2, 2, 1),
         'Mixolydian':  (2, 2, 1, 2, 2, 1, 2),  # dominant
         'Aeolian':     (2, 1, 2, 2, 1, 2, 2),  # natural minor | relative minor
         'Locrian':     (1, 2, 2, 1, 2, 2, 2)}

# predefined notes used for calculation: conforms to IPN (International Pitch Notation)
c2_freq = 65.40639
a4_freq = 440.0
a4_key_MIDI = 69

scale_degrees = ['tonic',
                 'supertonic',
                 'mediant',
                 'subdominant',
                 'dominant',
                 'submediant',
                 'leading tone',
                 'tonic octive']


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
        return "| {0:4} | {1:10} | {3:4} |".format(self.get_note(False), round(self.frequency, 2), self.cents, self.midi_ID)


def frequency_to_cents(freq):
    # C2 used as base "Low C"
    return frequency_to_cents(freq, c2_freq)


def frequency_to_cents(freq, base_freq):
    # 1200 = 12 notes * 100 cents.
    return (math.log(freq) - math.log(base_freq)) * 1200.0 * math.log2(math.e)


def frequency_to_note(freq, midi_note):
    base_freq = c2_freq
    base_octave = 2
    total_cents = frequency_to_cents(freq, base_freq)

    while total_cents < 0:
        base_octave -= 1
        base_freq /= 2
        total_cents = frequency_to_cents(freq, base_freq)

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
    note_letter = notes[note_num % 12]

    return Note(note=note_letter, octave=octave, frequency=freq, cents=cents, midi=midi_note)


def midi_note_to_frequency(midi_note):
    # twelfth root of two = 2^(1/12) = 1.0594631
    # represents the frequency ratio of a semitone in twelve-tone equal temperament
    return a4_freq * math.pow(2, (midi_note - a4_key_MIDI) / 12)


def generate_notes():
    note_map = {}
    octaves = 15
    for midi_note in range(len(notes) * octaves):
        frequency = midi_note_to_frequency(midi_note)
        note = frequency_to_note(frequency, midi_note)
        note_map[midi_note] = note
        print(note.to_string())

    return note_map


# generate scale
def get_mode_of_scale(key_signature, mode_intervals):
    new_scale = []
    note = notes.index(key_signature.upper())
    for x in range(len(mode_intervals)):
        offset = mode_intervals[x % len(mode_intervals)]
        new_scale.append(notes[note % len(notes)])
        note += offset

    return new_scale


# create triad chord
def get_triad(root, scale):
    # root = key_signature
    return [scale[(root + 0) % len(scale)],  # root | tonic
            scale[(root + 2) % len(scale)],  # third | mediant
            scale[(root + 4) % len(scale)]]  # fifth | dominant
            #scale[(root + 6) % len(scale)]]  # seventh | leading tone


note_map = generate_notes()
