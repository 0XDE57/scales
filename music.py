import math

# define music notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# modes/diatonic scale: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian
mode_ionian     = [2, 2, 1, 2, 2, 2, 1]  # major
mode_dorian     = [2, 1, 2, 2, 2, 1, 2]
mode_phrygian   = [1, 2, 2, 2, 1, 2, 2]
mode_lydian     = [2, 2, 2, 1, 2, 2, 1]
mode_mixolydian = [2, 2, 1, 2, 2, 1, 2]  # dominant
mode_aeolian    = [2, 1, 2, 2, 1, 2, 2]  # natural minor
mode_locrian    = [1, 2, 2, 1, 2, 2, 2]

intervals = [2, 2, 1, 2, 2, 2, 1]
# whole/half[w, w, h, w, w, w, h]
# tone/semi [T, T, S, T, T, T, S]

# predefined notes used for calculation: conforms to IPN (International Pitch Notation)
c2_freq = 65.40639
a4_freq = 440.0
a4_key_MIDI = 69

class Note:
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave
        # self.frequency =
        # self.cents =

def cents_from_frequency(freq):
    # C2 used as base "Low C"
    return cents_from_frequency(freq, c2_freq)


def cents_from_frequency(freq, base_freq):
    return (math.log(freq) - math.log(base_freq)) * 1200.0 * math.log2(math.e)


def frequency_to_note(freq):
    base_freq = c2_freq
    base_octave = 2
    total_cents = cents_from_frequency(freq, base_freq)

    while total_cents < 0:
        base_octave -= 1
        base_freq /= 2
        total_cents = cents_from_frequency(freq, base_freq)

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
    note = notes[note_num % 12]

    # print(note + str(octave) + ":" + str(cents))
    return note + str(octave)


def create_freq_map():
    frequency_map = {}

    for key_number in range(len(notes) * 9):
        # twelfth root of two
        # represents the frequency ratio of a semitone in twelve-tone equal temperament
        frequency = math.pow(2, (key_number - a4_key_MIDI) / 12) * a4_freq
        note = frequency_to_note(frequency)
        frequency_map[note] = frequency

    print('-' * 30)
    for key, value in frequency_map.items():
        if 'C' in key and '#' not in key:
            print("")
        print("{0:4} {1}".format(key, round(value, 3)))
    print('----')

    return frequency_map  # sorted(frequency_map.items(), key=lambda x: x[1])


# generate major scale
def get_scale(root):  # actually change key, scale is same, key is different?
    new_scale = []
    note = notes.index(root.upper())
    for x in range(len(intervals)):
        offset = intervals[x % len(intervals)]
        new_scale.append(notes[note % len(notes)])
        note += offset

    return new_scale


# create triad chord
def get_triad(root, scale):
    return [scale[(root + 0) % len(scale)],  # root | tonic
            scale[(root + 2) % len(scale)],  # third
            scale[(root + 4) % len(scale)]]  # fifth | dominant
            #scale[(root + 6) % len(scale)]]  # seventh



