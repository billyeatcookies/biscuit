# TODO Palette
#   - working commands
#   - sub menus


import tkinter as tk

from biscuit.core.components.utils import Frame, Toplevel

from .actionset import ActionSet
from .item import PaletteItem
from .searchbar import Searchbar


class Palette(Toplevel):
    """
    Palette

    Palette is an action menu centered horizontally and aligned to top of root.
    They contain a list of actions.

    +----------------------------------------------+
    |  \   | search                         |  \   |
    |   \  +--------------------------------+   \  |
    |    \    \    \    \    \    \    \    \    \ |
    |\    \    \    \    \    \    \    \    \    \|
    | \    \    \    \    \    \    \    \    \    |
    |  \    \    \    \    \    \    \    \    \   |
    |   \    \    \    \    \    \    \    \    \  |
    +----------------------------------------------+
    """
    def __init__(self, master, items=None, width=60, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(pady=1, padx=1, bg=self.base.theme.border)

        self.container = Frame(self, **self.base.theme.palette, padx=5, pady=5)
        self.container.pack(fill=tk.BOTH)

        self.width = round(width * self.base.scale)
        self.active = False

        self.withdraw()
        self.overrideredirect(True)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.row = 1
        self.selected = 0

        self.shown_items = []

        self.actionsets = []
        self.active_set = None
        self.add_search_bar()
        
        self.configure_bindings()

    def register_actionset(self, actionset):
        self.actionsets.append(actionset)
    
    def generate_help_actionset(self):
        self.help_actionset = ActionSet("Help", "?")
        for i in self.actionsets:
            i = i() # get the actionset
            if i.prompt:
                self.help_actionset.append((i.prompt, lambda _, i=i: self.after(50, self.show_prompt, i.prompt), i.description))
    
        self.register_actionset(lambda: self.help_actionset)

    def add_item(self, text, command, *args, **kwargs):
        new_item = PaletteItem(self.container, text, command, *args, **kwargs)
        new_item.grid(row=self.row, sticky=tk.EW)
        
        self.shown_items.append(new_item)

        self.row += 1
        self.refresh_selected()
        return new_item

    def add_search_bar(self):
        self.searchbar = Searchbar(self.container)
        self.searchbar.grid(row=0, sticky=tk.EW, pady=(1, 7), padx=1)
    
    def configure_bindings(self):
        self.bind("<FocusOut>", self.hide)
        self.bind("<Escape>", self.hide)

        self.row += 1
        self.refresh_selected()
    
    def pick_actionset(self, actionset):
        self.active_set = actionset
    
    def pick_file_search(self):
        self.active_set = self.base.explorer.get_actionset()
        
    def choose(self, *_):
        #TODO pass the term to the function as argument (for input requiring commands)
        self.shown_items[self.selected].command(self.searchbar.term)
        self.hide()
        
    def get_items(self):
        return self.active_set
    
    def hide(self, *args):
        self.withdraw()
        self.reset()
        
    def hide_all_items(self):
        for i in self.shown_items:
            i.destroy()
        
        self.shown_items = []
        self.row = 1
    
    def reset_selection(self):
        self.selected = 0
        self.refresh_selected()

    def refresh_selected(self):
        if not self.shown_items:
            return

        for i in self.shown_items:
            i.deselect()
        
        try:
            self.shown_items[self.selected].select()
        except IndexError as e:
            self.base.logger.error(f"Command '{self.selected}' doesnt exist: {e}")
    
    def reset(self):
        self.searchbar.clear()
        self.reset_selection()

    def search_bar_enter(self, *args):
        self.choose()
        return "break"
    
    def show_no_results(self):
        self.hide_all_items()
        self.reset_selection()
        self.add_item("No results found", lambda _:...)

    def select(self, delta):
        self.selected += delta
        self.selected = min(max(0, self.selected), len(self.shown_items) - 1)
        self.refresh_selected()
    
    def show_items(self, items):
        self.hide_all_items()

        for i in items[:10]:
            item = self.add_item(*i)
            item.mark_term(self.searchbar.term)

        self.reset_selection()

    def show_prompt(self, prompt):
        self.update_idletasks()
        
        x = self.master.winfo_rootx() + int((self.master.winfo_width() - self.winfo_width())/2)
        y = self.master.winfo_rooty() + self.base.menubar.winfo_height()
        self.geometry(f"+{x}+{y}")
        self.deiconify()
        
        self.focus_set()
        self.searchbar.focus()
        self.searchbar.add_prompt(prompt)
