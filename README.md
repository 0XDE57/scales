# scales
a simple music learning tool

an experimental project with the goal of learning music theory, and implenting what I learn into this toy
![screenshot](/documentation/ui.png)

## How does it work? 
Documentation in the [wiki](https://github.com/0XDE57/scales/wiki/How-to-calculate-notes-and-frequencies%3F)

## dependencies
- Python
- tkinter
- python-rtmidi (https://pypi.org/project/python-rtmidi/)

Tested with python 3.10 and python-rtmidi 1.4.9 

Turns out there are now a couple flavours of rtmidi for python in pip with very similar package names.
* rtmidi
* rtmidi2: Based on rtmidi-python
* rtmidi-python: Python wrapper for RtMidi, the lightweight, cross-platform MIDI I/O library. For Linux, Mac OS X and Windows.
* python-rtmidi: A Python binding for the RtMidi C++ library implemented using Cython.

Installing the incorrect one will cause compile errors. 

In older python this used to work with **rtmidi-python**, but now runs on **python-rtmidi**. 
