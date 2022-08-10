from .buttonsentry import ButtonsEntry
from .codicon import get_codicon
from .filetype import FileType
from .iconbutton import IconButton
from .label import WrappingLabel
from .scrollbar import Scrollbar
from .scrollframe import ScrollableFrame
from .tree import Tree


@staticmethod
def clamp(value, min_val, max_val):
    return min(max(min_val, value), max_val)