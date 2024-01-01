from __future__ import annotations

import tkinter as tk
import typing

from biscuit.core.components.utils import Frame, Scrollbar

if typing.TYPE_CHECKING:
    from . import Hover


class Renderer(tk.Text):
    def __init__(self, master: Hover, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.base = master.base

    def render_markdown(self, rawmd):
        self.delete("1.0", tk.END)
        self.insert(tk.END, rawmd)
        self.update_idletasks()
