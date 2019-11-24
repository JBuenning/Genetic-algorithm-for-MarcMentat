import shape
import tkinter
import random

class Algorithm:
    def __init__(self):
        self.name = self.get_name()
        self.activated = True
        self.default_settings()

    def default_settings(self):
        raise NotImplementedError

    def get_settings_frame(self, master): #has to return settings_frame
        frame = tkinter.Frame(master)
        label = tkinter.Label(frame, text='no settings available')
        label.pack()
        return frame

    def get_name(self):
        raise NotImplementedError

    def get_description(self):
        return 'no descriptin available'