import math

# define music notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# modes/diatonic scale: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian
# whole/half      [w, w, h, w, w, w, h]
# tone/semi       [T, T, S, T, T, T, S]
#mode_ionian     = [2, 2, 1, 2, 2, 2, 1]  # major
#mode_dorian     = [2, 1, 2, 2, 2, 1, 2]
#mode_phrygian   = [1, 2, 2, 2, 1, 2, 2]
#mode_lydian     = [2, 2, 2, 1, 2, 2, 1]
#mode_mixolydian = [2, 2, 1, 2, 2, 1, 2]  # dominant
#mode_aeolian    = [2, 1, 2, 2, 1, 2, 2]  # natural minor | relative minor
#mode_locrian    = [1, 2, 2, 1, 2, 2, 2]

#if aeolian and C -> c-minor

modes = {'Ionian':      [2, 2, 1, 2, 2, 2, 1],  # major
         'Dorian':      [2, 1, 2, 2, 2, 1, 2],
         'Phrygian':    [1, 2, 2, 2, 1, 2, 2],
         'Lydian':      [2, 2, 2, 1, 2, 2, 1],
         'Mixolydian':  [2, 2, 1, 2, 2, 1, 2],  # dominant
         'Aeolian':     [2, 1, 2, 2, 1, 2, 2],  # natural minor | relative minor
         'Locrian':     [1, 2, 2, 1, 2, 2, 2]}


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
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave
        self.frequency = frequencyMap[note + str(octave)]
        self.cents = 0

        diff_oct = (octave - 4) * 12
        diff_note = notes.index(note) - notes.index('A')
        self.midi_id = a4_key_MIDI + (diff_note + diff_oct)


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

    #print(note + str(octave) + ":" + str(cents))
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


frequencyMap = create_freq_map()