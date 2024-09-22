# scales
a simple music learning tool

an experimental project with the goal of learning music theory, and implementing what I learn into this toy
![screenshot](/documentation/ui.png)

## How does it work? 
Documentation in the [wiki](https://github.com/0XDE57/scales/wiki/How-to-calculate-notes-and-frequencies%3F)

## dependencies
- Python
- tkinter
- python-rtmidi (https://github.com/SpotlightKid/python-rtmidi)

## build and run
1. install python 3.
2. install python-rtmidi library from pip:
`pip install python-rtmidi`
3. run:
`python scales.py`


Note: Turns out there are a multiple variants of rtmidi available in pip with very similar package names (rtmidi, rtmidi2, rtmidi-python, python-rtmidi).
Installing the incorrect one will cause compile errors. The correct one is **python-rtmidi**. 

(last tested with python 3.10 and python-rtmidi 1.4.9)
