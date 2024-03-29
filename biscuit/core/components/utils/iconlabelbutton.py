import tkinter as tk

from .codicon import get_codicon
from .frame import Frame


class IconLabelButton(Frame):
    def __init__(self, master, text=None, icon=None, function=lambda *_: None, iconside=tk.LEFT, padx=5, pady=1, expandicon=True, highlighted=False, *args, **kwargs) -> None:
        super().__init__(master, padx=padx, pady=pady, *args, **kwargs)
        self.function = function

        self.bg, self.fg, self.hbg, self.hfg = self.base.theme.utils.iconlabelbutton.values() if not highlighted else self.base.theme.utils.button.values()
        self.config(bg=self.bg)
        self.text = text
        self.icon = icon

        if icon:
            self.icon_label = tk.Label(self, text=get_codicon(self.icon), anchor=tk.E, 
                bg=self.bg, fg=self.fg, font=("codicon", 14))
            self.icon_label.pack(side=iconside, fill=tk.BOTH, expand=expandicon)

        if text:
            self.text_label = tk.Label(self, text=self.text, anchor=tk.W, pady=2,
                    bg=self.bg, fg=self.fg, font=("Segoe UI", 10))
            self.text_label.pack(side=iconside, fill=tk.BOTH, expand=True)

        self.config_bindings()
        self.visible = False

    def config_bindings(self) -> None:
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.bind("<Button-1>", self.on_click)
        if self.text:
            self.text_label.bind("<Button-1>", self.on_click)
        if self.icon:
            self.icon_label.bind("<Button-1>", self.on_click)

    def on_enter(self, *_) -> None:
        self.config(bg=self.hbg)
        if self.text:
            self.text_label.config(bg=self.hbg, fg=self.hfg)
        if self.icon:
            self.icon_label.config(bg=self.hbg, fg=self.hfg)

    def on_leave(self, *_) -> None:
        self.config(bg=self.bg)
        if self.text:
            self.text_label.config(bg=self.bg, fg=self.fg)
        if self.icon:
            self.icon_label.config(bg=self.bg, fg=self.fg)

    def on_click(self, *_) -> None:
        self.function()

    def change_text(self, text) -> None:
        self.text_label.config(text=text)

    def change_icon(self, icon) -> None:
        self.icon_label.config(text=icon)

    def set_pack_data(self, **kwargs) -> None:
        self.pack_data = kwargs

    def get_pack_data(self):
        return self.pack_data

    def show(self) -> None:
        if not self.visible:
            self.visible = True
            self.pack(**self.get_pack_data())

    def hide(self) -> None:
        if self.visible:
            self.visible = False
            self.pack_forget()
