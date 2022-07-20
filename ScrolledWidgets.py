import tkinter as tk
import tkinter.ttk as ttk
from AutoScroll import _create_container, AutoScroll

class ScrolledListBox(AutoScroll, tk.Listbox):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledText(AutoScroll, tk.Text):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    """A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

    def insert(self, parent, index, iid=None, **kw):
        opts = ttk._format_optdict(kw)
        if iid is None:
            iid = "I{iid}".format(iid=format(len(self.get_children()) + 1, "03x"))
            
        return self.tk.call(self._w, "insert", parent, index, "-id", iid, *opts)

