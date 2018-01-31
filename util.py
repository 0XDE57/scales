

def get_color_for_octave(octave):
    # colorsys.rgb_to_hls(1, 0, 0)
    if octave == 1:
        return '#9400D3'
    elif octave == 2:
        return '#4B0082'
    elif octave == 3:
        return '#0000FF'
    elif octave == 4:
        return '#00FF00'
    elif octave == 5:
        return '#FFFF00'
    elif octave == 6:
        return '#FF0000'
    else:
        return 'black'