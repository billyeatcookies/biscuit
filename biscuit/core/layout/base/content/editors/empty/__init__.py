import tkinter as tk

from biscuit.core.components.utils import Frame

from .shortcuts import Shortcuts


class Empty(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(bd=0, relief=tk.FLAT, **self.base.theme.editors)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        try:
            self.logo = tk.Label(self, image=self.base.settings.res.logo, **self.base.theme.editors.labels)
            self.logo.grid(row=0, column=0)
        except tk.TclError:
            pass

        self.shortcuts = Shortcuts(self, **self.base.theme.editors)
        self.shortcuts.grid(row=1, column=0, pady=(0, 40))

        self.shortcuts.add_shortcut("Show all commands", ["Ctrl", "Shift", "p"])
        self.shortcuts.add_shortcut("Toggle terminal", ["Ctrl", "`"])
        self.shortcuts.add_shortcut("Open Folder", ["Ctrl", "Shift", "o"])

        self.bind("<Double-Button-1>", self.base.events.new_file)

    # TODO drop to open
    # def drop(self, event):
    #     if os.path.isfile(event.data):
    #         self.base.open_editor(event.data, exists=True)
    #     elif os.path.isdir(event.data):
    #         self.base.events.open_in_new_window(dir=event.data)
