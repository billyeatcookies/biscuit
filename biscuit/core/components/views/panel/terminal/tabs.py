import tkinter as tk

from biscuit.core.components.utils import Frame

from .tab import Tab


class Tabs(Frame):
    def __init__(self, master, width=170, *args, **kwargs):
        super().__init__(master, width=width, *args, **kwargs)
        self.pack_propagate(False)
        self.config(**self.base.theme.views.panel.terminal)

        self.tabs = []
        self.active_tab = None

    def add_tab(self, view):
        tab = Tab(self, view)
        tab.pack(fill=tk.X)
        self.tabs.append(tab)

        tab.select()

    def set_active_tab(self, selected_tab):
        self.active_tab = selected_tab
        for tab in self.tabs:
            if tab != selected_tab:
                tab.deselect()

    def clear_all_tabs(self):
        for tab in self.tabs:
            tab.destroy()
        
        self.tabs.clear()

    def close_active_tab(self):
        self.close_tab(self.active_tab)
    
    def close_tab(self, tab):
        i = self.tabs.index(tab)
        self.tabs.remove(tab)
        tab.terminal.grid_forget()
        self.master.delete_terminal(tab.terminal)
        tab.destroy()
        
        if self.tabs:
            if i < len(self.tabs):
                self.tabs[i].select()
            else:
                self.tabs[i-1].select()
        else:
            self.active_tab = None
        self.master.refresh()