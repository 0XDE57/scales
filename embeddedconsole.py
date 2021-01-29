import sys
import tkinter


class EmbeddedConsole:
    def __init__(self, window):
        self.frame = tkinter.Frame(window)
        self.entry = tkinter.Entry(self.frame)
        self.entry.pack()
        self.doIt = tkinter.Button(self.frame, text="Execute", command=self.on_enter)
        self.doIt.pack()
        self.output = tkinter.Text(self.frame)
        self.output.pack()
        sys.stdout = self

    def on_enter(self):
        print(eval(self.entry.get()))

    def write(self, txt):
        self.output.insert('end', str(txt))
