import platform
import tkinter as tk

from biscuit import __version__
from biscuit.core.components.utils import Frame, IconButton, Label

from .item import MenubarItem


class Menubar(Frame):
    """
    Root frame holds Menubar, BaseFrame, and Statusbar
    .
    App
    └── Root
        ├── Menubar
        ├── BaseFrame
        └── Statusbar
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.menus = []
        self.events = self.base.events

        if platform.system() == 'Windows':
            close = IconButton(self, icon='chrome-close', iconsize=12, padx=15, pady=8, event=self.events.quit)
            close.config(activebackground='#e81123', activeforeground="white")
            close.pack(side=tk.RIGHT, fill=tk.Y, padx=0)
            
            IconButton(self, icon='chrome-maximize', iconsize=12, icon2='chrome-restore', padx=15, pady=8, event=self.events.toggle_maximize).pack(side=tk.RIGHT, fill=tk.Y, padx=0)
            IconButton(self, icon='chrome-minimize', iconsize=12, padx=15, pady=8, event=self.events.minimize).pack(side=tk.RIGHT, fill=tk.Y, padx=0)
            self.config_bindings()

        self.title_lbl = Label(self, **self.base.theme.layout.menubar.title)
        self.update_idletasks()
        self.set_title()

        self.config(**self.base.theme.layout.menubar)
        self.add_menus()
    
    def set_title(self, title=None):
        self.title_lbl.config(text=f"{title} - Biscuit (v{__version__})" 
                              if title else f"Biscuit (v{__version__})")
        self.reposition_title()
    
    def reposition_title(self):
        x = self.winfo_x() + (self.winfo_width() - self.title_lbl.winfo_width())/2
        y = self.winfo_y() + (self.winfo_height() - self.title_lbl.winfo_height())/2
        
        self.title_lbl.place_forget()
        self.title_lbl.place(x=x, y=y)

    def config_bindings(self):
        self.bind('<Map>', self.events.window_mapped)
        self.bind("<Button-1>", self.startMove)
        self.bind("<ButtonRelease-1>", self.stopMove)
        self.bind("<B1-Motion>", self.moving)

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def moving(self,event):
        x = (event.x_root - self.x - self.winfo_rootx() + self.winfo_rootx())
        y = (event.y_root - self.y - self.winfo_rooty() + self.winfo_rooty())
        self.base.geometry(f"+{x}+{y}")
        
    def add_menu(self, text):
        new_menu = MenubarItem(self, text)
        new_menu.pack(side=tk.LEFT, fill=tk.BOTH)
        self.menus.append(new_menu.menu)
        
        return new_menu.menu

    def add_menus(self):
        self.add_file_menu()
        self.add_edit_menu()
        self.add_view_menu()

    # TODO: Implement events for the menu items
    def add_file_menu(self):
        events = self.events

        file_menu = self.add_menu("File")
        file_menu.add_item("New File", events.new_file)
        file_menu.add_item("New Window", events.new_window)
        file_menu.add_separator()
        file_menu.add_item("Open File", events.open_file)
        file_menu.add_item("Open Folder", events.open_directory)
        # TODO open recent files 
        file_menu.add_separator()
        file_menu.add_item("Close Editor", events.close_file)
        file_menu.add_item("Close Folder", events.close_dir)
        file_menu.add_item("Close Window", events.quit)
        file_menu.add_separator()
        file_menu.add_item("Save", events.save)
        file_menu.add_item("Save As...", events.save_as)
        file_menu.add_item("Save All", events.save_all)
        file_menu.add_separator()
        file_menu.add_item("Exit", events.quit)

    def add_edit_menu(self):
        events = self.events

        edit_menu = self.add_menu("Edit")
        edit_menu.add_item("Undo", events.undo)
        edit_menu.add_item("Redo", events.redo)
        edit_menu.add_separator()
        edit_menu.add_item("Cut", events.cut)
        edit_menu.add_item("Copy", events.copy)
        edit_menu.add_item("Paste", events.paste)
        edit_menu.add_separator()
        edit_menu.add_item("Find",)
        edit_menu.add_item("Replace",)
    
    def add_view_menu(self):
        events = self.events

        view_menu = self.add_menu("View")
        view_menu.add_item("Side Bar",)
        view_menu.add_item("Console",)
        view_menu.add_item("Status Bar",)
        view_menu.add_item("Menu",)
        view_menu.add_separator()
        view_menu.add_item("Syntax",)
        view_menu.add_item("Indentation",)
        view_menu.add_item("Line Endings",)

    def close_all_menus(self, *_):
        for menu in self.menus:
            menu.hide()

    def switch_menu(self, menu):
        active = False
        for i in self.menus:
            if i.active:
                active = True
            if i != menu:
                i.hide()
        
        if active:
            menu.show()
